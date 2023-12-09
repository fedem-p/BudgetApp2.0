"""Tests for the utils functions."""
import os
import sys

import pytest

# Get the directory containing your module
module_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sys.path.append('../')
sys.path.insert(0, module_directory)
from core.utils.dummy_data import EXAMPLE_DATA  # pylint: disable=C0413

# pylint: disable=C0116, W0621
from core.utils.utils import dict2str, str2dict  # pylint: disable=C0413


@pytest.mark.parametrize("my_dict", [{k: k} for k in range(9)] + EXAMPLE_DATA)
def test_str_2_dict_conversion(my_dict):
    my_s = dict2str(my_dict)

    my_d = str2dict(my_s)

    assert my_d == my_dict
