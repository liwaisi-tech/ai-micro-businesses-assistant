from unittest.mock import patch, mock_open
import datetime
import re
from src.business_assistant.prompts.prompts import _read_prompt_template_file, default_prompt, _get_prompt_template, get_prompt


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
            
    def test_get_prompt_template_with_coder(self):
        """Test _get_prompt_template with the coder template.
        
        It should replace the template variables with their values.
        """
        # Create a test template with multiple variables
        test_template = """
---
CURRENT_TIME: {{ CURRENT_TIME }}
USER_NAME: {{ USER_NAME }}
BUSINESS_TYPE: {{ BUSINESS_TYPE }}
---

You are a professional software engineer proficient in both Python and bash scripting. Your task is to analyze requirements, implement efficient solutions using Python and/or bash, and provide clear documentation of your methodology and results.
"""
        
        # Create a TypedDict for values with custom variables
        values = {
            "USER_NAME": "John Doe",
            "BUSINESS_TYPE": "Bakery"
        }
        
        # Call the function
        result = _get_prompt_template(test_template, values)
        
        # Check that all placeholders are gone
        assert "{{ CURRENT_TIME }}" not in result
        assert "{{ USER_NAME }}" not in result
        assert "{{ BUSINESS_TYPE }}" not in result
        
        # Check that our custom values were inserted
        assert "USER_NAME: John Doe" in result
        assert "BUSINESS_TYPE: Bakery" in result
        
        # Check that some time value was inserted (without validating the exact time)
        assert re.search(r'CURRENT_TIME: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', result) is not None
