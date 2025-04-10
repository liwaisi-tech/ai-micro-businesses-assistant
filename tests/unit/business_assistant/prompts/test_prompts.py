from unittest.mock import patch, mock_open
from src.business_assistant.prompts.prompts import _read_prompt_template_file, default_prompt, _get_prompt_template


class TestPrompts:
    """Test class for the prompts module."""

    def test_read_prompt_template_file_not_found(self):
        """Test _read_prompt_template_file when the file doesn't exist.
        
        It should return the default prompt processed through _get_prompt_template.
        """
        # Test with a non-existent file
        non_existent_file = "non_existent_file.md"
        
        # Mock the open function to raise FileNotFoundError
        with patch("builtins.open", side_effect=FileNotFoundError):
            # Also patch _get_prompt_template to return a known value for verification
            with patch("src.business_assistant.prompts.prompts._get_prompt_template", return_value=default_prompt):
                result = _read_prompt_template_file(non_existent_file)
                
                # Verify the result is the default prompt
                assert result == default_prompt
    
    def test_read_prompt_template_file_exists(self):
        """Test _read_prompt_template_file when the file exists.
        
        It should return the content of the file.
        """
        # Test with an existing file
        file_content = "This is a test prompt template"
        test_file = "test_file.md"
        
        # Mock the open function to return our test content
        with patch("builtins.open", mock_open(read_data=file_content)):
            result = _read_prompt_template_file(test_file)
            
            # Verify the result is the file content
            assert result == file_content
