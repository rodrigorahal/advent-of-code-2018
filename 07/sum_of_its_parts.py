import fileinput
from collections import defaultdict


def parse():
    nodes = set()
    graph = defaultdict(list)
    for line in fileinput.input():
        words = line.strip().split()
        before, after = words[1], words[-3]
        graph[after].append(before)
        nodes.add(after)
        nodes.add(before)
    return graph, nodes


def topological_sort(graph):
    rank = dict()
    seen = set()

    def recur(node, seen, rank):
        if node not in graph or not graph[node]:
            rank[node] = 0
            return 0

        seen.add(node)

        for v in graph[node]:
            if v not in rank and v not in seen:
                recur(v, seen, rank)

        curr = max(rank[v] for v in graph[node]) + 1

        rank[node] = curr

        return curr

    for node in graph:
        recur(node, seen, rank)
    return rank


def order(nodes, graph, rank):
    done = set()
    res = []

    _, first = sorted([(v, k) for (k, v) in rank.items()])[0]
    done.add(first)
    res.append(first)

    while len(done) < len(nodes):
        available = sorted(
            [n for n in nodes - done if all(v in done for v in graph[n])]
        )
        nxt = available[0]
        done.add(nxt)
        res.append(nxt)
    return "".join(res)


def order_with_time(nodes, graph, rank, size, diff=60):
    available = set(node for node in rank if rank[node] == 0)
    in_progress = set()
    done = set()

    workers = [None for _ in range(size)]
    res = []

    for i, node in enumerate(list(available)[:size]):
        workers[i] = (0, node)
        in_progress.add(node)
        available.remove(node)

    for t in range(1_000):
        busy = [(i, worker) for i, worker in enumerate(workers) if worker]

        for i, (start, node) in busy:
            if t - start == diff + (ord(node) - ord("A") + 1):
                done.add(node)
                in_progress.remove(node)
                res.append(node)
                workers[i] = None

                for n in nodes:
                    if (
                        n not in in_progress
                        and n not in done
                        and all(v in done for v in graph[n])
                    ):
                        available.add(n)

        idle = set(i for i, worker in enumerate(workers) if worker is None)

        while available and idle:
            i = sorted(idle)[0]
            next = sorted(available)[0]
            in_progress.add(next)
            workers[i] = (t, next)

            available.remove(next)
            idle.remove(i)

        # display(workers, res, available, t)

        if len(done) == len(nodes):
            return t
    return -1


def display(workers, res, available, t):
    ws = " ".join(["." if w is None else w[1] for w in workers])
    av = "".join(available)

    print(f"{t:02}  {ws}  {''.join(res)}  {av}")


def main():
    graph, nodes = parse()
    rank = topological_sort(graph)

    in_order = order(nodes, graph, rank)
    print(f"Part 1: {in_order}")

    time = order_with_time(nodes, graph, rank, 5, diff=60)
    print(f"Part 1: {time}")


if __name__ == "__main__":
    main()
