from django.db.models import Max
from rest_framework import decorators, permissions, response, status, viewsets

from chat.models import Chat
from chat.pagination import CustomPagination
from chat.services import read_messages
from chat.serializers import (
    ChatCreateDialogSerializer,
    ChatCreateGroupSerializer,
    ChatSerializer,
    MessageSerializer,
)


class ChatViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'options', 'post']
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    serializer_action_classes = {
        'list': ChatSerializer,
        'retrieve': MessageSerializer,
        'create_dialog': ChatCreateDialogSerializer,
        'create_group': ChatCreateGroupSerializer,
    }

    def get_queryset(self):
        current_user = self.request.user
        queryset = Chat.objects.annotate(
            last_date=Max('messages__created_at')
        ).filter(
            participants=current_user,
        ).order_by('-last_date')

        if self.action == 'list':
            queryset = queryset.exclude(messages=None)
        return queryset

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def get_paginated_response(self, data, custom_data=None):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, custom_data)

    def retrieve(self, request, *args, **kwargs):
        chat = self.get_object()

        read_messages(request.user, chat)

        chat_serializer = ChatSerializer(chat, context={'request': request})
        queryset = chat.messages.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            message_serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                message_serializer.data, chat_serializer.data,
            )

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return response.Response(status.HTTP_403_FORBIDDEN)

    @decorators.action(methods=['post'], detail=False, url_path='dialog')
    def create_dialog(self, request, *args, **kwargs):
        return super(viewsets.ModelViewSet, self).create(
            request, *args, **kwargs,
        )

    @decorators.action(methods=['post'], detail=False, url_path='group')
    def create_group(self, request, *args, **kwargs):
        return super(viewsets.ModelViewSet, self).create(
            request, *args, **kwargs,
        )
