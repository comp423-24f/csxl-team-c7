"""Definition of application states for organization applications."""

from enum import Enum, auto

__authors__ = ["Tejas Chandra"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class ApplicationState(Enum):
    """Enum representing the possible states of an organization application."""

    # Initial state when application is first submitted
    PENDING = "PENDING"

    # Application has been approved by organization leader
    APPROVED = "APPROVED"

    # Application has been rejected by organization leader
    REJECTED = "REJECTED"

    # Application has been withdrawn by the applicant
    WITHDRAWN = "WITHDRAWN"

    # Application requires additional information from applicant
    NEEDS_INFO = "NEEDS_INFO"

    def __str__(self) -> str:
        """Returns the string representation of the application state."""
        return self.value

    @staticmethod
    def from_string(state_str: str) -> "ApplicationState":
        """
        Converts a string to an ApplicationState enum value.

        Parameters:
            state_str (str): String representation of the state

        Returns:
            ApplicationState: Corresponding enum value

        Raises:
            ValueError: If the string doesn't match any state
        """
        try:
            return ApplicationState(state_str.upper())
        except ValueError:
            raise ValueError(
                f"'{state_str}' is not a valid application state. "
                f"Valid states are: {', '.join([state.value for state in ApplicationState])}"
            )
