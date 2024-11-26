"""Organization Application API routes."""

from fastapi import APIRouter, Depends
from typing import List

from ..services.organization_application import OrganizationApplicationService
from ..models.organization_application import OrganizationApplication, ApplicationStatus
from ..models.organization_details import OrganizationDetails
from ..models.user_details import UserDetails
from ..api.authentication import registered_user
from ..models.user import User

api = APIRouter(prefix="/api/organizations")


@api.post(
    "/{slug}/apply",
    response_model=OrganizationDetails,
    tags=["Organization Applications"],
)
def create_application(
    slug: str,
    application: OrganizationApplication,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationDetails:
    """Submit new application"""
    return application_service.create(subject, slug, application)


@api.get(
    "/{slug}/applications",
    response_model=OrganizationDetails,
    tags=["Organization Applications"],
)
def get_organization_applications(
    slug: str,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationDetails:
    """Get all applications for an organization (admin only)"""
    return application_service.get_organization_applications(subject, slug)


@api.get(
    "/applications/user", response_model=UserDetails, tags=["Organization Applications"]
)
def get_user_applications(
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> UserDetails:
    """Get current user's applications"""
    return application_service.get_user_applications(subject.id)


@api.put(
    "/applications/{application_id}",
    response_model=OrganizationDetails,
    tags=["Organization Applications"],
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
    tags=["Organization Applications"],
)
def delete_application(
    application_id: int,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationDetails:
    """Delete application"""
    return application_service.delete(subject, application_id)
