#!/usr/bin/env python
"""
K-Map Solver with GPT-4o Integration

This project is based on the original KMapSolver by salmanmorshed:
https://github.com/salmanmorshed/KMapSolver

Original Copyright (C) salmanmorshed
This enhanced version adds GPT-4o integration and MCP server capabilities.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import sys
import wx
from guis import KMapGui2, KMapGui3, KMapGui4


if __name__ == '__main__':
    gui_classes = [KMapGui2, KMapGui3, KMapGui4]

    app = wx.App()

    choice_dialog = wx.SingleChoiceDialog(None,
                                          'How many variables?',
                                          'Variables',
                                          ['2 variables', '3 variables', '4 variables'])
    if choice_dialog.ShowModal() == wx.ID_CANCEL:
        sys.exit()

    selection = choice_dialog.GetSelection()
    gui_classes[selection]()
    choice_dialog.Destroy()
    app.MainLoop()
