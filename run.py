#!/usr/bin/python3

import argparse

import code


def run(bytecode):
    stack = list()
    it = iter(bytecode)
    for byte in it:
        if byte == code.CMD_PUSH:
            byte = next(it)
            stack.append(byte)
        else:
            op = {
                code.CMD_ADD: lambda a, b: a + b,
                code.CMD_SUB: lambda a, b: a - b,
                code.CMD_MUL: lambda a, b: a * b,
                code.CMD_DIV: lambda a, b: a / b,
                code.CMD_POW: lambda a, b: a ** b,
            }[byte]
            b = stack.pop()
            a = stack.pop()
            res = int(op(a, b)) & 0xFF
            stack.append(res)
    return stack.pop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Exec bytecode.')
    parser.add_argument('input', help='Input bytecode file')
    args = parser.parse_args()
    with open(args.input, 'rb') as input:
        bytecode = bytes(input.read())
        result = run(bytecode)
        print(result)
