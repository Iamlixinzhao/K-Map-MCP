"""
K-Map Solver Helper Functions

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

def go_right(lst, i, j):
    try: return i, j+1, lst[i][j+1]
    except IndexError: return i, 0, lst[i][0]


def go_left(lst, i, j):
    return i, (j-1 if j != 0 else len(lst[i])-1), lst[i][j-1]


def go_up(lst, i, j):
    return (i-1 if i != 0 else len(lst)-1), j, lst[i-1][j]


def go_down(lst, i, j):
    try: return i+1, j, lst[i+1][j]
    except IndexError: return 0, j, lst[0][j]


def is_subset(lsa, lsb):  # Is lsb subset of lsa? Alternate: not set.isdisjoint()
    for b in lsb:
        if b in lsa: continue
        else: return False
    return True
