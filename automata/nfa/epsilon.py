from typing import override


class Epsilon:
    @override
    def __str__(self):
        return "ε"

    @override
    def __repr__(self):
        return "epsilon"

    @override
    def __hash__(self) -> int:
        return 0


epsilon: Epsilon = Epsilon()
