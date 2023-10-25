#!/bin/python3

import unittest
from server.dbconnection import DB_connection

credentials=dict()
credentials["name"]="status"
credentials["collection"]="memory"
credentials["address"]="mongodb://10.10.10.22:27017"
credentials["limit"]=10


class TestDataBase(unittest.TestCase):
    
    def test_get_database(self):
        db_connection = DB_connection(credentials)
        database = db_connection.get_database("status")
        self.assertEqual(database.name, "status", "Something went wrong.")

    def test_get_wrong_database(self):
        db_connection = DB_connection(credentials)
        database = db_connection.get_database("status")
        self.assertNotEqual(database.name, "memory", "Something went wrong.")
    
    def test_get_collection(self):
        db_connection = DB_connection(credentials)
        collect = db_connection.get_collection("memory")
        self.assertEqual(collect.name, "memory", "Something went wrong.")

if __name__=='__main__':
    unittest.main()
