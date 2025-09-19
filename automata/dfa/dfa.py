from typing import override

from automata.automaton import Automaton
from automata.nfa import epsilon
from automata.state import State


class DFA(Automaton):
    def __init__(
        self,
        states: set[State],
        alphabet: set[str],
        transitions: dict[State, dict[str, State]],
        initial: State,
        accepting: set[State],
    ):
        Automaton._validate_states(states)
        Automaton._validate_accepting(accepting)
        Automaton._validate_alphabet(alphabet)
        Automaton._validate_initial(initial)

        self.states: set[State] = states
        self.alphabet: set[str] = alphabet
        self.transitions: dict[State, dict[str, State]] = transitions
        self.initial: State = initial
        self.accepting: set[State] = accepting

        self._validate_transitions(transitions)

    @override
    def _traverse(self, string: str) -> tuple[list[State], bool]:
        is_valid: bool = False
        current_node: State | None = self.initial
        visited: list[State] = [current_node]
        for symbol in string:
            if symbol not in self.alphabet:
                return visited, False
            current_node = self.delta(current_node, symbol)
            if current_node is None:
                return visited, False
            is_valid = current_node in self.accepting
            visited.append(current_node)
        return visited, is_valid

    @override
    def accepts(self, string: str) -> bool:
        _, is_valid = self._traverse(string)
        return is_valid

    @override
    def state_transitions(self, string: str) -> list[State]:
        states, _ = self._traverse(string)
        return states

    @override
    def delta(self, state: State, symbol: str) -> State | None:
        try:
            state_key = self.transitions.get(state)
            if state_key is None:
                return None  # dead state
            return self.transitions[state].get(symbol)
        except KeyError:
            raise KeyError(
                f'Transition from {state!r} undefined for symbol "{symbol}".'
            )

    @override
    def _validate_transitions(
        self,
        transitions: dict[State, dict[str, State]],
    ):
        if not transitions:
            raise ValueError("No transitions.")
        symbols = {symb for val in transitions.values() for symb in val.keys()}
        states = {state for state in self.transitions} | {
            state
            for _state in self.states
            for state in self.transitions.get(_state, {}).values()
        }
        if epsilon in symbols:
            raise TypeError("epsilon not allowed in DFA.")
        elif any(state not in self.states for state in states):
            raise ValueError("Some state/s in transitions undefined in set of states.")
        elif any(symb not in self.alphabet for symb in symbols):
            raise ValueError("Transition symbols and alphabet do not match.")

    @override
    def display_transition_table(self):
        print("\t" + "\t".join(self.alphabet))
        for state in self.states:
            print(f"{state!s}\t", end="")
            for symbol in self.alphabet:
                print(self.delta(state, symbol) or "∅", end="\t")
            print()
