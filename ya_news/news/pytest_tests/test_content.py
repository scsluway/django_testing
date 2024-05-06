from django.conf import settings
from django.urls import reverse

import pytest
from pytest_django.asserts import assertRedirects
from http import HTTPStatus

HOME_URL = reverse('news:home')