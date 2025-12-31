"""Version information for ShiroInk."""

import os
import re

try:
    from importlib.metadata import version

    __version__ = version("shiroink")
except Exception:
    # Package is not installed, read from pyproject.toml
    try:
        pyproject_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "pyproject.toml"
        )
        with open(pyproject_path, "r") as f:
            content = f.read()
            match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
            if match:
                __version__ = match.group(1)
            else:
                __version__ = "unknown"
    except Exception:
        __version__ = "unknown"

__author__ = "Massimo Bonvicini"
__license__ = "ISC"
