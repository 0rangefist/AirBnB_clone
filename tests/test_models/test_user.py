#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_no_args_instantiates(self):
        """Test that User class can be instantiated without any arguments."""
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        """Test that a newly created User instance is stored in the 'objects' attribute of 'models.storage'."""
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test that the 'id' attribute of a User instance is of type str."""
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        """Test that the 'created_at' attribute of a User instance is of type datetime."""
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test that the 'updated_at' attribute of a User instance is of type datetime."""
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        """Test that the 'email' attribute of a User instance is of type str."""
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        """Test that the 'password' attribute of a User instance is of type str."""
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        """Test that the 'first_name' attribute of a User instance is of type str."""
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        """Test that the 'last_name' attribute of a User instance is of type str."""
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        """Test that two User instances have different IDs."""
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_two_users_different_created_at(self):
        """Test that two User instances have different 'created_at' timestamps."""
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_two_users_different_updated_at(self):
        """Test that two User instances have different 'updated_at' timestamps."""
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_str_representation(self):
        """Test the string representation of a User instance."""
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        user_str = user.__str__()
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + dt_repr, user_str)
        self.assertIn("'updated_at': " + dt_repr, user_str)

    def test_args_unused(self):
        """Test that passing None as an argument to User instance does not affect the attributes."""
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test that a User instance can be created with specific attributes using keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test that passing None as a value for keyword arguments raises a TypeError."""
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Unittests for testing save method of the User class."""

    @classmethod
    def setUpClass(cls):
        """Set up the test case by renaming 'object_instances.json' to 'tmp'."""
        try:
            os.rename("object_instances.json", "tmp")
        except IOError:
            pass
    
    @classmethod

    def tearDownClass(cls):
        """Tear down the test case by removing 'object_instances.json' if it exists and renaming 'tmp' back to 'file.json'."""
        try:
            os.remove("object_instances.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "object_instances.json")
        except IOError:
            pass

    def test_one_save(self):
        """Test that calling save() on a User instance updates the 'updated_at' attribute."""
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def test_two_saves(self):
        """Test that calling save() multiple times updates the 'updated_at' attribute accordingly."""
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        second_updated_at = user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        user.save()
        self.assertLess(second_updated_at, user.updated_at)

    def test_save_with_arg(self):
        """Test that calling save() with an argument raises a TypeError."""
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_save_updates_file(self):
        """Test that calling save() updates the content of the 'obj_inst.json' file."""
        user = User()
        user.save()
        user_id = "User." + user.id
        with open("object_instances.json", "r") as f:
            self.assertIn(user_id, f.read())


class TestUserToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        """Test that the return value of to_dict() is of type dict."""
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that the dictionary returned by to_dict() contains the correct keys."""
        user = User()
        user_dict = user.to_dict()
        self.assertIn("id", user_dict)
        self.assertIn("created_at", user_dict)
        self.assertIn("updated_at", user_dict)
        self.assertIn("__class__", user_dict)

    def test_to_dict_contains_added_attributes(self):
        """Test that the dictionary returned by to_dict() contains any additional attributes added to the User instance."""
        user = User()
        user.middle_name = "Holberton"
        user.my_number = 98
        self.assertEqual("Holberton", user.middle_name)
        self.assertIn("my_number", user.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test that the datetime attributes in the dictionary returned by to_dict() are of type str."""
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test the content of the dictionary returned by to_dict()."""
        dt = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        expected_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), expected_dict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test that the dictionary returned by to_dict() is not the same as the instance's __dict__."""
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def test_to_dict_with_arg(self):
        """Test that calling to_dict() with an argument raises a TypeError."""
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)


if __name__ == "__main__":
    unittest.main()

