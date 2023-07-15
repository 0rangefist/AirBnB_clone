#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        """
        Test if creating a City instance with no arguments returns an object of type City.
        """
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        """
        Test if a newly created City instance is stored in the models.storage.all() dictionary.
        """
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        """
        Test if the id attribute of a City instance is a string.
        """
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        """
        Test if the created_at attribute of a City instance is a datetime object.
        """
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        """
        Test if the updated_at attribute of a City instance is a datetime object.
        """
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        """
        Test if state_id is a public class attribute of City.
        """
        cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cy))
        self.assertNotIn("state_id", cy.__dict__)

    def test_name_is_public_class_attribute(self):
        """
        Test if name is a public class attribute of City.
        """
        cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cy))
        self.assertNotIn("name", cy.__dict__)

    def test_two_cities_unique_ids(self):
        """
        Test if two City instances have unique IDs.
        """
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def test_two_cities_different_created_at(self):
        """
        Test if the created_at attribute of two City instances have different values.
        """
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def test_two_cities_different_updated_at(self):
        """
        Test if the updated_at attribute of two City instances have different values.
        """
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def test_str_representation(self):
        """
        Test the string representation of a City instance.
        """
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cystr = cy.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_unused(self):
        """
        Test if creating a City instance with an argument does not add the argument to the instance's __dict__.
        """
        cy = City(None)
        self.assertNotIn(None, cy.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """
        Test if creating a City instance with keyword arguments sets the corresponding attributes correctly.
        """
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cy.id, "345")
        self.assertEqual(cy.created_at, dt)
        self.assertEqual(cy.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """
        Test if creating a City instance with None keyword arguments raises a TypeError.
        """
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("object_instances.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("object_instances.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "object_instances.json")
        except IOError:
            pass

    def test_one_save(self):
        """
        Test if the save method updates the updated_at attribute of a City instance.
        """
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def test_two_saves(self):
        """
        Test if the save method updates the updated_at attribute of a City instance on multiple saves.
        """
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cy.save()
        self.assertLess(second_updated_at, cy.updated_at)

    def test_save_with_arg(self):
        """
        Test if calling save method of a City instance with an argument raises a TypeError.
        """
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def test_save_updates_file(self):
        """
        Test if the save method updates the corresponding file with the object's data.
        """
        cy = City()
        cy.save()
        cyid = "City." + cy.id
        with open("object_instances.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        """
        Test if the return value of to_dict method of a City instance is a dictionary.
        """
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """
        Test if the return value of to_dict method of a City instance contains the correct keys.
        """
        cy = City()
        self.assertIn("id", cy.to_dict())
        self.assertIn("created_at", cy.to_dict())
        self.assertIn("updated_at", cy.to_dict())
        self.assertIn("__class__", cy.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """
        Test if the return value of to_dict method of a City instance contains any dynamically added attributes.
        """
        cy = City()
        cy.middle_name = "Holberton"
        cy.my_number = 98
        self.assertEqual("Holberton", cy.middle_name)
        self.assertIn("my_number", cy.to_dict())
