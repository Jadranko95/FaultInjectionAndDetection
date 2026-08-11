import os
from unittest.mock import patch
from src.utils.utils import get_env_variable


class TestGetEnvVariable:
    def test_returns_env_variable_when_exists(self):
        """Test that function returns the correct value when env variable exists."""
        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            result = get_env_variable("TEST_VAR")
            assert result == "test_value"

    def test_returns_none_when_env_variable_not_exists(self):
        """Test that function returns None when env variable doesn't exist."""
        with patch.dict(os.environ, {}, clear=False):
            if "NON_EXISTENT_VAR" in os.environ:
                del os.environ["NON_EXISTENT_VAR"]
            result = get_env_variable("NON_EXISTENT_VAR")
            assert result is None

    def test_prints_error_when_env_variable_not_exists(self, capsys):
        """Test that function prints error message when env variable doesn't exist."""
        with patch.dict(os.environ, {}, clear=False):
            if "NON_EXISTENT_VAR" in os.environ:
                del os.environ["NON_EXISTENT_VAR"]
            get_env_variable("NON_EXISTENT_VAR")
            captured = capsys.readouterr()
            assert "The environment variable NON_EXISTENT_VAR was not found." in captured.out

    def test_with_empty_string_variable(self):
        """Test that function returns empty string when env variable is empty."""
        with patch.dict(os.environ, {"EMPTY_VAR": ""}):
            result = get_env_variable("EMPTY_VAR")
            assert result == ""

    def test_with_special_characters_in_variable(self):
        """Test that function correctly handles special characters."""
        special_value = "test@#$%^&*()value"
        with patch.dict(os.environ, {"SPECIAL_VAR": special_value}):
            result = get_env_variable("SPECIAL_VAR")
            assert result == special_value
