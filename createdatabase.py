#!/usr/bin/env python3
#
# createdatabase.py - Create database for jvinventory app.
#
# Copyright (c) 2015 - Jesus Vedasto Olazo <jestoy.olazo@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

import sqlite3
import os


class CreateDatabase:

    def __init__(self, com_name,
                 com_address,
                 com_telephone,
                 com_fax,
                 com_email
                 ):
        self.com_name = com_name
        self.com_address = com_address
        self.com_telephone = com_telephone
        self.com_fax = com_fax
        self.com_email = com_email
        # Create the database.
        self.database = sqlite3.connect('inv_database.db')
        self.cur = self.database.cursor()

    def create(self):
        # Create item table.
        self.cur.execute("""
            CREATE TABLE item(rowid INTEGER PRIMARY KEY,
                itemcode TEXT,
                description TEXT,
                unit TEXT)
            """)
        # Create incoming transaction table.
        self.cur.execute("""
            CREATE TABLE incoming(rowid INTEGER PRIMARY KEY,
                itemcode TEXT,
                description TEXT,
                unit TEXT,
                quantity REAL,
                rate REAL,
                date DATE,
                remarks TEXT)
            """)
        # Create outgoing transaction table.
        self.cur.execute("""
            CREATE TABLE outgoing(rowid INTEGER PRIMARY KEY,
                itemcode TEXT,
                description TEXT,
                unit TEXT,
                quantity REAL,
                rate REAL,
                date DATE,
                remarks TEXT)
            """)
        # Create company details.
        self.cur.execute("""
            CREATE TABLE company(com_name TEXT,
                com_address TEXT,
                com_telephone TEXT,
                com_fax TEXT,
                com_email TEXT)
            """)
        # Insert company details.
        self.cur.execute("INSERT INTO company VALUES(?, ?, ?, ?, ?)",
                         (self.com_name,
                          self.com_address,
                          self.com_telephone,
                          self.com_fax,
                          self.com_email))
        # Apply the changes.
        try:
            self.database.commit()
        except sqlite3.Error:
            self.database.rollback()
        # Close the database.
        if self.database:
            self.cur.close()
            self.database.close()


def main():
    company = 'ABC Company'
    address = 'Balayan, Batangas'
    telephone = '222-3333'
    fax = '444-5555'
    email = 'email@yourcomany.com'
    
    if os.path.isfile('inv_database.db'):
        print('Database is available.')
    else:
        # Initialize the database.
        data = CreateDatabase(company,
                              address,
                              telephone,
                              fax,
                              email
                              )
        # Create the database and tables.
        data.create()

if __name__ == '__main__':
    main()
