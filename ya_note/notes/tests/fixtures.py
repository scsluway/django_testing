from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()


class TestFixtures(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='Reader')
        cls.note = Note.objects.create(
            title='1', text='2', slug='note-slug', author=cls.author
        )
        cls.auth_client = Client()
        cls.not_auth_client = Client()
        cls.not_auth_client.force_login(cls.reader)
        cls.auth_client.force_login(cls.author)
        cls.list_url = reverse('notes:list')
        cls.add_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')
        cls.login_url = reverse('users:login')
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
