"""Version information for ShiroInk."""

try:
    from importlib.metadata import version

    __version__ = version("shiroink")
except Exception:
    # Package is not installed, use fallback version
    __version__ = "2.0.0"

__author__ = "Massimo Bonvicini"
__license__ = "ISC"
