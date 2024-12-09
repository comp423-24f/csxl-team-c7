"""Tests for the OrganizationService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.entities.organization_application_entity import (
    OrganizationApplicationEntity,
)
from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)

# Tested Dependencies
from ....models import OrganizationApplication
from ....services import OrganizationApplicationService

# Injected Service Fixtures
from ..fixtures import organization_application_svc_integration

# Explicitly import Data Fixture to load entities in database
from ..core_data import setup_insert_data_fixture

# Data Models for Fake Data Inserted in Setup
from .organization_test_data import (
    organizations,
    to_add,
    cads,
    new_cads,
    to_add_conflicting_id,
)
from ..user_data import root, user, application


def test_get_organization_applications(
    organization_application_svc_integration: OrganizationApplicationService,
):
    org = organization_application_svc_integration.get_organization_applications(
        root, cads.slug
    )
    assert org is not None


def test_get_organization_applications_does_not_exist(
    organization_application_svc_integration: OrganizationApplicationService,
):
    with pytest.raises(ResourceNotFoundException) as excinfo:
        organization_application_svc_integration.get_organization_applications(
            root, "nonexistent_slug"
        )
    assert str(excinfo.value) == "Organization nonexistent_slug not found"


def test_get_user_applications(
    organization_application_svc_integration: OrganizationApplicationService,
):
    user = organization_application_svc_integration.get_user_applications(root.id)
    assert user is not None


def test_get_user_applications_does_not_exist(
    organization_application_svc_integration: OrganizationApplicationService,
):
    with pytest.raises(ResourceNotFoundException) as excinfo:
        organization_application_svc_integration.get_user_applications(-1)
    assert str(excinfo.value) == "User -1 not found"


def test_create_organization_application(
    organization_application_svc_integration: OrganizationApplicationService,
):
    new_application = organization_application_svc_integration.create(
        root, cads.slug, application
    )
    assert new_application.id is not None


def test_create_organization_application_does_not_exist(
    organization_application_svc_integration: OrganizationApplicationService,
):
    with pytest.raises(ResourceNotFoundException) as excinfo:
        organization_application_svc_integration.create(
            root, "nonexistent_slug", application
        )
    assert str(excinfo.value) == "Organization nonexistent_slug not found"


def test_delete(
    organization_application_svc_integration: OrganizationApplicationService,
):
    organization_application_svc_integration.create(root, cads.slug, application)
    org = organization_application_svc_integration.delete(root, application.id)
    assert org.applications == []


def test_delete_does_not_exist(
    organization_application_svc_integration: OrganizationApplicationService,
):
    with pytest.raises(ResourceNotFoundException) as excinfo:
        organization_application_svc_integration.delete(
            root, -1
        )  # Assuming -1 does not exist
    assert str(excinfo.value) == "Application not found"
