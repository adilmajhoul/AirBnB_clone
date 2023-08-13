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
import pycodestyle


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

class Testcodestyle(unittest.TestCase):
    """test codestyle"""
    def test_pep8(self):
        """test pep8"""
        pyc = pycodestyle.StyleGuide(quiet=True)
        result = pyc.check_files(["models/user.py"])
        errorMessage = "Found code style errors (and warnings)."
        self.assertEqual(result.total_errors, 0, errorMessage)


if __name__ == '__main__':
    unittest.main()
