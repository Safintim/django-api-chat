from django.urls import reverse
from django.conf import settings
from rest_framework import test


User = settings.AUTH_USER_MODEL


class ChatCreateTest(test.APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@mail.ru', password='hardpassword123',
        )
        self.other_user = User.objects.create_user(
            username='test2@mail.ru', password='hardpassword123',
        )
        self.client.force_login(user=self.user)
        self.not_valid_data_int = {'participants': 1}
        self.not_valid_data_empty_participants = {'participants': []}
        self.not_valid_data_not_exist_user = {'participants': [3]}
        self.not_valid_data_empty_title = {'participants': [self.other_user.pk]}

        self.valid_data_dialog = {'participants': [self.other_user.pk]}
        self.valid_data_group = {
            'title': '123',
            'participants': [self.other_user.pk],
        }

    def test_user_create_dialog_with_participants_int(self):
        """
        participants - массив ids пользователей
        """
        url = reverse('chats-create-dialog')
        response = self.client.post(
            url, data=self.not_valid_data_int, format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_user_create_dialog_with_participants_empty(self):
        url = reverse('chats-create-dialog')
        response = self.client.post(
            url, data=self.not_valid_data_empty_participants, format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_user_create_dialog_with_valid_data(self):
        """
        Пользователь может создать диалог с любым другим пользователем
        """
        url = reverse('chats-create-dialog')
        response = self.client.post(
            url, data=self.valid_data_dialog, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_create_dialog_with_not_exist_user(self):
        """
        Пользователь не может создать диалог с несуществующим пользователем
        """
        url = reverse('v0:chats-create-dialog')
        response = self.client.post(
            url, data=self.not_valid_data_not_exist_user, format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_user_create_group_with_participants_empty(self):
        url = reverse('chats-create-group')
        response = self.client.post(
            url, data=self.not_valid_data_empty_participants, format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_user_create_group_with_title_empty(self):
        url = reverse('chats-create-group')
        response = self.client.post(
            url, data=self.not_valid_data_empty_title, format='json',
        )
        self.assertEqual(response.status_code, 400)

    def test_user_create_group_with_valid_data(self):
        url = reverse('chats-create-group')
        response = self.client.post(
            url, data=self.valid_data_group, format='json',
        )
        self.assertEqual(response.status_code, 201)
