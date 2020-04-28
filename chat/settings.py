from django.conf import settings

CHAT_SETTINGS = getattr(settings, 'CHAT_SETTINGS', {})

# admin
SEARCH_FIELDS_CHATADMIN = CHAT_SETTINGS.get(
    'SEARCH_FIELDS_CHATADMIN', ('title',),
)

# functions
READ_ALL_MESSAGES_RETRIEVE_CHAT = CHAT_SETTINGS.get(
    'READ_ALL_MESSAGES_RETRIEVE_CHAT', False,
)
