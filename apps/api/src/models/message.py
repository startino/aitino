from datetime import UTC, datetime
from uuid import UUID, uuid4
from autogen import ConversableAgent

from pydantic import BaseModel, Field

from .composition import Composition

from .session import Session


class AutogenMessage(BaseModel):
    name: str
    recipient: str
    content: str
    role: str = "user"


class Message(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    session_id: UUID
    sender_id: UUID
    recipient_id: UUID
    content: str
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))


def message_from_autogen(
    composition: Composition,
    session: Session,
    recipient: ConversableAgent,
    message: dict,
) -> Message:

    # get recipient_id and sender_id
    recipient_id = uuid4()
    sender_id = uuid4()

    for agent in composition.agents:
        if agent.name == recipient.name:
            recipient_id = agent.id
        if agent.name == message["name"]:
            sender_id = agent.id

    return Message(
        session_id=session.id,
        recipient_id=recipient_id,
        sender_id=sender_id,
        content=message["content"],
        role=message["role"],
    )


def autogen_message_from_message(
    composition: Composition, message: Message
) -> AutogenMessage:

    return AutogenMessage(
        name=message.sender_id,
        recipient=message.recipient_id,
        content=message.content,
        role=message.role,
    )
