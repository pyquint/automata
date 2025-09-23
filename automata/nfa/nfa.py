from functools import reduce
from typing import override

from automata.automaton import Automaton
from automata.dfa.dfa import DFA
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

    @classmethod
    def concat(cls, nfa1: "NFA", nfa2: "NFA") -> "NFA":
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

    @classmethod
    def union(cls, nfa1: "NFA", nfa2: "NFA") -> "NFA":
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

    @classmethod
    def kleene_star(cls, nfa: "NFA", plus: bool = False) -> "NFA":
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

    def to_dfa(self) -> DFA:
        dfa_initial = self.epsilon_closure(self.initial)
        dfa_states: list[set[State]] = [dfa_initial]
        dfa_transitions: dict[State, dict[str, State]] = {}

        # Algorithms & Models of Computation
        # CS/ECE  374, Fall 2020
        # 5.1.2: Algorithm for converting NFA to DFA, p.11
        subsets_to_check = [dfa_initial]
        while subsets_to_check:
            X = subsets_to_check.pop(0)
            new_dfa_transition = State.from_set(X)
            dfa_transitions[new_dfa_transition] = {}
            for a in self.alphabet:
                U: set[State] = set()
                for q in X:
                    x1 = self.epsilon_closure({q})
                    y1 = reduce(set[State].union, (self.delta(p, a) for p in x1))
                    zqa = reduce(
                        set[State].union, (self.epsilon_closure({r}) for r in y1), set()
                    )
                    U.update(zqa)
                    if U not in dfa_states:
                        subsets_to_check.append(U)
                        dfa_states.append(U)
                    dfa_transitions[new_dfa_transition][a] = State.from_set(U)

        dfa_accepting = {
            State.from_set(state)
            for state in dfa_states
            if self.accepting.intersection(state)
        }
        nullstate = State.from_set(set())
        for a in self.alphabet:
            dfa_transitions[nullstate][a] = nullstate
        return DFA(
            {State.from_set(s) for s in dfa_states},
            self.alphabet,
            dfa_transitions,
            State.from_set(dfa_initial),
            dfa_accepting,
        )

    @override
    def _traverse(self, string: str) -> tuple[list[State], bool]:
        if not isinstance(string, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("DFA expects string input only.")  # pyright: ignore[reportUnreachable]
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

    @override
    def print_transition_function(self):
        for curr in sorted(self.transitions, key=lambda x: x.name):
            for symbol in (symbols := self.transitions[curr]):
                dests = ", ".join(
                    dest.name for dest in sorted(symbols[symbol], key=lambda x: x.name)
                )
                print(f"δ({curr},{symbol}) = {{{dests}}}")
