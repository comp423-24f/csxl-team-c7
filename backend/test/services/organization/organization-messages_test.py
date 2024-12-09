"""Tests for the OrganizationMessageService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from backend.entities.organization_messages_entity import (
    OrganizationMessageEntity,
)
from backend.services.exceptions import (
    UserPermissionException,
    ResourceNotFoundException,
)

# Tested Dependencies
from ....models import organization_message
from backend.services.organization_message_service import OrganizationMessageService

# Injected Service Fixtures
from ..fixtures import organization_message_svc_integration

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
from ..user_data import user, application


def test_get_organization_messages(
    organization_message_svc_integration: OrganizationMessageService,
):
    # Fetch the organization's messages using `user` instead of `root`
    messages = organization_message_svc_integration.get_organization_messages(
        user, cads.slug
    )
    assert messages is not None


def test_get_organization_messages_does_not_exist(
    organization_message_svc_integration: OrganizationMessageService,
):
    # Test for non-existent organization message
    with pytest.raises(ResourceNotFoundException) as excinfo:
        organization_message_svc_integration.get_organization_messages(
            user, "nonexistent_slug"  # Use `user` and a slug that doesn't exist
        )
    assert str(excinfo.value) == "Organization nonexistent_slug not found"


def test_get_user_messages(
    organization_message_svc_integration: OrganizationMessageService,
):
    # Fetch user messages
    user_messages = organization_message_svc_integration.get_user_messages(
        user.id
    )  # Use `user` instead of `root`
    assert user_messages is not None


def test_get_user_messages_does_not_exist(
    organization_message_svc_integration: OrganizationMessageService,
):
    # Test for non-existent user messages
    with pytest.raises(ResourceNotFoundException) as excinfo:
        organization_message_svc_integration.get_user_messages(
            -1  # Use -1 for a non-existent user
        )
    assert str(excinfo.value) == "User -1 not found"


def test_create_organization_message(
    organization_message_svc_integration: OrganizationMessageService,
):
    # Create an organization message
    new_message = organization_message_svc_integration.create(
        user, cads.slug, to_add  # Use `user` and a valid `slug` for the message
    )
    assert new_message.id is not None


def test_create_organization_message_does_not_exist(
    organization_message_svc_integration: OrganizationMessageService,
):
    # Test for creating message in a non-existent organization
    with pytest.raises(ResourceNotFoundException) as excinfo:
        organization_message_svc_integration.create(
            user, "nonexistent_slug", to_add  # Use `user` and a slug that doesn't exist
        )
    assert str(excinfo.value) == "Organization nonexistent_slug not found"


def test_delete_message(
    organization_message_svc_integration: OrganizationMessageService,
):
    # First create a message
    new_message = organization_message_svc_integration.create(user, cads.slug, to_add)

    # Now delete the created message
    message = organization_message_svc_integration.delete(
        user, new_message.id
    )  # Use `user` instead of `root`
    assert (
        message == "Message deleted successfully"
    )  # Assuming a successful delete message


def test_delete_message_does_not_exist(
    organization_message_svc_integration: OrganizationMessageService,
):
    # Test for trying to delete a non-existent message
    with pytest.raises(ResourceNotFoundException) as excinfo:
        organization_message_svc_integration.delete(
            user, -1  # Use -1 for a non-existent message ID
        )
    assert str(excinfo.value) == "Message not found"
