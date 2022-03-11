import fileinput
from collections import defaultdict

OPCODES = [
    "addr",
    "addi",
    "mulr",
    "muli",
    "banr",
    "bani",
    "borr",
    "bori",
    "setr",
    "seti",
    "gtir",
    "gtri",
    "gtrr",
    "eqir",
    "eqri",
    "eqrr",
]


def parse():
    readings = []
    instructions = []
    last = False
    program = False
    for line in fileinput.input():

        if program:
            if line.strip():
                instructions.append(tuple(map(int, line.split())))
            continue

        if line.startswith("Before"):
            reading = []
            before = tuple(
                map(int, line.strip().strip("Before: [").strip("]").split(","))
            )
            reading.append(before)
            last = False
        elif line.startswith("After"):
            after = tuple(
                map(int, line.strip().strip("After: [").strip("]").split(","))
            )
            reading.append(after)
            readings.append(reading)
            last = False
        elif line.startswith("\n"):
            if last:
                program = True
            last = True
            continue
        else:
            instruction = tuple(map(int, line.split()))
            reading.append(instruction)
            last = False

    return readings, instructions


def run(instructions, regs):
    for opcode, A, B, C in instructions:

        if opcode == "addr":
            regs[C] = regs[A] + regs[B]

        elif opcode == "addi":
            regs[C] = regs[A] + B

        elif opcode == "mulr":
            regs[C] = regs[A] * regs[B]

        elif opcode == "muli":
            regs[C] = regs[A] * B

        elif opcode == "banr":
            regs[C] = regs[A] & regs[B]

        elif opcode == "bani":
            regs[C] = regs[A] & B

        elif opcode == "borr":
            regs[C] = regs[A] | regs[B]

        elif opcode == "bori":
            regs[C] = regs[A] | B

        elif opcode == "setr":
            regs[C] = regs[A]

        elif opcode == "seti":
            regs[C] = A

        elif opcode == "gtir":
            regs[C] = 1 if A > regs[B] else 0

        elif opcode == "gtri":
            regs[C] = 1 if regs[A] > B else 0

        elif opcode == "gtrr":
            regs[C] = 1 if regs[A] > regs[B] else 0

        elif opcode == "eqir":
            regs[C] = 1 if A == regs[B] else 0

        elif opcode == "eqri":
            regs[C] = 1 if regs[A] == B else 0

        elif opcode == "eqrr":
            regs[C] = 1 if regs[A] == regs[B] else 0

        else:
            print(opcode)
            assert False
    return regs


def simulate(readings):
    multiple = 0
    for reading in readings:
        if matches(reading) >= 3:
            multiple += 1
    return multiple


def matches(reading):
    before, inst, after = reading
    m = 0
    _, A, B, C = inst
    for opcode in OPCODES:
        res = run([(opcode, A, B, C)], dict(enumerate(before)))
        if tuple(res.values()) == after:
            m += 1
    return m


def get_candidates(readings):
    candidates = defaultdict(set)
    for before, inst, after in readings:
        code, A, B, C = inst
        for opcode in OPCODES:
            res = run([(opcode, A, B, C)], dict(enumerate(before)))
            if tuple(res.values()) == after:
                candidates[code].add(opcode)
    return candidates


def find_mappings(readings):
    found = set()
    candidates = get_candidates(readings)
    mappings = {}

    while len(found) != len(OPCODES):

        for code in candidates:
            candidates[code] -= found

        for code, opcodes in candidates.items():
            if len(opcodes) == 1:
                opcode = next(iter(opcodes))
                if opcode in found:
                    continue
                mappings[code] = opcode
                found.add(opcode)
    return mappings


def run_program(program, mappings):
    regs = dict(enumerate(range(4)))

    mapped = []
    for code, A, B, C in program:
        mapped.append((mappings[code], A, B, C))

    return run(mapped, regs)


def main():
    readings, program = parse()

    multiple = simulate(readings)
    print(f"Part 1: {multiple}")

    mappings = find_mappings(readings)

    regs = run_program(program, mappings)
    print(f"Part 2: {regs[0]}")


if __name__ == "__main__":
    main()
