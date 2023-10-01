#!/usr/bin/env python3
#
# tarsierstock.py - A simple inventory software.
#
# Copyright (c) 2023 - Jesus Vedasto Olazo <jestoy.olazo@gmail.com>
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

import PySimpleGUI as sg
import os
import sys
from datetime import datetime
from dtbase.dtbase import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__appname__ = "Tarsier Stock"
__description__ = "A simple inventory software for small business."
__version__ = "1.0"
__author__ = "Jesus Vedasto Olazo"
__email__ = "jestoy.olazo@gmail.com"
__web__ = "https://jesusolazo.rf.gd"
__license__ = "GPLV2"
__status__ = "Development"
__maintainer__ = "Jesus Vedasto Olazo"
__copyright__ = "Copyright (c) 2023 - Jesus Vedasto Olazo"

DB_NAME = "tarsierstock.sqlite"
ENGINE = create_engine(f'sqlite:///{DB_NAME}')

if not os.path.exists(DB_NAME):
    Base.metadata.create_all(ENGINE)

Base.metadata.bind = ENGINE
DBSession = sessionmaker(bind=ENGINE)


def product_window():
    layout = [
        [sg.T('Product Window')],
        [sg.B('Quit')]
    ]

    window = sg.Window('Product', layout)

    while True:
        # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()

def company_window():
    layout = [
        [sg.T('Company Window')],
        [sg.B('Quit')]
    ]

    window = sg.Window('Company', layout)

    while True:
        # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()

def license_window():
    layout = [
        [sg.T('License Window')],
        [sg.B('Quit')]
    ]

    window = sg.Window('License', layout)

    while True:
        # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()

def report_window():
    layout = [
        [sg.T('Report Window')],
        [sg.B('Quit')]
    ]

    window = sg.Window('Report', layout)

    while True:
        # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()

def trans_window(mode):
    layout = [
        [sg.T('Transaction window')],
        [sg.B('Quit')]
    ]

    window = sg.Window(f'{mode}', layout)

    while True:
        # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()

def about_window():
    layout = [
        [sg.T(f'{__appname__}')],
        [sg.T(f'version: {__version__}')],
        [sg.T(f'{__description__}')],
        [sg.T(f'{__author__}')],
        [sg.T(f'{__email__}')],
        [sg.T(f'{__web__}')],
        [sg.T(f'{__license__}')],
        [sg.B('Quit')]
    ]

    window = sg.Window('About', layout)

    while True:
        # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break

    window.close()

def main():
    # Set the theme.
    sg.theme('DarkGrey3')
    # Widgets layout
    layout = [
        [sg.Menu([['File', ['Product', 'Incoming', 'Outgoing', '---', 'Quit']],
            ['Option', ['Themes']],
            ['Help', ['License', 'Company', '---', 'About']]])
            ],
        [sg.B('Product'), sg.B('Incoming'), sg.B('Outgoing'),
        sg.B('Report'), sg.B('Quit')]
    ]

    window = sg.Window(f'Tarsier Stock - {__version__}', layout)

    while True:
        # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        if event == 'About':
            about_window()
        if event in ('Incoming', 'Outgoing'):
            trans_window(event)
        if event == 'Report':
            report_window()
        if event == 'Company':
            company_window()
        if event == 'License':
            license_window()
        if event == 'Product':
            product_window()

    window.close()

if __name__ == "__main__":
    main()
