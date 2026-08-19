import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger("netautolab")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(log_format)
    logger.addHandler(ch)
    
    # File handler
    fh = RotatingFileHandler(
        log_dir / "application.log", 
        maxBytes=5*1024*1024, 
        backupCount=5
    )
    fh.setFormatter(log_format)
    logger.addHandler(fh)
    
    return logger

logger = setup_logging()
