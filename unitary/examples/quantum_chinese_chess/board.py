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
from typing import List
import unitary.alpha as alpha
from unitary.examples.quantum_chinese_chess.enums import (
    SquareState,
    Color,
    Type,
    Language,
)
from unitary.examples.quantum_chinese_chess.piece import Piece


# The default initial state of the game.
_INITIAL_FEN = "RHEAKAEHR/9/1C5C1/P1P1P1P1P/9/9/p1p1p1p1p/1c5c1/9/rheakaehr w---1"


class Board:
    """Board holds the assemble of all pieces. Each piece could be either in classical or quantum state."""

    def __init__(
        self, board: alpha.QuantumWorld, current_player: int, king_locations: List[str]
    ):
        self.board = board
        self.current_player = current_player
        self.king_locations = king_locations
        self.lang = Language.EN  # The default language is English.

    def set_language(self, lang: Language):
        self.lang = lang

    @classmethod
    def from_fen(cls, fen: str = _INITIAL_FEN) -> "Board":
        """
        Translates FEN (Forsyth-Edwards Notation) symbols into the whole QuantumWorld board.
        FEN rule for Chinese Chess could be found at https://www.wxf-xiangqi.org/images/computer-xiangqi/fen-for-xiangqi-chinese-chess.pdf
        """
        chess_board = {}
        row_index = 9
        king_locations = []
        pieces, turns = fen.split(" ", 1)
        for row in pieces.split("/"):
            col = ord("a")
            for char in row:
                # Add empty board pieces.
                if "1" <= char <= "9":
                    for i in range(int(char)):
                        name = f"{chr(col)}{row_index}"
                        chess_board[name] = Piece(
                            name, SquareState.EMPTY, Type.EMPTY, Color.NA
                        )
                        col += 1
                # Add occupied board pieces.
                else:
                    name = f"{chr(col)}{row_index}"
                    piece_type = Type.type_of(char)
                    if piece_type == Type.KING:
                        king_locations.append(name)
                    color = Color.RED if char.isupper() else Color.BLACK
                    chess_board[name] = Piece(
                        name, SquareState.OCCUPIED, piece_type, color
                    )
                    col += 1
            row_index -= 1
        board = alpha.QuantumWorld(chess_board.values())
        # Here 0 means the player RED while 1 the player BLACK.
        current_player = 0 if "w" in turns else 1
        return cls(board, current_player, king_locations)

    def __str__(self):
        num_rows = 10
        board_string = ["\n "]
        # Print the top line of col letters.
        for col in "abcdefghi":
            board_string.append(f" {col}")
        board_string.append("\n")
        for row in range(num_rows):
            # Print the row index on the left.
            board_string.append(f"{row} ")
            for col in "abcdefghi":
                piece = self.board[f"{col}{row}"]
                board_string += piece.symbol(self.lang)
                if self.lang == Language.EN:
                    board_string.append(" ")
            # Print the row index on the right.
            board_string.append(f" {row}\n")
        board_string.append(" ")
        # Print the bottom line of col letters.
        for col in "abcdefghi":
            board_string.append(f" {col}")
        board_string.append("\n")
        if self.lang == Language.EN:
            return "".join(board_string)
        # We need to turn letters into their full-width counterparts to align
        # a mix of letters + Chinese characters.
        chars = "".join(chr(c) for c in range(ord(" "), ord("z")))
        full_width_chars = "\N{IDEOGRAPHIC SPACE}" + "".join(
            chr(c)
            for c in range(
                ord("\N{FULLWIDTH EXCLAMATION MARK}"),
                ord("\N{FULLWIDTH LATIN SMALL LETTER Z}"),
            )
        )
        translation = str.maketrans(chars, full_width_chars)
        return (
            "".join(board_string)
            .replace(" ", "")
            .replace("abcdefghi", " abcdefghi")
            .translate(translation)
        )