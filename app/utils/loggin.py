import logging

def setup_logging():
    # Define the logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure the logging
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler()  # Output logs to the console
        ]
    )
    
    # Get the root logger
    logger = logging.getLogger("app")
    return logger
