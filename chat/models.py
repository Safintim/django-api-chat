from django.db import models
from django.conf import settings


class Chat(models.Model):
    title = models.CharField(
        'Название',
        max_length=1000,
        blank=True,
        null=True,
    )
    is_group = models.BooleanField('Групповой чат', default=False)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='chat.ParticipantChat',
        verbose_name='Участники',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self):
        return f'Чат №{self.id}-{self.title}'

    def is_exist_unread_messages(self, user):
        return Chat.objects.filter(
            id=self.id,
            messages__messagestatus__user=user,
            messages__messagestatus__is_read=False,
        ).exists()

    def last_message_date(self):
        last_message = self.messages.first()
        if last_message:
            return last_message.created_at
    last_message_date.short_description = 'Дата последнего сообщения'

    def last_message_text(self):
        last_message = self.messages.first()
        if last_message:
            return last_message.text
    last_message_text.short_description = 'Последнее сообщение'

    def get_recipient_for_dialog(self, request_user):
        if not self.is_group:
            user1, user2 = self.participants.all()
            return user2 if request_user == user1 else user1

    def count_participants(self):
        return self.participants.count()
    count_participants.short_description = 'Количество участников'


class ParticipantChat(models.Model):
    chat = models.ForeignKey(
        'chat.Chat',
        on_delete=models.CASCADE,
        verbose_name='Чат',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чатов'
        unique_together = ('chat', 'user')

    def __str__(self):
        return f'Чат №{self.chat}-{self.user}'


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Чат',
    )
    text = models.TextField('Текст сообщения')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.user} - {self.text[:20]}...'

    def type_chat(self):
        return 'Группа' if self.chat.is_group else 'Диалог'
    type_chat.short_description = 'Тип чата'


class MessageStatus(models.Model):
    message = models.ForeignKey(
        'chat.Message',
        on_delete=models.CASCADE,
        verbose_name='Сообщение',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    is_read = models.BooleanField('Прочитано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Статус сообщений'
        verbose_name_plural = 'Статус сообщений'
        ordering = ('-id', )

    def __str__(self):
        return f'Сообщение №{self.message_id} прочитал {self.user}'
