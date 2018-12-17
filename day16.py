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

# Part 2


def find_opcodes(samples):
    """
    Go through the samples to identify the operation associated with the code
    """
    operations = set([addr, addi, mulr, muli, banr, bani, borr, bori,
                      setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr])
    opcodes = [operations] * 16

    # Utility to update the opcodes when one is found
    def remove_found_opcode(opcodes, num_found, op_found):
        for i, possibles in enumerate(opcodes):
            if i != num_found:
                possibles.difference_update(op_found)
        return opcodes
    # Loop through the samples
    samples_iter = iter(samples)
    while max(map(len, opcodes)) > 1:
        sample = next(samples_iter)
        possible = set()
        for op in opcodes[sample.instruction.op]:
            if op(sample.before, sample.instruction) == sample.after:
                possible.add(op)
        opcodes[sample.instruction.op] = (
            opcodes[sample.instruction.op].intersection(possible)
        )
        if len(opcodes[sample.instruction.op]) == 1:
            opcodes = remove_found_opcode(opcodes,
                                          sample.instruction.op,
                                          opcodes[sample.instruction.op])
    return [fun for op in opcodes for fun in op]


def parse_input_part2(filename):
    prog = []
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            if i >= 3238:
                prog.append(Instruction(*read_digits(line)))
    return prog


def exectute_program(program, opcodes):
    registers = [0, 0, 0, 0]
    for instr in program:
        registers = opcodes[instr.op](registers, instr)
    return registers


program = parse_input_part2('day16_input.txt')
opcodes = find_opcodes(samples)
registers = exectute_program(program, opcodes)
print(f'Solution for part 2: {registers[0]}')
