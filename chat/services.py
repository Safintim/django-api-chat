from rest_framework import exceptions

from chat.models import Chat, MessageStatus, ParticipantChat


def get_dialog_between_users(user1_id, user2_id):
    qs = ParticipantChat.objects.filter(chat__is_group=False)

    chats_user1 = qs.filter(user__id=user1_id).values_list('chat_id', flat=True)
    chats_user2 = qs.filter(user__id=user2_id).values_list('chat_id', flat=True)

    dialog_ids = set(chats_user1) & set(chats_user2)

    if len(dialog_ids) > 1:
        raise exceptions.ValidationError(
            detail='There is more than one chat between users',
        )
    if not dialog_ids:
        return None

    dialog_id = dialog_ids.pop()
    return Chat.objects.filter(id=dialog_id).first()


def create_message_statuses(message):
    participants = message.chat.participants.exclude(id=message.user.id)
    messages_statuses = [MessageStatus(message=message, user=user)
                         for user in participants]
    return MessageStatus.objects.bulk_create(messages_statuses)


def read_messages(user, chat):
    return MessageStatus.objects.filter(
        user=user, message__chat=chat,
    ).update(is_read=True)
