import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
import unittest
from unittest.mock import MagicMock
import customtkinter as ctk
import gui  # Import your GUI script

class TestGUI(unittest.TestCase):

    def setUp(self):
        """Reinitialize the GUI before each test."""
        gui.app = ctk.CTk()
        gui.app.title("TERNOPS - Celebrity Bio Application")

        # Initialize actual frames to prevent NoneType issues
        gui.mainFrame = ctk.CTkFrame(gui.app)
        gui.signInFrame = ctk.CTkFrame(gui.app)
        gui.editCelebrityFrame = ctk.CTkFrame(gui.app)  # Ensure it exists
        gui.celebrityFrame = ctk.CTkFrame(gui.app)
        gui.filterFrame = ctk.CTkFrame(gui.app)

        # Mock frame hiding methods
        gui.mainFrame.pack_forget = MagicMock()
        gui.signInFrame.place_forget = MagicMock()
        gui.editCelebrityFrame.pack_forget = MagicMock()  # Use pack_forget()
        gui.celebrityFrame.pack_forget = MagicMock()
        gui.filterFrame.pack_forget = MagicMock()

    def test_hide_all_frames(self):
        """Test if hideAllFrames correctly hides all frames."""
        gui.hideAllFrames()
        
        gui.mainFrame.pack_forget.assert_called_once()
        gui.signInFrame.place_forget.assert_called_once()
        gui.editCelebrityFrame.pack_forget.assert_called_once()  # Corrected method
        gui.celebrityFrame.pack_forget.assert_called_once()
        gui.filterFrame.pack_forget.assert_called_once()

    def test_app_initialization(self):
        """Ensure the application initializes with the correct properties."""
        self.assertEqual(gui.app.wm_title(), "TERNOPS - Celebrity Bio Application")

if __name__ == "__main__":
    unittest.main()
