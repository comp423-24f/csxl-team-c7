"""Definition of detailed model for organization applications, including related data."""

from datetime import datetime
from pydantic import BaseModel
from .organization_application_state import ApplicationState
from .organization import Organization
from .user import User

__authors__ = ["Tejas Chandra"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OrganizationApplicationDetails(BaseModel):
    """
    Detailed model for organization applications.
    Includes all base fields plus related organization and user data.
    """

    id: int
    answers: str
    state: ApplicationState
    created_at: datetime
    reviewed_at: datetime | None
    reviewer_notes: str
    organization_id: int
    applicant_id: int
    reviewer_id: int | None

    # Related models
    organization: Organization
    applicant: User
    reviewer: User | None
