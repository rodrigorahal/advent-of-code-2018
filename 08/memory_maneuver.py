from __future__ import annotations
import fileinput
from dataclasses import dataclass, field
from turtle import st
from typing import List, Tuple


@dataclass
class Node:
    children_size: int = None
    metadata_size: int = None
    children: List[Node] = field(default_factory=list)
    metadata: List[int] = field(default_factory=list)


def parse() -> List[int]:
    return [int(n) for n in fileinput.input().readline().strip().split()]


def parse_tree(numbers: List[int]) -> Tuple[Node, List[Node]]:
    root = Node()
    stack = [root]
    nodes = [root]

    i = 0
    while i < len(numbers):
        if not stack[-1].children_size and not stack[-1].metadata_size:
            children_size, metadata_size = numbers[i], numbers[i + 1]
            stack[-1].children_size = children_size
            stack[-1].metadata_size = metadata_size
            children = [Node() for _ in range(children_size)]
            stack[-1].children.extend(children)
            stack.extend(children)
            nodes.extend(children)
            i += 2
        else:
            metadata_size = stack[-1].metadata_size
            metadata = numbers[i : i + metadata_size]
            stack[-1].metadata.extend(metadata)
            i += metadata_size
            stack.pop()

    return root, nodes


def value(node: Node):
    if not node.children:
        return sum(node.metadata)
    children = list(reversed(node.children))
    return sum(value(children[i - 1]) for i in node.metadata if i <= node.children_size)


def main():
    numbers = parse()
    root, nodes = parse_tree(numbers)
    print(f"Part 1: {sum(sum(node.metadata) for node in nodes)}")
    print(f"Part 2: {value(root)}")


if __name__ == "__main__":
    main()
