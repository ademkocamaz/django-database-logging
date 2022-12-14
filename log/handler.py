import logging
from .models import Log

db_default_formatter = logging.Formatter()

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        
        trace = None

        if record.exc_info:
            trace = db_default_formatter.formatException(record.exc_info)

        msg = record.getMessage()

        kwargs = {
            'logger_name': record.name,
            'level': record.levelno,
            'msg': msg,
            'trace': trace
        }

        Log.objects.create(**kwargs)

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = db_default_formatter

        if type(fmt) == logging.Formatter:
            record.message = record.getMessage()

            if fmt.usesTime():
                record.asctime = fmt.formatTime(record, fmt.datefmt)

            return fmt.formatMessage(record)
        else:
            return fmt.format(record)
