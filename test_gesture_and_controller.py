import pytest
from unittest.mock import MagicMock, patch
import mediapipe as mp
from keymotions.gesture_recognition import GestureRecognition
from keymotions.controller import Controller
from pynput.keyboard import Key

@pytest.fixture
def gesture_recognition():
    return GestureRecognition()

@pytest.fixture
def controller():
    return Controller()

class TestGestureRecognition:
    def test_has_recognized(self, gesture_recognition):
        assert not gesture_recognition.has_recognized()
        gesture_recognition.results = MagicMock()
        assert gesture_recognition.has_recognized()

class TestController:
    @patch('pynput.keyboard.Controller.press')
    def test_press_key(self, mock_press, controller):
        controller.press_key('a')
        mock_press.assert_called_once_with('a')
        assert controller.current_pressed_key == 'a'

    @patch('pynput.keyboard.Controller.release')
    def test_release_key(self, mock_release, controller):
        controller.current_pressed_key = 'b'
        controller.release_key()
        mock_release.assert_called_once_with('b')
        assert controller.current_pressed_key is None

    def test_is_pressing_key(self, controller):
        assert not controller.is_pressing_key()
        controller.current_pressed_key = Key.space
        assert controller.is_pressing_key()
