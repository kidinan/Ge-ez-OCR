import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("app")

try:
    # Setup code here
    logger.info("Entering the block")
    
    # Your main code here
    logger.info("Inside the block")
    
    # You can raise an exception to see how it's handled
    raise ValueError("Something went wrong")
    
except Exception as e:
    # Teardown code here (exception handling)
    logger.error(f"An exception occurred: {e}")
finally:
    # Teardown code here (always runs)
    logger.info("Exiting the block")
