import pytest
from unittest.mock import MagicMock, patch, call, ANY

import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui import *
import accounts

@pytest.fixture
def mock_gui(monkeypatch):
    
    # Mock Gui components
    with patch('customtkinter.CTk') as mock_ctk, \
         patch('CTkMessagebox.CTkMessagebox'), \
         patch('PIL.Image.open'), \
         patch('gui.CTkImage'), \
         patch('gui.CTkFrame'), \
         patch('gui.CTkButton') as mock_button, \
         patch('gui.CTkLabel'), \
         patch('gui.CTkEntry'), \
         patch('gui.CTkScrollableFrame'):

        # Create mock user account
        mock_user = MagicMock(spec=accounts.Account)
        mock_user.get_is_admin.return_value = False
        mock_user.get_user_name.return_value = "TestUser"
        mock_user.get_favourites.return_value = []
        
        # Patch the global userAccount in gui module
        monkeypatch.setattr('gui.userAccount', mock_user)

        # Mock main app window
        mock_app = MagicMock()
        mock_ctk.return_value = mock_app

        yield {
            'app': mock_app,
            'user_account': mock_user,
            'ctk_button': mock_button
        }

def test_create_celebrity_row(mock_gui):
    # UT-23-OB: Test celebrity row creation and proper buttons
    mock_scroll = MagicMock()
    mock_scroll.winfo_children.return_value = []
    
    test_celeb = {
        "first_name": "Test",
        "last_name": "Celeb",
        "date_of_birth": "2000-01-01",
        "date_of_death": "",
        "industry": "Tech",
        "biography": "Test bio",
        "images_path": "test.png"
    }
    
    createCelebrityRow([test_celeb], mock_scroll)
    
    # Verify button creation with command parameter
    mock_gui['ctk_button'].assert_any_call(
        ANY,  
        text="Learn More",
        width=60,
        command=ANY  
    )

def test_favorite_buttons(mock_gui):
    # UT-24-OB: Test favourite button with Account mocking
    mock_user = mock_gui['user_account']
    
    # Test add favorite
    addFavouriteButtonFunc(MagicMock(), MagicMock(), "test.csv", "TestCeleb")
    mock_user.add_favourite.assert_called_once_with("test.csv", "TestCeleb")
    
    # Test remove favorite
    mock_user.get_favourites.return_value = ["TestCeleb"]
    removeFavouriteButtonFunc(MagicMock(), MagicMock(), "test.csv", "TestCeleb")
    mock_user.remove_favourite.assert_called_once_with("test.csv", "TestCeleb")



if __name__ == "__main__":
    pytest.main()