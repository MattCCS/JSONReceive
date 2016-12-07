#!/usr/local/bin/python3

import inspect
import json

from . import jsonreceive


def test():
    pattern = """\
{
    'foo': foo,
    'bar': {
        'stuff': things,
        'buzz': {
            'doesnt have to match': fruit,
            'deep data': [first, second],
        },
    }
}
"""

    for item in jsonreceive.parse(pattern):
        print(item)

    data = {'foo': 5, 'bar': {'stuff': [1, 2, 3], 'buzz': {'ignorable': 'trash', 'doesnt have to match': 'apple', 'deep data': ['joe', 'bob']}}}

    print("\nWithout mutation:")
    print("Output: {}".format(jsonreceive.receive(pattern, data)))
    print("Locals: {}".format(locals()))
    try:
        print((foo, fiz, fruit, first, second))
    except NameError as exc:
        print("-> Got the exception we expected: {}".format(exc))

    foo = things = fruit = first = second = None
    print(inspect.stack())
    print(inspect.currentframe())
    print("\nWith mutation:")
    print("Output: {}".format(jsonreceive.receive(pattern, data, frame=inspect.currentframe(), local=True)))
    print("Locals: {}".format(locals()))

    print("\nNew local variables:")
    print("-> Now the local variables exist: {}".format((foo, things, fruit, first, second)))

    output = jsonreceive.receive(pattern, data)
    print("\nSummary:")
    print("--------")
    print("\nPattern: \n{}".format(pattern))
    print("\nJSON data: \n{}".format(json.dumps(data, indent=4)))
    print("\nMatched values: \n{}".format(json.dumps(output, indent=4)))


def wrap():
    test()
    print(foo)  # <-- should also fail


def main():
    wrap()
    print(foo)  # <-- should fail


if __name__ == '__main__':
    main()
