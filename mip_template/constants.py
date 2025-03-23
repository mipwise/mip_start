from enum import StrEnum


APP_OUTPUT_DIR = '/app/output'


class SolverTypes(StrEnum):
    GUROBI = 'Gurobi'
    SCIP = 'SCIP'


class Portions(StrEnum):
    WHOLE = 'Ensure whole portions'
    FRACTIONAL = 'Portions can be fractional'
