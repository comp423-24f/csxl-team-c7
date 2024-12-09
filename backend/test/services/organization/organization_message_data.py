"""Test data for OrganizationMessageService."""

from ....models import OrganizationMessage

messages = [
    OrganizationMessage(
        id=1,
        organization_id=1,
        user_id=1,
        title="Welcome to the Organization!",
        body="Congratulations on making the cut!",
        created_at="2024-12-01",
    ),
    OrganizationMessage(
        id=2,
        organization_id=1,
        user_id=1,
        title="Upcoming Event",
        body="We have coffee chats coming up this weekend!",
        created_at="2024-12-05",
    ),
]

new_message = OrganizationMessage(
    id=3,
    organization_id=1,
    user_id=1,
    title="Meeting Reminder",
    body="Team Meeting tomorrow in Sitterson.",
    created_at="2024-12-07",
)
