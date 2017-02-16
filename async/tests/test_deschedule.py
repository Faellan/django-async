"""
    Test the deschedule API.
"""
from django.test import TestCase
# No name 'sha1' in module 'hashlib'
# pylint: disable=E0611
from hashlib import sha1

from async import schedule
from async.api import deschedule
from async.models import Job


def _example(*_a, **_kw):
    """An example function that can be used for testing purposes.
    """
    pass


class TestDeschedule(TestCase):
    """Make sure that descheduling works correctly.
    """
    def test_unicode_generated(self):
        """Make sure that the unicode generated by a real scheduled job
        and one used to create an identity match.
        """
        job1 = schedule('async.tests.test_deschedule._example')
        job2 = Job(name='async.tests.test_deschedule._example',
            args="[]", kwargs="{}")
        try:
            self.assertEqual(job1.identity, sha1(unicode(job2)).encode('utf-8').hexdigest())
        except NameError:
            self.assertEqual(job1.identity, sha1(str(job2).encode('utf-8')).hexdigest())

    def test_deschedule_by_name(self):
        """We must be able to deschedule a job by giving its name.
        """
        job = schedule('async.tests.test_deschedule._example')
        self.assertEqual(job.name, 'async.tests.test_deschedule._example')
        deschedule('async.tests.test_deschedule._example')
        job = Job.objects.get(pk=job.pk)
        self.assertIsNotNone(job.cancelled)

    def test_deschedule_by_function(self):
        """We must be able to schedule a job by giving a function.
        """
        job = schedule(_example)
        # Different versions of Django will import this file differently
        self.assertTrue(job.name.endswith(
            'async.tests.test_deschedule._example'))
        deschedule(_example)
        job = Job.objects.get(pk=job.pk)
        self.assertIsNotNone(job.cancelled)
