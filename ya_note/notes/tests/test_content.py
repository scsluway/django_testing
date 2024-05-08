from django.contrib.auth import get_user

from .fixtures import TestFixtures
from notes.forms import NoteForm


class TestContent(TestFixtures):

    def test_notes_list_for_different_users(self):
        clients = (
            (self.auth_client, True),
            (self.reader_client, False)
        )
        for client, note_in_list in clients:
            with self.subTest(client=get_user(client)):
                response = client.get(self.list_url)
                self.assertEqual(
                    (self.note in response.context['object_list']),
                    note_in_list
                )

    def test_pages_contains_form(self):
        for url in (self.add_url, self.edit_url):
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
