import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookModelForm
from catalog import constants


class RenewBookModelFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookModelForm()
        label = form.fields['due_back'].label
        self.assertTrue(label is None or label == 'Renewal date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookModelForm()
        expected_text = (
            f'Enter a date between now and {constants.NUM_OF_WEEKS} weeks '
            f'(default {constants.NUM_OF_WEEKS_DEFAULT}).'
        )
        self.assertEqual(form.fields['due_back'].help_text, expected_text)

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookModelForm(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(
            weeks=constants.NUM_OF_WEEKS, days=1
        )
        form = RenewBookModelForm(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookModelForm(data={'due_back': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime().date() + datetime.timedelta(
            weeks=constants.NUM_OF_WEEKS
        )
        form = RenewBookModelForm(data={'due_back': date})
        self.assertTrue(form.is_valid())
