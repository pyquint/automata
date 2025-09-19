from abc import ABC, abstractmethod

from automata.state import State


class Automaton(ABC):
    base_state_name: str = "new"

    @classmethod
    def set_base_state_name(cls, base_name: str):
        if not isinstance(base_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("Base name must be of type string.")  # pyright: ignore[reportUnreachable]
        cls.base_state_name = base_name

    @staticmethod
    def _validate_states(states: set[State]):
        Automaton.__validate_sets_of_states(states, "states")

    @staticmethod
    def _validate_alphabet(alphabet: set[str]):
        if not alphabet:
            raise ValueError("Parameter alphabet must have at least one element.")
        elif any(not isinstance(symbol, str) for symbol in alphabet):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("All elements in alphabet must be of type State.")
        elif any(len(symbol) != 1 for symbol in alphabet):
            raise ValueError("Alphabet must only contain strings of length 1.")

    @staticmethod
    def _validate_initial(initial: State | set[State]):
        if isinstance(initial, set):
            Automaton.__validate_sets_of_states(initial, "initial")

    @staticmethod
    def _validate_accepting(accepting: set[State]):
        if not accepting == set():
            Automaton.__validate_sets_of_states(accepting, "initial")

    @abstractmethod
    def _validate_transitions(self, transitions):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        pass

    @abstractmethod
    def _traverse(self, string: str) -> tuple[list[State], bool]:
        pass

    @abstractmethod
    def accepts(self, string: str) -> bool:
        pass

    @abstractmethod
    def state_transitions(self, string: str) -> list[State]:
        pass

    @abstractmethod
    def delta(self, state: State, symbol: str) -> None | State | set[State]:
        pass

    @staticmethod
    def __validate_sets_of_states(_states: set[State], parameter_name: str):
        if not _states:
            raise ValueError(
                f"Parameter {parameter_name} must have at least one State object."
            )
        elif any(not isinstance(state, State) for state in _states):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"All elements in {parameter_name} must be of type State.")

    @classmethod
    def _new_unique_state(cls, existing: set[State]):
        counter: int = 0
        name: str = f"{cls.base_state_name}{counter}"
        while any(s.name == name for s in existing):
            name = f"{cls.base_state_name}{counter}"
            counter += 1
        return State(name)

    @abstractmethod
    def display_transition_table(self):
        pass
