from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Event, Outcomes
from .views import EventViewSet


User = get_user_model()


class OutcomeTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="football match",
            date=timezone.now(),
            description="",
            is_finished=False,
        )

    def test_outcome_is_success(self):
        """Check outcome.is_success"""
        outcome = Outcomes.objects.create(
            event=self.event, cf=1.2, name="team 1 wins", success=True
        )

        self.assertTrue(
            outcome.is_success(), "outcome.is_success must be true if suceess is true"
        )

        outcome = Outcomes.objects.create(
            event=self.event, cf=1.2, name="team 2 wins", success=False
        )

        self.assertFalse(
            outcome.is_success(), "outcome.is_success must be false if suceess is false"
        )

    def test_example_assert_raises(self):
        """Check self.assertRaises work"""
        with self.assertRaises(ObjectDoesNotExist):
            Event.objects.get(name="football match2")


class EventViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.viewset = EventViewSet.as_view({"post": "create"})

        self.admin_user = User.objects.create_superuser(
            username="testadminuser",
            email="test@example.com",
            password="strongpassword123",
        )

        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="strongpassword123"
        )

    def test_create(self):
        "Check event creation"

        match_date = timezone.now()

        request = self.factory.post(
            "/api/v1/events/",
            data={
                "name": "football match",
                "date": match_date,
                "description": "sample test event",
                "is_finished": False,
            },
            format="json",
        )

        response = self.viewset(request)
        self.assertEqual(
            response.status_code, 403, "only authenticated user can create event"
        )

        force_authenticate(request, self.user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 403, "only admin user can create event")

        force_authenticate(request, self.admin_user)
        response = self.viewset(request)
        self.assertEqual(response.status_code, 201, "created status code must be 201")

        newEvent = Event.objects.get(name="football match")

        self.assertEqual(
            newEvent.name, "football match", "new event name must match provided"
        )
        self.assertEqual(
            newEvent.description,
            "sample test event",
            "new event description must match provided",
        )
        self.assertFalse(newEvent.is_finished, "event must have provided is_finished")
        self.assertEqual(newEvent.date, match_date, "event must have provided date")
