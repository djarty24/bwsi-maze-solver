from typing import Literal
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Operator

Direction = Literal["N", "E", "S", "W"]

"""
returns an operator that makes the ket corresponding to the direction on a given |00> state
"""
def make_direction_ket(direction: Direction) -> Operator:
  op = QuantumCircuit(2)

  if direction in ["E", "W"]: op.x(1)
  if direction in ["S", "W"]: op.x(0)

  Operator(op)

  return op

"""
without safety checks applies direction and returns new position
i is x (col), j is y (row)
"""
def apply_direction(direction: Direction, i: int, j: int) -> int[2]:
  match direction:
    case "N":
      j -= 1
    case "E":
      i += 1
    case "S":
      j += 1
    case "W":
      i -= 1

  return (i, j)

