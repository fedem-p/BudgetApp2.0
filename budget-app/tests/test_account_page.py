# import os
# import sys

# import pytest

# # Get the directory containing your module
# module_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # sys.path.append('../')
# sys.path.insert(0, module_directory)

# from core.account_panel import AccountPage
# from core.data_manager import DataManager

# from kivymd.uix.list import (
#     IconLeftWidget,
#     IconRightWidget,
#     MDList,
#     OneLineAvatarIconListItem,
# )

# TEST_FOLDER_PATH = "/tmp/tmp_dir/"

# @pytest.fixture
# def data_manager():
#     dm = DataManager(data_folder=TEST_FOLDER_PATH)
#     dm.initialize_data()
#     return dm

# def test_new_account_widget(data_manager):
#     dm = data_manager

#     account_page = AccountPage(dm)
