from typing import override

from automata.automaton import Automaton
from automata.nfa.epsilon import Epsilon, epsilon
from automata.state import State


class NFA(Automaton):
    def __init__(
        self,
        states: set[State],
        alphabet: set[str],
        transitions: dict[State, dict[str | Epsilon, set[State]]],
        initial: set[State],
        accepting: set[State],
    ):
        Automaton._validate_states(states)
        Automaton._validate_alphabet(alphabet)
        Automaton._validate_initial(initial)
        Automaton._validate_accepting(accepting)

        self.states: set[State] = states
        self.alphabet: set[str] = alphabet
        self.transitions: dict[State, dict[str | Epsilon, set[State]]] = transitions
        self.initial: set[State] = initial
        self.accepting: set[State] = accepting

        self._validate_transitions(transitions)

        if len(initial) > 1:
            _ = self._merge_initial_states()

    def epsilon_closure(self, states: set[State]):
        closure: set[State] = states
        stack: list[State] = list(states)
        while stack:
            state: State = stack.pop()
            if epsilon in self.transitions.get(state, {}):
                for next_state in self.delta(state, epsilon):
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def _merge_initial_states(self, new_initial: None | State = None) -> State:
        new_initial = new_initial or NFA._new_unique_state(self.states)
        self.transitions[new_initial] = {}
        self.transitions[new_initial][epsilon] = self.initial
        self.states.add(new_initial)
        self.initial = {new_initial}
        return new_initial

    def _merge_accepting_states(self, new_accepting: None | State = None) -> State:
        new_accepting = new_accepting or NFA._new_unique_state(self.states)
        for accepting in self.accepting:
            self.transitions[accepting] = {}
            self.transitions[accepting][epsilon] = {new_accepting}
        self.states.add(new_accepting)
        self.accepting = {new_accepting}
        return new_accepting

    @staticmethod
    def concat(nfa1: "NFA", nfa2: "NFA") -> "NFA":
        new_transitions = nfa1.transitions | nfa2.transitions
        for accepting in nfa1.accepting:
            new_transitions[accepting] = {}
            new_transitions[accepting][epsilon] = nfa2.initial
        return NFA(
            states=nfa1.states | nfa2.states,
            alphabet=nfa1.alphabet | nfa2.alphabet,
            transitions=new_transitions,
            initial=nfa1.initial,
            accepting=nfa2.accepting,
        )

    @staticmethod
    def union(nfa1: "NFA", nfa2: "NFA") -> "NFA":
        new_states = nfa1.states | nfa2.states
        new_transitions = nfa1.transitions | nfa2.transitions
        new_nfa = NFA(
            states=new_states,
            alphabet=nfa1.alphabet | nfa2.alphabet,
            transitions=new_transitions,
            initial=nfa1.initial | nfa2.initial,
            accepting=nfa1.accepting | nfa2.accepting,
        )
        _ = new_nfa._merge_accepting_states()
        return new_nfa

    @staticmethod
    def kleene_star(nfa: "NFA", plus: bool = False) -> "NFA":
        new_nfa = NFA(
            states=nfa.states,
            alphabet=nfa.alphabet,
            transitions=nfa.transitions,
            initial=nfa.initial,
            accepting=nfa.accepting,
        )
        new_initial = new_nfa._merge_initial_states()
        new_accepting = new_nfa._merge_accepting_states()
        if not plus:
            new_nfa.transitions[new_initial][epsilon] = new_nfa.transitions[
                new_initial
            ][epsilon] | {new_accepting}
        for accepting in nfa.accepting:
            new_nfa.transitions[accepting][epsilon] = (
                new_nfa.transitions[accepting][epsilon] | nfa.initial
            )
        return new_nfa

    @override
    def _traverse(self, string: str) -> tuple[list[State], bool]:
        is_valid: bool = False
        current_nodes: set[State] = self.epsilon_closure(self.initial)
        visited: list[State] = list(current_nodes)
        for symbol in string:
            if symbol not in self.alphabet:
                return visited, False
            next_nodes: set[State] = set()
            for node in current_nodes:
                next_nodes.update(self.delta(node, symbol))
            current_nodes = self.epsilon_closure(next_nodes)
            visited.extend(current_nodes)
        is_valid = any(state in self.accepting for state in current_nodes)
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
    def delta(self, state: State, symbol: str | Epsilon) -> set[State]:
        try:
            state_key = self.transitions.get(state)
            if state_key is None:
                return set()  # dead state
            return self.transitions[state].get(symbol, set())
        except KeyError:
            if symbol not in self.alphabet:
                raise KeyError(
                    f'Transition from {state!r} undefined for symbol "{symbol}".'
                ) from None
            return set()

    @override
    def display_transition_table(self):
        print("\t" + "\t".join((*self.alphabet, f"{epsilon}")))
        for state in self.states:
            print(f"{state}\t", end="")
            for symbol in self.alphabet | {epsilon}:
                print(
                    {state.name for state in self.delta(state, symbol)} or "∅", end="\t"
                )
            print()

    @override
    def _validate_transitions(
        self,
        transitions: dict[State, dict[str | Epsilon, set[State]]],
    ):
        if not transitions:
            raise ValueError("No transitions.")
        symbols = {
            symb
            for val in transitions.values()
            for symb in val.keys()
            if symb is not epsilon
        }
        states = {state for state in transitions} | {
            state
            for _state in self.states
            for states in transitions.get(_state, {}).values()
            for state in states
        }
        if any(state not in self.states for state in states):
            raise ValueError("Some state/s in transitions undefined in set of states.")
        elif any(symb not in self.alphabet for symb in symbols):
            raise ValueError("Transition symbols and alphabet do not match.")
