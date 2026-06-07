"""
conftest.py -- shared fixtures and path setup for the tests.

Adds analytics/ and creatives/ to sys.path so imports
from the tests work without installing the package.
"""

import sys
import os

# Project root -- one level above tests/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add analytics/ and creatives/ to sys.path for imports
sys.path.insert(0, os.path.join(ROOT, "analytics"))
sys.path.insert(0, os.path.join(ROOT, "creatives"))
