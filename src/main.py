from business_assistant.config.logging import get_logger

# Get a logger for the main module
# This uses the singleton pattern - only one logger per name will be created
# across the entire application
logger = get_logger(__name__)

def main():
    logger.info('Hello, World!')


if __name__ == "__main__":
    main()
