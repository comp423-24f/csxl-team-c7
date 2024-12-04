"""Organization API

Organization routes are used to create, retrieve, and update Organizations."""

from fastapi import APIRouter, Depends

from backend.models.organization_application import (
    ApplicationStatus,
    OrganizationApplication,
)
from backend.models.organization_message import OrganizationMessage
from backend.models.user_details import UserDetails
from backend.services.organization_application import (
    OrganizationApplication,
    OrganizationApplicationService,
)
from backend.services.organization_messages import OrganizationMessageService

from ..services import OrganizationService, RoleService
from ..models.organization import Organization
from ..models.organization_details import OrganizationDetails
from ..api.authentication import registered_user
from ..models.user import User

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter(prefix="/api/organizations")
openapi_tags = {
    "name": "Organizations",
    "description": "Create, update, delete, and retrieve CS Organizations.",
}


@api.get("", response_model=list[Organization], tags=["Organizations"])
def get_organizations(
    organization_service: OrganizationService = Depends(),
) -> list[Organization]:
    """
    Get all organizations

    Parameters:
        organization_service: a valid OrganizationService

    Returns:
        list[Organization]: All `Organization`s in the `Organization` database table
    """

    # Return all organizations
    return organization_service.all()


@api.post("", response_model=Organization, tags=["Organizations"])
def new_organization(
    organization: Organization,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
    role_service: RoleService = Depends(),
) -> Organization:
    """
    Create organization

    Parameters:
        organization: a valid Organization model
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Returns:
        Organization: Created organization

    Raises:
        HTTPException 422 if create() raises an Exception
    """

    new_organization = organization_service.create(subject, organization)
    # Create a new role for the organization newly created
    role_service.create(subject, new_organization.slug)
    return new_organization


@api.get(
    "/{slug}",
    responses={404: {"model": None}},
    response_model=OrganizationDetails,
    tags=["Organizations"],
)
def get_organization_by_slug(
    slug: str, organization_service: OrganizationService = Depends()
) -> OrganizationDetails:
    """
    Get organization with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        organization_service: a valid OrganizationService

    Returns:
        Organization: Organization with matching slug

    Raises:
        HTTPException 404 if get_by_slug() raises an Exception
    """

    return organization_service.get_by_slug(slug)


@api.put(
    "",
    responses={404: {"model": None}},
    response_model=Organization,
    tags=["Organizations"],
)
def update_organization(
    organization: Organization,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
) -> Organization:
    """
    Update organization

    Parameters:
        organization: a valid Organization model
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Returns:
        Organization: Updated organization

    Raises:
        HTTPException 404 if update() raises an Exception
    """

    return organization_service.update(subject, organization)


@api.delete("/{slug}", response_model=None, tags=["Organizations"])
def delete_organization(
    slug: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
):
    """
    Delete organization based on slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Raises:
        HTTPException 404 if delete() raises an Exception
    """

    organization_service.delete(subject, slug)


@api.post("/{slug}/join", response_model=Organization, tags=["Organizations"])
def join_organization(
    slug: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
) -> Organization:
    """Join an organization"""
    return organization_service.add_member(subject, slug)


@api.post("/{slug}/leave", response_model=None, tags=["Organizations"])
def leave_organization(
    slug: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
):
    """Leave an organization"""
    organization_service.remove_member(subject, slug)


@api.get("/{slug}/membership", response_model=bool, tags=["Organizations"])
def check_membership(
    slug: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
) -> bool:
    """Check if user is member of organization"""
    return organization_service.is_member(subject.id, slug)


@api.post("/{slug}/apply", response_model=OrganizationDetails, tags=["Organizations"])
def create_application(
    slug: str,
    application: OrganizationApplication,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationDetails:
    """Submit new application"""
    return application_service.create(subject, slug, application)


@api.get(
    "/{slug}/applications", response_model=OrganizationDetails, tags=["Organizations"]
)
def get_organization_applications(
    slug: str,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationDetails:
    """Get all applications for an organization (admin only)"""
    return application_service.get_organization_applications(subject, slug)


@api.get("/applications/user", response_model=UserDetails, tags=["Organizations"])
def get_user_applications(
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> UserDetails:
    """Get current user's applications"""
    return application_service.get_user_applications(subject.id)


@api.put(
    "/applications/{application_id}",
    response_model=OrganizationDetails,
    tags=["Organizations"],
)
def update_application_status(
    application_id: int,
    status: ApplicationStatus,
    admin_response: str | None = None,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationDetails:
    """Update application status (admin only)"""
    return application_service.update_status(
        subject, application_id, status, admin_response
    )


@api.delete(
    "/applications/{application_id}",
    response_model=OrganizationDetails,
    tags=["Organizations"],
)
def delete_application(
    application_id: int,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationDetails:
    """Delete application"""
    return application_service.delete(subject, application_id)


@api.post(
    "/{slug}/messages", response_model=OrganizationMessage, tags=["Organizations"]
)
def create_message(
    slug: str,
    content: str,
    subject: User = Depends(registered_user),
    message_service: OrganizationMessageService = Depends(),
) -> OrganizationMessage:
    """Create new organization message (admin only)"""
    return message_service.create_message(subject, slug, content)


@api.put(
    "/messages/{message_id}", response_model=OrganizationMessage, tags=["Organizations"]
)
def update_message(
    message_id: int,
    content: str,
    subject: User = Depends(registered_user),
    message_service: OrganizationMessageService = Depends(),
) -> OrganizationMessage:
    """Update organization message (admin only)"""
    return message_service.update_message(subject, message_id, content)


@api.delete("/messages/{message_id}", response_model=None, tags=["Organizations"])
def delete_message(
    message_id: int,
    subject: User = Depends(registered_user),
    message_service: OrganizationMessageService = Depends(),
):
    """Delete organization message (admin only)"""
    message_service.delete_message(subject, message_id)
