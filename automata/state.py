from typing import override


class State:
    def __init__(self, name: str):
        self.name: str = name

    @override
    def __str__(self):
        return self.name

    @override
    def __repr__(self):
        return f"Node({self.name})"

    @override
    def __hash__(self) -> int:
        return hash(self.name)

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, State):
            return self.name == value.name
        else:
            return False
