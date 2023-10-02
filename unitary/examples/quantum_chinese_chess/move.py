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
from typing import Optional
from unitary.alpha.quantum_effect import QuantumEffect
from enums import (
    MoveType,
    MoveVariant
)


class Move(QuantumEffect):
    def __init__(
        self,
        source: str,
        target: str,
        source2: Optional[str] = None,
        target2: Optional[str] = None,
        move_type: Optional[MoveType] = None,
        move_variant: Optional[MoveVariant] = None,
        measurement: Optional[int] = None,
    ):
        self.source = source
        self.source2 = source2
        self.target = target
        self.target2 = target2
        self.move_type = move_type
        self.move_variant = move_variant
        self.measurement = measurement


    def __eq__(self, other):
        if isinstance(other, Move):
            return (
                self.source == other.source
                and self.source2 == other.source2
                and self.target == other.target
                and self.target2 == other.target2
                and self.move_type == other.move_type
                and self.move_variant == other.move_variant
                and self.measurement == other.measurement
            )
        return False

    def effect(self, *objects):
        return

    @classmethod
    def from_string(cls, str_to_parse: str):
        """Creates a move from a string shorthand for tests.
        Format=sources_and_targets[.measurement]:type:variant                              
        where sources_and_targets could be:
            a pair of 2-character square strings concatenated together   
            s1^t1t2 for split moves with 2 targets                                         
            s1s2^t1 for merge moves with 2 sources
        Examples:                    
           'a1a2:JUMP:BASIC'                                                               
           'b1^a3c3:SPLIT_JUMP:BASIC'                                                      
           'b1^a3c3.m0:SPLIT_JUMP:BASIC'
           'b1^a3c3.m1:SPLIT_JUMP:BASIC'
           'a3b1^c3:MERGE_JUMP:BASIC'
        """
        sources = None
        targets = None

        if "^" in str_to_parse:
            sources_str, targets_str = str_to_parse.split("^", maxsplit=1)
            # The only two allowed cases here are s1^t1t2 and s1s2^t1.
            if str_to_parse.count("^") > 1 or len(str_to_parse) != 7 or len(sources_str) not in [2, 4]:
                raise ValueError(f"Invalid sources/targets string {str_to_parse}")
            sources = [sources_str[i : i + 2] for i in range(0, len(sources_str), 2)]
            targets = [targets_str[i : i + 2] for i in range(0, len(targets_str), 2)]
        else:
            # The only allowed case here is s1t1.
            if len(str_to_parse) != 4:
                raise ValueError(f"Invalid sources/targets string {str_to_parse}")
            sources = [str_to_parse[0:2]]
            targets = [str_to_parse[2:4]]

        # Make sure all the locations are valid.
        for location in sources + targets:
            if location[0].lower() not in "abcdefghi" or not location[1].isdigit():
                raise ValueError(f"Invalid location string. Make sure they are from a0 to i9.")

        # TODO(): more detailed analysis to determine move type and variant.
        move_type = MoveType.UNSPECIFIED_STANDARD
        move_variant = MoveVariant.UNSPECIFIED
        if len(sources) == 1 and len(targets) == 1:
            return cls(
                sources[0],
                targets[0],
                move_type=move_type,
                move_variant=move_variant,
            )
        if len(sources) == 1 and len(targets) == 2:
            return cls(
                sources[0],
                targets[0],
                target2=targets[1],
                move_type=move_type,
                move_variant=move_variant,
            )
        if len(sources) == 2 and len(targets) == 1:
            return cls(
                sources[0],
                targets[0],
                source2=sources[1],
                move_type=move_type,
                move_variant=move_variant,
            )
        raise ValueError(
            f"Wrong number of sources {sources} or targets {targets} for {str_to_parse}"
        )

    def is_split_move(self) -> bool:
        return self.target2 is not None

    def is_merge_move(self) -> bool:
        return self.source2 is not None

    def has_measurement(self) -> bool:
        return self.measurement is not None

    def to_string(self, include_type=False) -> str:
        """
        Constructs the string representation of this move object.
        By default, only returns the move source(s), target(s), and measurement
        if present.
        Args:
            include_type: also include the move type/variant in the string
        """
        movestr = self.source + self.target
        if self.is_split_move():
            movestr = self.source + "^" + self.target + str(self.target2)
        elif self.is_merge_move():
            movestr = self.source + str(self.source2) + "^" + self.target
        if self.has_measurement():
            movestr += ".m" + str(self.measurement)

        if include_type and self.move_type is not None:
            movestr += ":" + self.move_type.name
        if include_type and self.move_variant is not None:
            movestr += ":" + self.move_variant.name

        return movestr

    def __str__(self):
        return self.to_string()
