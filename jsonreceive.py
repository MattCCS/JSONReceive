
import ctypes
import re


REGEX_NAME_ERROR = r"name '([^']+)' is not defined"


class DestructuredValue(object):
    pass


def walk(json_obj, path=()):
    if type(json_obj) is dict:
        for (k, v) in json_obj.items():
            for val in walk(v, path=path + (k,)):
                yield val

    if type(json_obj) in (list, tuple):
        for (i, obj) in enumerate(json_obj):
            for val in walk(obj, path=path + (i,)):
                yield val

    if path:
        yield (path, json_obj)


def get_nested(json_obj, path):
    for key in path:
        json_obj = json_obj[key]
    return json_obj


def parse(pattern):
    localz = {}
    while True:
        try:
            json_obj = eval(pattern, {}, localz)
            break
        except NameError as exc:
            name = re.match(REGEX_NAME_ERROR, str(exc)).group(1)
            localz[name] = DestructuredValue()

    paths = {}
    vals = list(localz.values())
    for (path, obj) in walk(json_obj):
        if obj in vals:
            paths[obj] = path

    return ((name, paths[obj]) for (name, obj) in localz.items())


def receive(pattern, json_obj, frame=None, local=True):
    values = {}
    varnames_and_paths = parse(pattern)
    for (varname, path) in varnames_and_paths:
        value = get_nested(json_obj, path)
        values[varname] = value

        if frame:
            if local:
                frame.f_locals[varname] = value
            else:
                frame.f_globals[varname] = value
            ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(0))

    return values
