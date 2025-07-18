# enum class
from enum import Enum


class LoanStatus(Enum):
    """
    Enum representing the status of a loan.
    """

    MAINTENANCE = "m"
    ON_LOAN = "o"
    AVAILABLE = "a"
    RESERVED = "r"


# Maximum lengths for CharFields
MAX_LENGTH_TITLE = 200
MAX_LENGTH_NAME = 100
MAX_LENGTH_SUMMARY = 100
MAX_LENGTH_ISBN = 13
MAX_LENGTH_IMPRINT = 200
DISPLAY_GENRE_LIMIT = 3
DEFAULT_PAGINATION = 10
PAGINATE_BY = 10
NUM_OF_WEEKS = 4
NUM_OF_WEEKS_DEFAULT = 3
INITIAL_DATE_OF_DEATH = "11/06/2020"
