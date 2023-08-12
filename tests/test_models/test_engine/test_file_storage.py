import unittest
import os
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel
from models import storage


class TestFileStorage(unittest.TestCase):

    def test_all(self):
        """ test the all() method of storage """
        all_objects = storage.all()
        self.assertIsInstance(all_objects, dict)

    def test_new(self):
        """ test adding a new object to storage """
        user = User()
        user_id = user.id
        storage.new(user)
        self.assertIn(f"User.{user_id}", storage.all())

    def test_save_and_reload(self):
        """ test saving and reloading objects to/from a file """
        user = User()
        storage.new(user)
        storage.save()
        storage.reload()
        all_objects = storage.all()
        self.assertIn(f"User.{user.id}", all_objects)
        self.assertIsInstance(all_objects[f"User.{user.id}"], User)


if __name__ == '__main__':
    unittest.main()
