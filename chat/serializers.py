from django.conf import settings
from rest_framework import serializers

from chat.tools import import_callable
from chat.models import Chat, Message, ParticipantChat
from chat.services import get_dialog_between_users
from chat.exceptions import ObjectAllreadyExists

User = settings.AUTH_USER_MODEL


class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )


class ChatSerializer(serializers.ModelSerializer):
    is_exist_unread_messages = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    recipient = serializers.SerializerMethodField()

    def get_is_exist_unread_messages(self, obj):
        user = self.context['request'].user
        return obj.is_exist_unread_messages(user)

    def get_title(self, obj):
        user = self.context['request'].user
        if obj.is_group:
            return obj.title

        recipient = obj.get_recipient_for_dialog(user)
        return recipient.nickname

    def get_recipient(self, obj):
        if not obj.is_group:
            user = self.context['request'].user
            recipient = obj.get_recipient_for_dialog(user)
            chat_settings = getattr(settings, 'CHAT_SETTINGS', {})
            UserSerializer = import_callable(
                chat_settings.get('USER_SERIALIZER', DefaultUserSerializer),
            )
            return UserSerializer(recipient).data

    class Meta:
        model = Chat
        fields = (
            'id',
            'title',
            'is_group',
            'created_at',
            'is_exist_unread_messages',
            'last_message_date',
            'last_message_text',
            'count_participants',
            'recipient',
        )


class ChatCreateSerializer:
    representation_serializer = ChatSerializer

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        current_user = self.context['request'].user
        participants.append(current_user.id)
        ids_users_in_db = set(
            User.objects.filter(id__in=participants).values_list(
                'id', flat=True,
            ),
        )
        users_not_in_db = list(set(participants) - ids_users_in_db)
        if users_not_in_db:
            raise serializers.ValidationError(
                {'participants': f'users with id {users_not_in_db} not exist'},
            )

        chat = Chat.objects.create(**validated_data)
        for user_id in ids_users_in_db:
            ParticipantChat.objects.create(chat=chat, user_id=user_id)
        return chat

    def to_representation(self, instance):
        serializer = self.representation_serializer(
            instance, context=self.context,
        )
        return serializer.data


class ChatCreateDialogSerializer(
    ChatCreateSerializer,
    serializers.ModelSerializer,
):
    participants = serializers.ListSerializer(
        child=serializers.IntegerField(min_value=1),
    )

    class Meta:
        model = Chat
        fields = (
            'id',
            'participants',
        )

    def validate(self, attr):
        participants = attr.get('participants')
        if not participants or len(participants) != 1:
            raise serializers.ValidationError(
                {'participants': 'This is dialogue, must contain one user_id'},
            )

        participant_id = participants[0]
        current_user = self.context['request'].user
        if participant_id == current_user.id:
            raise serializers.ValidationError(
                {'participants': 'You cannot create a dialogue by yourself'},
            )

        chat = get_dialog_between_users(participant_id, current_user.id)
        if chat:
            serializer = self.representation_serializer(
                chat, context=self.context,
            )
            raise ObjectAllreadyExists(
                detail=serializer.data,
            )
        return attr

    def create(self, validated_data):
        validated_data.update({'is_group': False})
        return super().create(validated_data)


class ChatCreateGroupSerializer(
    ChatCreateSerializer,
    serializers.ModelSerializer,
):
    participants = serializers.ListSerializer(
        child=serializers.IntegerField(min_value=1),
    )

    class Meta:
        model = Chat
        fields = (
            'id',
            'title',
            'participants',
        )
        extra_kwargs = {'title': {'required': True, 'allow_null': False}}

    def validate(self, attr):
        participants = attr.get('participants')
        if not participants or not len(participants):
            raise serializers.ValidationError(
                {'participants': 'This is group,must contain more one user_id'},
            )
        return attr

    def create(self, validated_data):
        validated_data.update({'is_group': True})
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'text',
            'created_at',
            'user',
        )


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'text',
        )
