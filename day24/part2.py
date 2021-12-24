from __future__ import annotations

import argparse
import operator
import os.path
from typing import Any
from typing import Protocol

import pytest
from z3 import Int
from z3 import Optimize
from z3 import sat

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class _Expr(Protocol):
    @property
    def left(self) -> int | _Expr | Var: ...
    @property
    def op(self) -> str: ...
    @property
    def right(self) -> int | _Expr | Var: ...
    def __add__(self, other: object) -> _Expr: ...
    def __radd__(self, other: object) -> _Expr: ...
    def __mul__(self, other: object) -> int | _Expr: ...
    def __rmul__(self, other: object) -> int | _Expr: ...
    def __floordiv__(self, other: object) -> _Expr: ...
    def __rfloordiv__(self, other: object) -> _Expr: ...
    def __mod__(self, other: object) -> _Expr: ...
    def __rmod__(self, other: object) -> _Expr: ...


class Expr:
    def __init__(
            self,
            left: int | _Expr | Var,
            op: str,
            right: int | _Expr | Var,
    ) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return (
            f'{type(self).__name__}('
            f'left={self.left!r}, '
            f'op={self.op!r}, '
            f'right={self.right!r})'
        )

    def __add__(self, other: object) -> _Expr:
        if other == 0:
            return self
        elif isinstance(other, (int, Expr, Var)):
            return type(self)(self, '+', other)
        else:
            raise AssertionError('unexpected', self, other)

    __radd__ = __add__

    def __mul__(self, other: object) -> int | _Expr:
        if other == 0:
            return 0
        elif other == 1:
            return self
        elif isinstance(other, (int, Expr)):
            return type(self)(self, '*', other)
        else:
            raise AssertionError('unexpected', self, other)

    __rmul__ = __mul__

    def __floordiv__(self, other: object) -> _Expr:
        if other == 1:
            return self
        elif isinstance(other, (int, Expr)):
            return type(self)(self, '//', other)
        else:
            raise AssertionError('unexpected', self, other)

    def __mod__(self, other: object) -> _Expr:
        if isinstance(other, (int, Expr)):
            return type(self)(self, '%', other)
        else:
            raise AssertionError('unexpected', self, other)

    def not_supported(self, other: object) -> _Expr:
        raise AssertionError('unexpected', self, other)

    __rfloordiv__ = __rmod__ = not_supported

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            assert other in (0, 1), other
            return False
        assert self.op == '+'
        assert isinstance(self.right, int), self.right
        assert self.right < 1 or self.right >= 10
        assert isinstance(other, Var)
        return False


class Var:
    def __init__(self, digit: int) -> None:
        self.digit = digit

    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.digit})'

    def __add__(self, other: object) -> Var | Expr:
        if other == 0:
            return self
        elif isinstance(other, (int, Expr)):
            return Expr(other, '+', self)
        else:
            raise AssertionError(self, other)

    __radd__ = __add__

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        else:
            assert isinstance(other, int), (self, other)
            assert other < 1 or other >= 10
            return False

    def not_supported(self, other: object) -> bool:
        raise AssertionError('unreachable!', self, other)

    __mul__ = __rmul__ = not_supported
    __floordiv__ = __rfloordiv__ = not_supported
    __mod__ = __rmod__ = not_supported


def compute(s: str) -> int:
    variables: dict[str, int | _Expr | Var] = {
        'x': 0,
        'y': 0,
        'z': 0,
    }
    var_w = Var(-1)

    def lookup(s: str) -> int | _Expr | Var:
        if s == 'w':
            return var_w
        elif s.isalpha():
            return variables[s]
        else:
            return int(s)

    ops = {
        '+': operator.add,
        '*': operator.mul,
        '//': operator.truediv,
        '%': operator.mod,
    }

    def _to_z3(expr: int | _Expr | Var) -> Any:
        if isinstance(expr, bool):
            return int(expr)
        elif isinstance(expr, int):
            return expr
        elif isinstance(expr, Var):
            return digits[expr.digit]
        else:
            return ops[expr.op](_to_z3(expr.left), _to_z3(expr.right))

    digits = [Int(f'W_{i}') for i in range(14)]
    o = Optimize()
    for digit in digits:
        o.add(1 <= digit)
        o.add(digit < 10)

    for line in s.splitlines():
        cmd = line.split()
        if cmd[0] == 'inp':
            var_w = Var(var_w.digit + 1)
        elif cmd[0] == 'add':
            if cmd[2].startswith('-'):
                o.add(
                    digits[var_w.digit] == _to_z3(variables['x'] + int(cmd[2]))
                )
                variables['x'] = var_w
            else:
                variables[cmd[1]] += lookup(cmd[2])
        elif cmd[0] == 'mul':
            if cmd[2] == '0':
                variables[cmd[1]] = 0
            else:
                variables[cmd[1]] *= lookup(cmd[2])
        elif cmd[0] == 'div':
            variables[cmd[1]] //= lookup(cmd[2])
        elif cmd[0] == 'mod':
            variables[cmd[1]] %= lookup(cmd[2])
        elif cmd[0] == 'eql':
            variables[cmd[1]] = (variables[cmd[1]] == lookup(cmd[2]))
        else:
            raise AssertionError(cmd)

    sum_v = Int('Sum')
    o.add(sum_v == sum(var * 10 ** (13 - i) for i, var in enumerate(digits)))
    o.minimize(sum_v)
    assert o.check() == sat
    model = o.model()
    return model[sum_v]


INPUT_S = '''\

'''
EXPECTED = 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
