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
"""Module to combine all the zones of the RPG world into one list."""

import unitary.examples.quantum_rpg.final_state_preparation.classical_frontier as classical_frontier
import unitary.examples.quantum_rpg.final_state_preparation.oxtail_university as oxtail_university
import unitary.examples.quantum_rpg.final_state_preparation.hadamard_hills as hadamard_hills
import unitary.examples.quantum_rpg.final_state_preparation.quantum_perimeter as quantum_perimeter


WORLD = [
    *classical_frontier.CLASSICAL_FRONTIER,
    *oxtail_university.OXTAIL_UNIVERSITY,
    *hadamard_hills.HADAMARD_HILLS,
    *quantum_perimeter.QUANTUM_PERIMETER,
]
