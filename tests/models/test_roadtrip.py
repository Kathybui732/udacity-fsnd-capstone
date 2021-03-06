import unittest

from sqlalchemy.exc import IntegrityError

from api import create_app, db
from api.database.models import User, City, RoadTrip


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.city_1 = City(
            name='Denver', state='CO', lat=1.23, lng=3.45, city_id=1
        )
        self.city_1.insert()
        self.city_2 = City(
            name='Arvada', state='CO', lat=2.23, lng=4.45, city_id=2
        )
        self.city_2.insert()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_roadtrip_model(self):
        rt = RoadTrip(
            name='daily commute',
            start_city_id=self.city_1.id,
            end_city_id=self.city_2.id
        )
        rt.insert()

        self.assertIsInstance(rt, RoadTrip)
        self.assertIsNotNone(rt.id)
        self.assertEqual('daily commute', rt.name)
        self.assertEqual(rt.start_city_id, self.city_1.id)
        self.assertEqual(rt.end_city_id, self.city_2.id)

    def test_roadtrip_model_trimmed_strings(self):
        rt = RoadTrip(
            name=' daily commute ',
            start_city_id=self.city_1.id,
            end_city_id=self.city_2.id
        )
        rt.insert()

        self.assertEqual('daily commute', rt.name)

    def test_roadtrip_model_blank_name(self):
        try:
            rt = RoadTrip(
                name='',
                start_city_id=self.city_1.id,
                end_city_id=self.city_2.id
            )
            rt.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_roadtrip_model_missing_name(self):
        try:
            rt = RoadTrip(
                name=None,
                start_city_id=self.city_1.id,
                end_city_id=self.city_2.id
            )
            rt.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_roadtrip_model_missing_city1(self):
        try:
            rt = RoadTrip(
                name='daily commute',
                start_city_id=None,
                end_city_id=self.city_2.id
            )
            rt.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_roadtrip_model_missing_city2(self):
        try:
            rt = RoadTrip(
                name='daily commute',
                start_city_id=self.city_1.id,
                end_city_id=None
            )
            rt.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    def test_roadtrip_start_city(self):
        rt = RoadTrip(
            name='daily commute',
            start_city_id=self.city_1.id,
            end_city_id=self.city_2.id
        )
        rt.insert()

        result = rt.start_city().city_state()
        self.assertEqual('Denver, CO', result)

    def test_roadtrip_end_city(self):
        rt = RoadTrip(
            name='daily commute',
            start_city_id=self.city_1.id,
            end_city_id=self.city_2.id
        )
        rt.insert()

        result = rt.end_city().city_state()
        self.assertEqual('Arvada, CO', result)
