#!/usr/bin/python

# This file is part of ZemoteHost.
# 
# ZemoteHost is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ZemoteHost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ZemoteHost. If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
from ZemoteCore import __version__ as zemote_version

setup(name = "Zemote Host",
      version = zemote_version,
      description = "Host software for Zemote",
      author = "Cameron Lai",
      url = "http://github.com/cameronlai/ZemoteHost/",
      license = "GPLv3",
      packages = ["gui"],
      scripts = ["ZemoteHost.py", "ZemoteCore.py"],
      )
