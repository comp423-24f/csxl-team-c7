"""Organization Applications API

APIs for handling organization membership applications."""

from fastapi import APIRouter, Depends
from ..api.authentication import registered_user
from ..services.organizations_applications import OrganizationApplicationService
from ..models.user import User
from ..models.organization_application import (
    OrganizationApplication,
    NewOrganizationApplication,
)
from ..models.organization_application_details import OrganizationApplicationDetails

__authors__ = ["Tejas Chandra"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/organizations/applications")
openapi_tags = {
    "name": "Organization Applications",
    "description": "Create, review, and manage organization membership applications.",
}


@api.post(
    "/{organization_id}",
    response_model=OrganizationApplication,
    tags=["Organization Applications"],
)
def create_application(
    organization_id: int,
    application: NewOrganizationApplication,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationApplication:
    """
    Create a new application for an organization.

    Parameters:
        organization_id: ID of the organization being applied to
        application: Application content and details
        subject: Currently logged in user
        application_service: Organization application service

    Returns:
        OrganizationApplication: Created application
    """
    return application_service.create(subject, organization_id, application)


@api.get(
    "/{application_id}",
    response_model=OrganizationApplicationDetails,
    tags=["Organization Applications"],
)
def get_application(
    application_id: int,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationApplicationDetails:
    """
    Get details of a specific application.

    Parameters:
        application_id: ID of the application to retrieve
        subject: Currently logged in user
        application_service: Organization application service

    Returns:
        OrganizationApplicationDetails: Application details including related data
    """
    return application_service.get(subject, application_id)


@api.put(
    "/{application_id}/review",
    response_model=OrganizationApplication,
    tags=["Organization Applications"],
)
def review_application(
    application_id: int,
    application: OrganizationApplication,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> OrganizationApplication:
    """
    Review an application (approve/reject/request more info).

    Parameters:
        application_id: ID of the application to review
        application: Updated application data
        subject: Currently logged in user
        application_service: Organization application service

    Returns:
        OrganizationApplication: Updated application
    """
    return application_service.review(subject, application_id, application)


@api.get(
    "/organization/{organization_id}",
    response_model=list[OrganizationApplicationDetails],
    tags=["Organization Applications"],
)
def list_organization_applications(
    organization_id: int,
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> list[OrganizationApplicationDetails]:
    """
    List all applications for an organization.

    Parameters:
        organization_id: ID of the organization
        subject: Currently logged in user
        application_service: Organization application service

    Returns:
        list[OrganizationApplicationDetails]: List of applications with details
    """
    return application_service.list_by_organization(subject, organization_id)


@api.get(
    "/user/applications",
    response_model=list[OrganizationApplicationDetails],
    tags=["Organization Applications"],
)
def list_user_applications(
    subject: User = Depends(registered_user),
    application_service: OrganizationApplicationService = Depends(),
) -> list[OrganizationApplicationDetails]:
    """
    List all applications submitted by the current user.

    Parameters:
        subject: Currently logged in user
        application_service: Organization application service

    Returns:
        list[OrganizationApplicationDetails]: List of user's applications with details
    """
    return application_service.list_by_user(subject)
