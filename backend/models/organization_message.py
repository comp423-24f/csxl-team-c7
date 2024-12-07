from pydantic import BaseModel
from datetime import datetime


class OrganizationMessage(BaseModel):
    """
    Pydantic model to represent an `OrganizationMessage`, including back-populated
    relationship fields.

    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `Organization` database in the PostgreSQL database.
    """

    id: int | None = None
    organization_id: int
    user_id: int
    content: str
    created_at: datetime | None = None
