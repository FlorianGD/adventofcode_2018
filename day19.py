"""AoC 2018 Day 19: Go With The Flow"""

from collections import namedtuple
from itertools import count

# Part 1
Instruction = namedtuple('Instruction', ['op', 'A', 'B', 'C'])


def mulr(reg, instr):
    reg[instr.C] = reg[instr.A] * reg[instr.B]


def muli(reg, instr):
    reg[instr.C] = reg[instr.A] * instr.B


def gtir(reg, instr):
    reg[instr.C] = (instr.A > reg[instr.B]) * 1


def gtri(reg, instr):
    reg[instr.C] = (reg[instr.A] > instr.B) * 1


def gtrr(reg, instr):
    reg[instr.C] = (reg[instr.A] > reg[instr.B]) * 1


def eqir(reg, instr):
    reg[instr.C] = (instr.A == reg[instr.B]) * 1


def eqri(reg, instr):
    reg[instr.C] = (reg[instr.A] == instr.B) * 1


def eqrr(reg, instr):
    reg[instr.C] = (reg[instr.A] == reg[instr.B]) * 1


def addr(reg, instr):
    reg[instr.C] = reg[instr.A] + reg[instr.B]


def addi(reg, instr):
    reg[instr.C] = reg[instr.A] + instr.B


def setr(reg, instr):
    reg[instr.C] = reg[instr.A]


def seti(reg, instr):
    reg[instr.C] = instr.A


def read_program(prog):
    program = []
    bound_reg = int(prog[0][-1])
    for line in prog[1:]:
        splitted = line.split(' ')
        # splitted[0] = eval(splitted[0])
        splitted[1:] = [int(i) for i in splitted[1:]]
        program.append(Instruction(*splitted))
    return bound_reg, program


def execute_line(bound_reg, ip, instr, registers):
    registers[bound_reg] = ip
    eval(instr.op)(registers, instr)
    ip = registers[bound_reg]
    ip += 1
    return ip


def execute_program(bound_reg, program):
    registers = [0] * 6
    ip = 0
    while True:
        try:
            ip = execute_line(bound_reg, ip, program[ip], registers)
        except IndexError:
            break
    return registers


def read_and_execute(prog):
    bound_reg, program = read_program(prog)
    registers = execute_program(bound_reg, program)
    return registers[0]


test_prog = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""".splitlines()

assert read_and_execute(test_prog) == 6

with open('day19_input.txt') as f:
    day = f.read().splitlines()

# print(f'Solution for part 1: {read_and_execute(day)}')

# Part 2
# The same except register 0 starts with value 1


def execute_program_part2(bound_reg, program):
    registers = [0] * 6
    registers[0] = 1
    ip = 0
    for i in count():
        try:
            print(f'ip: {ip}: {program[ip]}:  {registers}')
            ip = execute_line(bound_reg, ip, program[ip], registers)
            # if i % 100000 == 0:
            if i > 100:
                break
        except IndexError:
            break
    return registers


def read_and_execute_part2(prog):
    bound_reg, program = read_program(prog)
    registers = execute_program_part2(bound_reg, program)
    return registers[0]


print(f'Solution for part 2: {read_and_execute_part2(day)}')
# It is way too long, and I need to put a pen and paper to figure out
# what is going on, and take shortcuts in the calculation
