from pydantic import BaseModel
from enum import Enum


class ApplicationStatus(str, Enum):
    """Represents the Application Status Enums"""

    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class OrganizationApplication(BaseModel):
    """Represents the model to create Organization Applications"""

    id: int | None = None
    user_id: int
    organization_id: int
    status: ApplicationStatus = ApplicationStatus.PENDING
    interest_statement: str
    experience: str
    expected_graduation: str
    program_pursued: str
    additional_info: str
    admin_response: str | None = None
