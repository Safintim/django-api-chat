from django.conf import settings

CHAT_SETTINGS = getattr(settings, 'CHAT_SETTINGS', {})

# admin
CHAT_SETTINGS.setdefault('SEARCH_FIELDS_CHATADMIN', ('title',))
CHAT_SETTINGS.setdefault('USER_SERIALIZER', None)

# functions
CHAT_SETTINGS.setdefault('READ_ALL_MESSAGES_RETRIEVE_CHAT', False)
