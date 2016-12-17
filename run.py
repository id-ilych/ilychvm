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
            b = stack.pop()
            a = stack.pop()
            if byte == code.CMD_ADD:
                stack.append(a + b)
            elif byte == code.CMD_SUB:
                stack.append(a - b)
            elif byte == code.CMD_MUL:
                stack.append(a * b)
            elif byte == code.CMD_DIV:
                stack.append(a / b)
            elif byte == code.CMD_POW:
                stack.append(a ** b)
            else:
                raise 'unknown cmd {:02X}'.format(byte)
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
