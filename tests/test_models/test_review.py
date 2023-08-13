#!/usr/bin/python3
import json
import unittest
from models.base_model import BaseModel
from datetime import datetime
import pycodestyle
from models.user import User
import models
from io import StringIO
import sys
from unittest.mock import patch


class Testtheuser(unittest.TestCase):
    """test the user class"""
    def test_theuser(self):
        """test the user"""
        new = User()
        self.assertTrue(hash(new), "id")
        self.assertTrue(hasattr(new, "created_at"))
        self.assertTrue(hasattr(new, "updated_at"))
        self.assertTrue(hasattr(new, "email"))
        self.assertTrue(hasattr(new, "password"))
        self.assertTrue(hasattr(new, "first_name"))
        self.assertTrue(hasattr(new, "last_name"))
        """type test"""
        self.assertIsInstance(new.email, str)
        self.assertIsInstance(new.password, str)
        self.assertIsInstance(new.first_name, str)
        self.assertIsInstance(new.last_name, str)

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
