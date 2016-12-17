#!/usr/bin/python3

import argparse
from pyparsing import OneOrMore, nestedExpr

import code


def parse(source):
    source = source.strip()
    return OneOrMore(nestedExpr()).parseString(source)


def interpret(ast):
    def impl(expr):
        if isinstance(expr, str):
            return int(expr)
        else: 
            res = {
                '+': lambda: impl(expr[1]) + impl(expr[2]),
                '-': lambda: impl(expr[1]) - impl(expr[2]),
                '*': lambda: impl(expr[1]) * impl(expr[2]),
                '/': lambda: impl(expr[1]) / impl(expr[2]),
                '^': lambda: impl(expr[1]) ** impl(expr[2]),
            }[expr[0]]()
            res = int(res) & 0xFF
            return res
    return impl(ast[0])


def compile(ast):
    bytecode = bytearray()
    def impl(expr):
        if isinstance(expr, str):
            bytecode.append(code.CMD_PUSH)
            value = int(expr)
            byte = value.to_bytes(1, byteorder='big')
            bytecode.append(byte[0])
        else: 
            impl(expr[1])
            impl(expr[2])
            op = {
                '+': code.CMD_ADD,
                '-': code.CMD_SUB,
                '*': code.CMD_MUL,
                '/': code.CMD_DIV,
                '^': code.CMD_POW,
            }[expr[0]]
            bytecode.append(op)

    impl(ast[0])
    return bytecode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Exec source code or compile it to bytecode.')
    parser.add_argument('input', help='Input source code file')
    parser.add_argument('--output', dest='output', help='Output for bytecode file')
    args = parser.parse_args()
    with open(args.input, 'r') as input:
        source = input.read()
        ast = parse(source)
        if args.output is not None:
            bytecode = compile(ast)
            with open(args.output, 'wb') as output:
                output.write(bytecode)
        else:
            print(interpret(ast))

