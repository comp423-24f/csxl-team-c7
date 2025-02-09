"""User operations open to registered users such as searching for fellow user profiles."""

from fastapi import APIRouter, Depends

from backend.models.organization import Organization
from backend.models.user_details import UserDetails
from ..services import UserService
from ..models import User
from .authentication import registered_user

api = APIRouter(prefix="/api/user")
openapi_tags = {
    "name": "Users",
    "description": "User profile search and related operations.",
}


@api.get("", response_model=list[User], tags=["Users"])
def search(
    q: str, subject: User = Depends(registered_user), user_svc: UserService = Depends()
):
    """Search for users based on a query string which matches against name, onyen, and email address."""
    return user_svc.search(subject, q)


@api.get("/organizations", response_model=list[Organization], tags=["Users"])
def get_user_organizations(
    subject: User = Depends(registered_user), user_svc: UserService = Depends()
):
    """Get organizations the current user is a member of"""
    return user_svc.get_user_organizations(subject.id)


@api.get("/{onyen}", tags=["Users"])
def get_by_onyen(
    onyen: str,
    subject: User = Depends(registered_user),
    user_svc: UserService = Depends(),
):
    """Search for one user by their onyen"""
    return user_svc.get_by_onyen(subject, onyen)


@api.get("/applications", response_model=UserDetails, tags=["Users"])
def get_user_applications(
    subject: User = Depends(registered_user), user_svc: UserService = Depends()
):
    """Get all applications submitted by the current user"""
    return user_svc.get_user_details(subject.id)


# @api.get("/{id}/roles", tags=["Users"])
# def get_user_role(
#    subject: User = Depends(registered_user), user_svc: UserService = Depends()
# ):
#    return user_svc.get_user_role(subject.id)
