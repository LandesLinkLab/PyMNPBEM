# PyMNPBEM - Python implementation of the MNPBEM toolbox
#
# Copyright (C) 2026 Jaekak Yoo and PyMNPBEM contributors
#
# Based on the MNPBEM Toolbox
# Copyright (C) 2017 Ulrich Hohenester and Andreas Truegler
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-2.0-or-later

# Shim for tooling that still invokes setup.py directly. All packaging
# metadata lives in pyproject.toml; duplicating it here would let the two
# drift apart.

from setuptools import setup

setup()
