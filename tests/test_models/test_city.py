#!/usr/bin/python3
import unittest
from models.engine.file_storage import FileStorage
from models.city import City
from models import storage

""" city class unit test """


class TestCity(unittest.TestCase):
    """ city class unit test """

    def setUp(self):
        self.city = City()
        self.city.name = "San Francisco"
        self.city.state_id = "CA"

    def tearDown(self):
        del self.city

    def test_save_reload_city(self):
        """ test that a City object can be saved and reloaded correctly """
        storage.new(self.city)
        storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        new_objects = new_storage.all()
        self.assertIn(f"City.{self.city.id}", new_objects)
        new_city = new_objects[f"City.{self.city.id}"]
        self.assertEqual(new_city.name, self.city.name)
        self.assertEqual(new_city.state_id, self.city.state_id)

    def test_reload(self):
        """ ensure that reload works """
        len_before = len(storage.all())
        storage.new(City())
        storage.reload()
        len_after = len(storage.all())
        self.assertEqual(len_after, len_before + 1)

class Testpycodestyle(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
