"""Definition of models for organization applications."""

from datetime import datetime
from pydantic import BaseModel
from organization_application_state import ApplicationState

__authors__ = ["Tejas Chandra"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class NewOrganizationApplication(BaseModel):
    """
    Model representing a new organization application being submitted.
    Contains only the fields that can be set when creating a new application.
    """

    answers: str
    organization_id: int
    applicant_id: int


class OrganizationApplication(BaseModel):
    """Model representing an organization application."""

    id: int
    answers: str
    state: ApplicationState
    created_at: datetime
    reviewed_at: datetime | None
    reviewer_notes: str
    organization_id: int
    applicant_id: int
    reviewer_id: int | None
