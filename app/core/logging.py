"""
Logging configuration for the application.
Provides setup for different loggers and handlers.
"""
import logging
import logging.handlers
from pathlib import Path
from app.core.config import get_config

def setup_logger(name, log_file=None):
    """
    Set up a logger with the specified name and optional log file.
    If no log file is specified, logs will go to the default location based on config.
    
    Args:
        name (str): Name of the logger
        log_file (str, optional): Path to the log file. Defaults to None.
        
    Returns:
        logging.Logger: Configured logger
    """
    config = get_config()
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Create formatters
    formatter = logging.Formatter(
        fmt=config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
    )
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log_file is specified or we're not in testing mode
    if not config.TESTING:
        if log_file is None:
            # Use default log file in logs directory
            log_file = config.LOGS_DIR / f"{name}.log"
        else:
            log_file = Path(log_file)
        
        # Create log directory if it doesn't exist
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Set up rotating file handler
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=log_file,
            when='midnight',
            interval=1,
            backupCount=config.LOG_RETENTION_DAYS,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Set up root logger with basic configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create loggers for different components
scraper_logger = setup_logger('scraper')
model_logger = setup_logger('model')
analysis_logger = setup_logger('analysis')
api_logger = setup_logger('api') 