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

# Set theme to use
sg.theme('BluePurple')

# Widgets layout
layout = [
    [sg.Menu([['File', ['Quit']], ['Option'], ['Help']])],
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

window.close()
