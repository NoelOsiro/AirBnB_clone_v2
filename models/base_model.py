#!/usr/bin/python3
"""Test suite for the BaseModel class"""

from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def __init__(self, *args, **kwargs):
        """Initialize test class attributes"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Set up any necessary resources before running the tests"""
        pass

    def tearDown(self):
        """Clean up any resources that were created during testing"""
        try:
            os.remove('file.json')
        except:
            pass

    def test_default(self):
        """Test creating a default instance of BaseModel"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test creating an instance of BaseModel with kwargs"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """Test creating an instance with invalid kwargs (int)"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """Test saving an instance of BaseModel"""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """Test the __str__ method of BaseModel"""
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """Test the to_dict method of BaseModel"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """Test creating an instance with kwargs containing None"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """Test creating an instance with kwargs containing a single key"""
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """Test the type of the 'id' attribute"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """Test the type of the 'created_at' attribute"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """Test the type and inequality of 'updated_at' and 'created_at'"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    def test_equality(self):
        """Test equality of BaseModel instances"""
        i1 = self.value()
        i2 = self.value()
        self.assertNotEqual(i1, i2)

        i1.some_attribute = "some_value"
        self.assertNotEqual(i1, i2)

    def test_valid_uuid(self):
        """Test if the 'id' attribute is a valid UUID"""
        i = self.value()
        try:
            UUID(i.id, version=4)
        except ValueError:
            self.fail("Invalid UUID format")

    def test_default_values(self):
        """Test default values of BaseModel attributes"""
        i = self.value()
        self.assertEqual(i.created_at, i.updated_at)

    def test_json_serialization(self):
        """Test JSON serialization and deserialization of BaseModel"""
        i1 = self.value()
        json_str = json.dumps(i1.to_dict())
        i2 = self.value(**json.loads(json_str))
        self.assertEqual(i1, i2)

    def test_invalid_date_format(self):
        """Test __init__ with invalid date format"""
        invalid_date = {'created_at': 'invalid_date_format'}
        with self.assertRaises(ValueError):
            new = self.value(**invalid_date)

    def test_save_without_changes(self):
        """Test save method without changes"""
        i = self.value()
        initial_updated_at = i.updated_at
        i.save()
        self.assertEqual(initial_updated_at, i.updated_at)


if __name__ == '__main__':
    unittest.main()
