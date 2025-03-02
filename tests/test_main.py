import unittest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import create_app


class TestMain(unittest.TestCase):
    """Test cases for the main.py module."""

    @patch('src.main.register_routes')
    def test_create_app(self, mock_register_routes):
        """Test that the create_app function returns a properly configured FastAPI instance."""
        # Arrange
        mock_register_routes.return_value = None
        
        # Act
        app = create_app()
        
        # Assert
        self.assertIsInstance(app, FastAPI)
        self.assertEqual(app.title, "AI Micro Businesses Assistant")
        self.assertEqual(app.description, "API for AI-powered assistant for micro businesses")
        self.assertEqual(app.version, "0.1.0")
        
        # Verify register_routes was called with the app instance
        mock_register_routes.assert_called_once()
        self.assertEqual(mock_register_routes.call_args[0][0], app)

    @patch('src.main.register_routes')
    def test_cors_middleware_configuration(self, mock_register_routes):
        """Test that CORS middleware is properly configured."""
        # Arrange
        mock_register_routes.return_value = None
        
        # Act
        app = create_app()
        client = TestClient(app)
        
        # Assert - Check if CORS middleware is added
        # This is a basic check that the middleware exists
        cors_middleware = None
        for middleware in app.user_middleware:
            if middleware.cls.__name__ == 'CORSMiddleware':
                cors_middleware = middleware
                break
        
        self.assertIsNotNone(cors_middleware)
        
        # Check CORS settings - Fix: Access the kwargs instead of options
        cors_config = middleware.kwargs
        self.assertEqual(cors_config['allow_origins'], ["*"])
        self.assertTrue(cors_config['allow_credentials'])
        self.assertEqual(cors_config['allow_methods'], ["*"])
        self.assertEqual(cors_config['allow_headers'], ["*"])

    def test_app_instance(self):
        """Test that the app instance is created correctly."""
        # Instead of trying to patch after the fact, we'll verify the app instance directly
        # Import the app instance
        from src.main import app
        
        # Assert that it's a FastAPI instance
        self.assertIsInstance(app, FastAPI)
        
        # We can't easily verify that register_routes was called since it happened during import
        # But we can verify that the app has the expected configuration
        self.assertEqual(app.title, "AI Micro Businesses Assistant")
        self.assertEqual(app.description, "API for AI-powered assistant for micro businesses")
        self.assertEqual(app.version, "0.1.0")
        
        # And we can verify that it has middleware configured
        has_cors_middleware = False
        for middleware in app.user_middleware:
            if middleware.cls.__name__ == 'CORSMiddleware':
                has_cors_middleware = True
                break
        
        self.assertTrue(has_cors_middleware, "App should have CORS middleware configured")


if __name__ == '__main__':
    unittest.main()
