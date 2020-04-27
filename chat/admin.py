from django.contrib import admin
from django.conf import settings

from chat import models
from chat.settings import CHAT_SETTINGS


User = settings.AUTH_USER_MODEL


class InlineParticipantChat(admin.TabularInline):
    model = models.ParticipantChat
    raw_id_fields = ('user', )


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = list_display_links = (
        'id',
        'title',
        'is_group',
        'created_at',
        'count_participants',
        'last_message_date',
        'last_message_text',
    )

    fields = (
        'title',
        'is_group',
        'created_at',
        'last_message_date',
        'last_message_text',
    )

    readonly_fields = ('created_at', 'last_message_date', 'last_message_text')
    search_fields = CHAT_SETTINGS['SEARCH_FIELDS_CHATADMIN']
    list_filter = ('is_group', )
    inlines = (InlineParticipantChat, )
    raw_id_fields = ('participants', )


class InlineMessageStatus(admin.TabularInline):
    model = models.MessageStatus
    raw_id_fields = ('user', )


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = list_display_links = (
        'id',
        'user',
        'text',
        'type_chat',
        'created_at',
    )

    fields = (
        'user',
        'text',
        'chat',
        'type_chat',
    )

    inlines = (InlineMessageStatus, )
    readonly_fields = ('type_chat', )
    raw_id_fields = ('user', )
    list_filter = ('chat__is_group', )


