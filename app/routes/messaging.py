import json
import re
from datetime import datetime
import pytz
from app.helpers.api_helper import respond
from app.routes.util.routes import create_twilio_client
from app.routes.auth.decorators import roles_required
from . import admin


def get_latest_read_time(read_receipts, email):
    # Input format: '2020-11-24T17:12:53.107456+00:00'
    # TODO find better way to convert to datetime?
    latest_read_time = re.sub(r"\.[0-9+:]*", "", read_receipts[email])
    return pytz.UTC.localize(datetime.strptime(latest_read_time, "%Y-%m-%dT%H:%M:%S"))


def is_read(conversation, email):
    messages = conversation.messages.list()
    if not messages:
        return True

    read_receipts = json.loads(conversation.attributes).get("read_receipts")
    if email not in read_receipts:
        return False

    latest_read_time = get_latest_read_time(read_receipts, email)
    latest_message_time = messages[-1].date_created

    return latest_read_time >= latest_message_time


# history example:
# [
#     {
#         "status": "Resolved",
#         "changed_by": "System",
#         "changed_on": "2022-01-26T08:47:44.044837+00:00",
#     },
#     {
#         "status": "In Progress",
#         "changed_by": "linh@zippitycars.com",
#         "changed_on": "2022-01-26T08:48:27.317981+00:00",
#     },
# ]
def get_status(conversation):
    history = json.loads(conversation.attributes).get("ticket_history")
    return history[-1]["status"] if len(history) >= 1 else None


def is_participant(conversation, email):
    participants_list = conversation.participants.list()
    participant_emails = [participant.identity for participant in participants_list]
    return email in participant_emails


# A conversation should count as unread if BOTH of these are true:
# 1. The user is a participant in the conversation
# 2. The latest message in the conversation is unread
def should_show_unread(conversation, email):
    if not is_participant(conversation, email):
        return False
    if is_read(conversation, email):
        return False
    return True


@admin.route("/get-unread-message-boolean", methods=["GET"])
@roles_required(["admin"])
def has_unread_conversation(user_):
    email = user_.username
    client = create_twilio_client()
    conversation_list = client.conversations.conversations.list()
    for c in conversation_list or []:
        if should_show_unread(c, email):
            return respond(200, {"has_unread_message": True})
    return respond(200, {"has_unread_message": False})
