from abc import ABC, abstractmethod

from automata.state import State


class Automaton(ABC):
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
        new_state = State()
        while new_state in existing:
            print(existing)
            print(State.base_name, State.instance_counter)
            print(f"new: {new_state!r}")
            new_state = State()
        return new_state

    @abstractmethod
    def print_transition_function(self):
        pass
