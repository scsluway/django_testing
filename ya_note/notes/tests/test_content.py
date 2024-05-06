from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='Reader')
        cls.note = Note.objects.create(title='1', text='2', author=cls.author)

    def test_notes_list_for_different_users(self):
        users = (
            (self.author, True),
            (self.reader, False)
        )
        url = reverse('notes:list')
        for user, note_in_list in users:
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual((self.note in object_list), note_in_list)

    def test_pages_contains_form(self):
        url_names = (
            ('notes:add', None),
            ('notes:edit', (self.note.id,))
        )
        self.client.force_login(self.author)
        for name, args in url_names:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
