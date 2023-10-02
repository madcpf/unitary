# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unitary.alpha as alpha
from enums import (
    SquareState,
    GameState
)

class Board:
    def __init__(self):
        chess_board = {}
        for col in 'abcdefghi':
            for row in '09':
                chess_board[col+row]= alpha.QuantumObject(col+row, SquareState.OCCUPIED)
            for row in '1458':
                chess_board[col+row]= alpha.QuantumObject(col+row, SquareState.EMPTY)
        for row in '27':
            for col in 'bh':
                chess_board[col+row]= alpha.QuantumObject(col+row, SquareState.OCCUPIED)
            for col in 'acdefgi':
                chess_board[col+row]= alpha.QuantumObject(col+row, SquareState.EMPTY)
        for row in '36':
            for col in 'acegi':
                chess_board[col+row]= alpha.QuantumObject(col+row, SquareState.OCCUPIED)
            for col in 'bdfh':
                chess_board[col+row]= alpha.QuantumObject(col+row, SquareState.EMPTY)           
        self.board = alpha.QuantumWorld(chess_board.values())
        self.load_fen("RHEAGAEHR/9/1C5C1/S1S1S1S1S/9/9/s1s1s1s1s/1c5c1/9/rheagaehr")
        self.general_locations = {"e0", "e9"}
        self.current_state = GameState.CONTINUE

    def load_fen(self):
        y = self.size
        for row in fen.split("/"):
            y -= 1
            x = 0
            for char in row:
                if "1" <= char <= "9":
                    x += int(char)
                else:
                    piece = c.REV_PIECES[char]
                    square = to_square(x, y)
                    self._pieces[square] = piece
                    x += 1
        self.board.with_state(self._bit_board())
        self._probs = self.board.get_probability_distribution(self.reps)

    def print(self):
        print("### board print to be implemented")

    def flying_general(self) -> bool:
        print("### flying general rule check to be implemented")
        return False
        
