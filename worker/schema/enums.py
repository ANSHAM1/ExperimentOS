from enum import Enum


class Step(Enum):
    GENERATION = "generation"
    EVALUATION = "evaluation"
    RETRY      = "retry"