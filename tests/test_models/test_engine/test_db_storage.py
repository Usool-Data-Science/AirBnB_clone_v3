#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the db class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        ex_state = {"name": "Abuja"}
        state1 = State(**ex_state)
        models.storage.new(state1)
        models.storage.save()

        session = models.storage._DBStorage__session
        everything = session.query(State).all()
        self.assertNotEquals(len(everything), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        ex_state = {"name": "Abuja"}
        state1 = State(**ex_state)
        models.storage.new(state1)
        models.storage.save()

        session = models.storage._DBStorage__session
        abuja = session.query(State).where(State.name == 'Abuja').one_or_none()
        self.assertNotNone(abuja)
        self.assertEqual(state1.id, abuja.id)
        self.assertEqual(state1.name, abuja.name)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """
        Test that save properly saves objects to database by:
            First add Abuja to the db, then add Kano to the db.
            Check the len before and after Kano they must not
            be equal otherwise data is not properly being saved.
        """
        ex_state1 = {"name": "Abuja"}
        state1 = State(**ex_state1)
        models.storage.new(state1)
        models.storage.save()
        session = models.storage._DBStorage__session
        after_abuja = session.query(State).all()

        ex_state2 = {"name": "Kano"}
        state1 = State(**ex_state2)
        models.storage.new(state1)
        models.storage.save()
        session = models.storage._DBStorage__session
        after_Kano = session.query(State).all()

        self.assertNotEqual(len(after_abuja), len(after_Kano))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """
        Tests if the get function is working perfectly by:
            1. Create a valid state instance, then use storage.get()
                to retrieve it back
            2. Compare the id of the retrieved to the id of the instance.
                They must be equal
            3. Then try with a valid State but wrong ID
            4. Then try with an invalid class e.g. STATES instead of State,
                or Country instead of City
        """
        storage = models.storage
        storage.reload()
        ex_state1 = {"name": "Calabar"}
        state1 = State(**ex_state1)
        models.storage.new(state1)
        models.storage.save()
        calabar = models.storage.get(State, state1.id)
        self.assertEqual(calabar.id, state1.id)

        wrong_id = models.storage.get(State, 'wrong_id')
        self.assertIsNone(wrong_id)

        invalid_class = models.storage.get('STATES', 'any_id')
        self.assertIsNone(invalid_class)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """
        Test the count function by:
            Creating 2 instances of objects and then count the instance
            and also remove the object to count all instances.
        """
        storage = models.storage
        storage.reload()
        ex_state1 = {"name": "Calabar"}
        state1 = State(**ex_state1)
        models.storage.new(state1)
        models.storage.save()

        ex_city1 = {'name': 'Ibadan', 'state_id': state1.id}
        city1 = City(**ex_city1)

        models.storage.new(city1)
        models.storage.save()

        state_count = models.storage.count(State)
        self.assertEqual(state_count, len(storage.all(State)))

        all_count = models.storage.count()
        self.assertEqual(all_count, len(storage.all()))
