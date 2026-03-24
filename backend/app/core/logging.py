import logging
import json
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Format log records as JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        # Add custom context fields if present
        for attr in ['user_id', 'project_id', 'operation', 'duration_ms']:
            if hasattr(record, attr):
                log_data[attr] = getattr(record, attr)
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Configure structured JSON logging"""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger("thistory")
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    return logger


def log_with_context(logger: logging.Logger, level: int, message: str, **kwargs):
    """Log a message with additional context"""
    extra = {k: v for k, v in kwargs.items()}
    logger.log(level, message, extra=extra)
