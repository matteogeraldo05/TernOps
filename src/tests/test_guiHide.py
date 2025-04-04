import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
import unittest
from unittest.mock import MagicMock
import customtkinter as ctk
import gui

class TestGUI(unittest.TestCase):

    def setUp(self):
        # initialize GUI at start of each test
        gui.app = ctk.CTk()
        gui.app.title("TERNOPS - Celebrity Bio Application")

        # Initialize actual frames to prevent NoneType issues
        gui.mainFrame = ctk.CTkFrame(gui.app)
        gui.signInFrame = ctk.CTkFrame(gui.app)
        gui.editCelebrityFrame = ctk.CTkFrame(gui.app)
        gui.celebrityFrame = ctk.CTkFrame(gui.app)
        gui.filterFrame = ctk.CTkFrame(gui.app)

        # Mock frame hiding methods
        gui.mainFrame.pack_forget = MagicMock()
        gui.signInFrame.place_forget = MagicMock()
        gui.editCelebrityFrame.pack_forget = MagicMock() 
        gui.celebrityFrame.pack_forget = MagicMock()
        gui.filterFrame.pack_forget = MagicMock()

    def test_hide_all_frames(self):
        # UT-21-OB: Test hiding frames functuon
        gui.hideAllFrames()
        
        gui.mainFrame.pack_forget.assert_called_once()
        gui.signInFrame.place_forget.assert_called_once()
        gui.editCelebrityFrame.pack_forget.assert_called_once()
        gui.celebrityFrame.pack_forget.assert_called_once()
        gui.filterFrame.pack_forget.assert_called_once()

    def test_app_initialization(self):
        # UT-22-OB: Test Initialization
        self.assertEqual(gui.app.wm_title(), "TERNOPS - Celebrity Bio Application")

if __name__ == "__main__":
    unittest.main()
