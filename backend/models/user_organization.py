from pydantic import BaseModel


class UserOrganization(BaseModel):
    user_id: int
    organization_id: int
    role: str  # Role is optional in case it's not always provided.
