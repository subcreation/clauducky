#!/usr/bin/env python3
"""
Tests for the Clauducky Ducky Debug Script
"""
import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import scripts.python.ducky_debug
from scripts.python.ducky_debug import ducky_debug_openai, ducky_debug_anthropic

class TestDuckyDebugScript(unittest.TestCase):
    """Tests for the ducky_debug.py script"""
    
    def test_ducky_debug_openai(self):
        """Test the OpenAI ducky debug function with a mocked client"""
        # Create a mock for OpenAI class
        mock_openai = MagicMock()
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test debugging response from OpenAI"
        mock_client.chat.completions.create.return_value = mock_response
        
        # Patch the OpenAI global in the module
        with patch.object(scripts.python.ducky_debug, 'OpenAI', mock_openai):
            # Test with environment variable
            with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
                result = ducky_debug_openai(
                    problem="Test error message", 
                    code="console.log(x)",
                    expected="Console should show the value of x",
                    detailed=True
                )
            
            # Assertions
            self.assertIn("result", result)
            self.assertEqual(result["result"], "Test debugging response from OpenAI")
            self.assertEqual(result["provider"], "openai")
            self.assertEqual(result["model"], "gpt-4o")
    
    def test_ducky_debug_anthropic(self):
        """Test the Anthropic ducky debug function with a mocked client"""
        # Create a mock for Anthropic class
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = "Test debugging response from Anthropic"
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response
        
        # Patch the Anthropic global in the module
        with patch.object(scripts.python.ducky_debug, 'Anthropic', mock_anthropic):
            # Test with environment variable
            with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
                result = ducky_debug_anthropic(
                    problem="Test error message", 
                    code="console.log(x)",
                    expected="Console should show the value of x",
                    detailed=True
                )
            
            # Assertions
            self.assertIn("result", result)
            self.assertEqual(result["result"], "Test debugging response from Anthropic")
            self.assertEqual(result["provider"], "anthropic")
            self.assertEqual(result["model"], "claude-3-haiku-20240307")
    
    def test_openai_missing_api_key(self):
        """Test the OpenAI ducky debug function with missing API key"""
        # We need to ensure OpenAI module is available but API key is missing
        mock_openai = MagicMock()
        
        # Patch OpenAI and clear environment variables
        with patch.object(scripts.python.ducky_debug, 'OpenAI', mock_openai):
            with patch.dict('os.environ', {}, clear=True):
                result = ducky_debug_openai("Test error message")
                
                # Assertions
                self.assertIn("error", result)
                self.assertEqual(result["error"], "OPENAI_API_KEY environment variable not set")
    
    def test_anthropic_missing_api_key(self):
        """Test the Anthropic ducky debug function with missing API key"""
        # We need to ensure Anthropic module is available but API key is missing  
        mock_anthropic = MagicMock()
        
        # Patch Anthropic and clear environment variables
        with patch.object(scripts.python.ducky_debug, 'Anthropic', mock_anthropic):
            with patch.dict('os.environ', {}, clear=True):
                result = ducky_debug_anthropic("Test error message")
                
                # Assertions
                self.assertIn("error", result)
                self.assertEqual(result["error"], "ANTHROPIC_API_KEY environment variable not set")

if __name__ == '__main__':
    unittest.main()