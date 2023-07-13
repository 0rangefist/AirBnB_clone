#!/usr/bin/python3
"""
Unit tests for the BaseModel class
"""
import uuid
import unittest
from datetime import datetime
from models.base_model import BaseModel
import json
import os


class TestBaseModelInit(unittest.TestCase):
    def test_no_args_creates_instance(self):
        # Test that creating an instance without any arguments is successful
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)

    def test_instance_has_attributes(self):
        # Test that the instance has the required attributes:
        # id, created_at, & updated_at
        model = BaseModel()
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))
        self.assertTrue(hasattr(model, "updated_at"))

    def test_id_is_valid_string_uuid(self):
        # Test that the id attribute is a string (UUID4)
        model = BaseModel()
        self.assertIsNotNone(model.id)
        self.assertIsInstance(model.id, str)
        self.assertEqual(uuid.UUID(model.id).version, 4)

    def test_created_at_is_datetime(self):
        # Test that the created_at attribute is a datetime object
        model = BaseModel()
        self.assertIsInstance(model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        # Test that the updated_at attribute is a datetime object
        model = BaseModel()
        self.assertIsInstance(model.updated_at, datetime)

    def test_created_at_equals_updated_at(self):
        # Test that created_at and updated_at attributes are equal upon init
        model = BaseModel()
        self.assertEqual(model.created_at, model.updated_at)

    def test_unique_ids(self):
        # Test that two BaseModel instances have different (unique) ids
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_kwargs_creates_instance(self):
        # Test that creating an instance with kwargs is successful
        model_dict = {
            "id": "some_id",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "some_attribute": "some value"
        }
        model = BaseModel(**model_dict)
        self.assertIsInstance(model, BaseModel)
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))
        self.assertTrue(hasattr(model, "updated_at"))
        self.assertTrue(hasattr(model, "some_attribute"))

    def test_kwargs_with_ignored_args_creates_instance(self):
        # Test that args are ignored and kwargs are correctly
        # used to create an instance
        model_dict = {
            "id": "some_id",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "some_attribute": "some value"
        }
        model = BaseModel("ignored arg", **model_dict)
        self.assertIsInstance(model, BaseModel)
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))
        self.assertTrue(hasattr(model, "updated_at"))
        self.assertTrue(hasattr(model, "some_attribute"))


class TestBaseModelSave(unittest.TestCase):
    file_path = "object_instances.json"

    def test_updated_at_changes(self):
        # Test that the updated_at attribute changes to
        # a new datetime upon calling save()
        model = BaseModel()
        initial_updated_at = model.updated_at

        model.save()

        self.assertNotEqual(model.updated_at, initial_updated_at)

    def test_instance_saved_to_file(self):
        # Test that the BaseModel instance is saved to file_path
        model = BaseModel()

        model.save()

        # Load the contents of the file
        with open(self.file_path, "r") as file:
            data = json.load(file)

        # Check if the instance of BaseModel.id is a key in loaded data
        self.assertIn("BaseModel." + model.id, data)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


class TestBaseModelToDict(unittest.TestCase):
    def test_returns_dictionary(self):
        # Test that to_dict() returns a dictionary
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIsInstance(model_dict, dict)

    def test_keys_values_in_dict(self):
        # Test that all keys and values from the instance's "__dict__" are
        # present in the returned dictionary except "created_at" & "updated_at"
        model = BaseModel()
        model_dict = model.to_dict()

        for key, value in model.__dict__.items():
            self.assertIn(key, model_dict)
            if key != "created_at" and key != "updated_at":
                self.assertEqual(value, model_dict[key])

    def test_class_key_present(self):
        # Test that the "__class__" key with the value of the instance's
        # class name is present in the returned dictionary
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertIn("__class__", model_dict)
        self.assertEqual(model_dict["__class__"], model.__class__.__name__)

    def test_created_at_iso_format(self):
        # Test that value for the “created_at” key in the returned dictionary
        # is a string in ISO format
        model = BaseModel()
        dict = model.to_dict()
        self.assertIn("created_at", dict)
        self.assertIsInstance(dict["created_at"], str)
        self.assertEqual(dict["created_at"], model.created_at.isoformat())

    def test_updated_at_iso_format(self):
        # Test that value for the “updated_at” key in the returned dictionary
        # is a string in ISO format
        model = BaseModel()
        dict = model.to_dict()
        self.assertIn("updated_at", dict)
        self.assertIsInstance(dict["updated_at"], str)
        self.assertEqual(dict["updated_at"], model.updated_at.isoformat())


if __name__ == "__main__":
    unittest.main()
