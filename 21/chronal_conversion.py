import fileinput


def run(instructions, regs, ipreg, p1=True):
    ip = regs[ipreg]

    last = None
    seen = set()

    while ip < len(instructions):
        opcode, A, B, C = instructions[ip]

        if opcode == "eqrr":
            if p1:
                return regs[5]
            else:
                if regs[5] in seen:
                    return last
                seen.add(regs[5])
                last = regs[5]

        regs[ipreg] = ip

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

        ip = regs[ipreg]
        ip += 1

    return regs


def parse():
    cmds = []
    for line in fileinput.input():
        words = line.split()
        if len(words) == 2:
            cmds.append([words[0], int(words[1])])
        else:
            cmds.append([words[0]] + [int(word) for word in words[1:]])
    return cmds


def main():
    cmds = parse()
    _, ipreg = cmds[0]
    regs = dict([(i, 0) for i in range(6)])
    print(f"Part 1: {run(cmds[1:], regs, ipreg)}")
    regs = dict([(i, 0) for i in range(6)])
    print(f"Part 2: {run(cmds[1:], regs, ipreg, p1=False)}")


if __name__ == "__main__":
    main()
