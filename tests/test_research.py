#!/usr/bin/env python3
"""
Tests for the Clauducky Research Script
"""
import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.python.research import research_with_openai, research_with_anthropic

class TestResearchScript(unittest.TestCase):
    """Tests for the research.py script"""
    
    @patch('scripts.python.research.OpenAI')
    def test_research_with_openai(self, mock_openai):
        """Test the OpenAI research function with a mocked client"""
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response from OpenAI"
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test with environment variable
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
            result = research_with_openai("Test query")
            
            # Assertions
            self.assertIn("result", result)
            self.assertEqual(result["result"], "Test response from OpenAI")
            self.assertEqual(result["provider"], "openai")
            self.assertEqual(result["model"], "gpt-4o")
    
    @patch('scripts.python.research.Anthropic')
    def test_research_with_anthropic(self, mock_anthropic):
        """Test the Anthropic research function with a mocked client"""
        # Setup mock
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        
        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = "Test response from Anthropic"
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response
        
        # Test with environment variable
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test_key'}):
            result = research_with_anthropic("Test query")
            
            # Assertions
            self.assertIn("result", result)
            self.assertEqual(result["result"], "Test response from Anthropic")
            self.assertEqual(result["provider"], "anthropic")
            self.assertEqual(result["model"], "claude-3-haiku-20240307")
    
    def test_openai_missing_api_key(self):
        """Test the OpenAI research function with missing API key"""
        # Ensure environment variable is not set
        with patch.dict('os.environ', {}, clear=True):
            result = research_with_openai("Test query")
            
            # Assertions
            self.assertIn("error", result)
            self.assertEqual(result["error"], "OPENAI_API_KEY environment variable not set")
    
    def test_anthropic_missing_api_key(self):
        """Test the Anthropic research function with missing API key"""
        # Ensure environment variable is not set
        with patch.dict('os.environ', {}, clear=True):
            result = research_with_anthropic("Test query")
            
            # Assertions
            self.assertIn("error", result)
            self.assertEqual(result["error"], "ANTHROPIC_API_KEY environment variable not set")

if __name__ == '__main__':
    unittest.main()