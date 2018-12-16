"""AoC 2018 Day 16: Chronal Classification"""

import re
from collections import namedtuple

# Part 1

Sample = namedtuple("Sample", ['before', 'instruction', 'after'])
Instruction = namedtuple('Instruction', ['op', 'A', 'B', 'C'])


def read_digits(line):
    return [int(i) for i in re.findall(r'(\d+)', line)]


def parse_input(filename):
    with open(filename) as f:
        sample_list = []
        # Read 4 lines at a time
        for before, instr, after, _ in zip(f, f, f, f):
            if not before.startswith("Before"):
                break
            before_list = read_digits(before)
            after_list = read_digits(after)
            instruction = Instruction(*read_digits(instr))
            sample_list.append(Sample(before_list, instruction, after_list))
    return sample_list


def addr(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A] + reg[instr.B]
    return reg


def addi(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A] + instr.B
    return reg


def mulr(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A] * reg[instr.B]
    return reg


def muli(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A] * instr.B
    return reg


def banr(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A] & reg[instr.B]
    return reg


def bani(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A] & instr.B
    return reg


def borr(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A] | reg[instr.B]
    return reg


def bori(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A] | instr.B
    return reg


def setr(regi, instr):
    reg = regi.copy()
    reg[instr.C] = reg[instr.A]
    return reg


def seti(regi, instr):
    reg = regi.copy()
    reg[instr.C] = instr.A
    return reg


def gtir(regi, instr):
    reg = regi.copy()
    reg[instr.C] = (instr.A > reg[instr.B]) * 1
    return reg


def gtri(regi, instr):
    reg = regi.copy()
    reg[instr.C] = (reg[instr.A] > instr.B) * 1
    return reg


def gtrr(regi, instr):
    reg = regi.copy()
    reg[instr.C] = (reg[instr.A] > reg[instr.B]) * 1
    return reg


def eqir(regi, instr):
    reg = regi.copy()
    reg[instr.C] = (instr.A == reg[instr.B]) * 1
    return reg


def eqri(regi, instr):
    reg = regi.copy()
    reg[instr.C] = (reg[instr.A] == instr.B) * 1
    return reg


def eqrr(regi, instr):
    reg = regi.copy()
    reg[instr.C] = (reg[instr.A] == reg[instr.B]) * 1
    return reg


def count_possible(sample):
    """
    Test all possible operation on the sample. Returns the number of valid
    operations (that would produce the good after given before and instruction)
    """
    operations = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti,
                  gtir, gtri, gtrr, eqir, eqri, eqrr]
    count = 0
    for op in operations:
        if op(sample.before, sample.instruction) == sample.after:
            count += 1
    return count


def test_all(samples):
    total = 0
    for sample in samples:
        if count_possible(sample) >= 3:
            total += 1
    return total


sample_test = Sample([3, 2, 1, 1], Instruction(9, 2, 1, 2), [3, 2, 2, 1])
assert count_possible(sample_test) == 3

samples = parse_input("day16_input.txt")
print(f'Solution for part 1: {test_all(samples)}')
