import fileinput


def run(instructions, regs, ipreg):
    ip = regs[ipreg]

    while ip < len(instructions):
        opcode, A, B, C = instructions[ip]

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


def divisors(num):
    for div in range(1, num + 1):
        if num % div == 0:
            yield div


def main():
    cmds = parse()
    _, ipreg = cmds[0]
    regs = dict([(i, 0) for i in range(6)])
    run(cmds[1:], regs, ipreg)
    print(f"Part 1: {regs[0]}")

    # regs = dict([(i, 0) for i in range(6)])
    # regs[0] = 1
    # run(cmds[1:], regs, ipreg)
    """
    After manual inspection of program we find the following pattern:

    reg[0] = 1
    reg[1] = 1
    reg[2] = 10551376
    reg[3] = 1
    reg[4] = ip
    reg[5] = 1

    while reg[1] < reg[2]:
        reg[5] = 1
        while reg[5] <= reg[2]:
            reg[3] = reg[1] * reg[5]
            if reg[3] == reg[2]:
                reg[0] += 1
            reg[5] += 1
    
    This is the same as summing all divisors of 10551376
    """
    print(f"Part 2: {sum(divisors(num=10551376))}")


if __name__ == "__main__":
    main()
