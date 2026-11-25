import os
import sys
import pytest
from unittest.mock import MagicMock
import pigal_flask.interfaces as pkg

def test_is_configured_with_nothing():
    assert pkg.PublicApi()

