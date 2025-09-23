from typing import override


class State:
    base_name: str = "q"
    instance_counter: int = 0

    def __init__(self, name: str | None = None):
        if name is not None:
            self.set_name(name)
        else:
            self.name: str = f"{State.base_name}{State.instance_counter}"
            State.instance_counter += 1

    def set_name(self, name: str):
        if not isinstance(name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("State name must be of type string.")  # pyright: ignore[reportUnreachable]
        self.name = name

    @override
    def __str__(self):
        return self.name

    @override
    def __repr__(self):
        return f'State("{self.name}")'

    @override
    def __hash__(self) -> int:
        return hash(self.name)

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, State):
            return self.name == value.name
        else:
            return False

    @classmethod
    def set_base_name(cls, base_name: str):
        if not isinstance(base_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("Base name must be of type string.")  # pyright: ignore[reportUnreachable]
        cls.base_name = base_name

    @classmethod
    def reset_naming(cls):
        cls.base_name = "q"
        cls.instance_counter = 0

    @classmethod
    def from_set(cls, states: set["State"]) -> "State":
        return State(
            f"{{{','.join(state.name for state in sorted(states, key=lambda s: s.name))}}}"
        )
