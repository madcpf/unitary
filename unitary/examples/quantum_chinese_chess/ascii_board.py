# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import math
from typing import Optional, Sequence

import unitary.examples.quantum_chinese_chess.bit_utils as bu
import unitary.examples.quantum_chinese_chess.constants as c
import unitary.examples.quantum_chinese_chess.enums as enums
import unitary.examples.quantum_chinese_chess.quantum_board as qb
from unitary.quantum_chess.move import Move

_ORD_A = ord("a")


def to_rank(x: int) -> str:
    """Returns the algebraic notation rank from the x coordinate."""
    return chr(_ORD_A + x)


def to_square(x: int, y: int) -> str:
    """Returns the algebraic notation of a square, ranging from a0 to i9."""
    return chr(_ORD_A + x) + str(y)


def x_of(square: str) -> int:
    """Returns x coordinate of an algebraic notation square (e.g. 'f4'->5)."""
    return ord(square[0]) - _ORD_A


def y_of(square: str) -> int:
    """Returns y coordinate of an algebraic notation square (e.g. 'f4'->4)."""
    return int(square[1])
