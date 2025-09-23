from automata.nfa.nfa import NFA
from automata.state import State

precedence = {"*": 2, "+": 2, "|": 1}


class ParsingError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


class RegExParser:
    @classmethod
    def to_nfa(cls, re: str) -> NFA:
        return cls.compile(cls.parse(cls.tokenize(re)))

    @classmethod
    def tokenize(cls, re: str) -> list[tuple[str, str]]:
        tokens: list[tuple[str, str]] = []
        i = 0
        while i < len(re):
            char = re[i]
            if char.isalnum():
                tokens.append(("CHARACTER", char))
            elif char == "|":
                tokens.append(("UNION", char))
            elif char == "*":
                tokens.append(("STAR", char))
            elif char == "+":
                tokens.append(("PLUS", char))
            elif char == "(":
                tokens.append(("LPAREN", char))
            elif char == ")":
                tokens.append(("RPAREN", char))
            else:
                raise ParsingError(f"Unrecognized symbol: {char}")
            i += 1
        return tokens

    @classmethod
    def parse(cls, tokens: list[tuple[str, str]]) -> list[str]:
        """
        Modified shunting yard algorithm for regular expression
        and added support for (postfix) Keene star and positive closure.
        """
        out_queue: list[str] = []
        op_stack: list[str] = []
        for token_type, symbol in tokens:
            if token_type == "CHARACTER":
                out_queue.append(symbol)
            elif token_type in ("STAR", "PLUS"):
                try:
                    if out_queue[-1] in ("*", "+"):
                        raise ParsingError(
                            "Invalid regular expression with Kleene star."
                        )
                except IndexError:
                    raise ParsingError("Invalid regular expression with Kleene star.")
                out_queue.append(symbol)
            elif token_type == "UNION":
                while (
                    op_stack
                    and op_stack[-1] != "("
                    and precedence[symbol] <= precedence[op_stack[-1]]
                ):
                    out_queue.append(op_stack.pop())
                op_stack.append(symbol)
            elif token_type == "LPAREN":
                op_stack.append(symbol)
            elif token_type == "RPAREN":
                try:
                    while (op_stack[-1]) != "(":
                        out_queue.append(op_stack.pop())
                except IndexError:
                    raise ParsingError("Mismatched parentheses.")
                not_lp = op_stack.pop()
                if not_lp[-1] != "(":
                    raise ParsingError("Mismatched parentheses.")
        while op_stack:
            not_lp = op_stack[-1]
            if not_lp[-1] == "(":
                raise ParsingError("Mismatched parentheses.")
            out_queue.append(op_stack.pop())
        return out_queue

    @classmethod
    def compile(cls, parsed_tokens: list[str]) -> NFA:
        stack: list[NFA] = []
        try:
            while parsed_tokens:
                token = parsed_tokens.pop(0)
                if token.isalnum():
                    stack.append(cls.atomic_nfa(token))
                elif token == "*":
                    stack.append(NFA.kleene_star(stack.pop(0)))
                elif token == "+":
                    stack.append(NFA.kleene_star(stack.pop(0), plus=True))
                elif token == "|":
                    r = stack.pop()
                    l = stack.pop()
                    stack.append(NFA.union(r, l))
                else:
                    raise ParsingError(f"Invalid token: {token}.")
        except IndexError:
            raise ParsingError("Invalid regular expression.")
        out = stack.pop(0)
        while stack:
            out = NFA.concat(out, stack.pop(0))
        State.reset_naming()
        return out

    @classmethod
    def atomic_nfa(cls, symbol: str):
        return NFA({i := State(), a := State()}, {symbol}, {i: {symbol: {a}}}, {i}, {a})


if __name__ == "__main__":
    nfa = RegExParser.to_nfa("ab|c*")
    print(nfa)
