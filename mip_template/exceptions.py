class InputDataError(Exception):
    """
    Raised whenever the input data is not valid.
    """


class SolutionError(Exception):
    """
    Raised when the output from the optimization or the output tables contain some problem.
    
    For example, if the solution is not feasible, or if the output from the optimization violates an expected
    constraint.
    """
