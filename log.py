from pathlib import Path
import logging


DEFAULT_LOG_DIR_PATH = 'logs'
DEFAULT_LOG_FILENAME = 'app.log'
DEFAULT_DATE_FORMAT = '%d-%b-%y %H:%M'
DEFAULT_LOG_FORMAT = '[%(asctime)s] -> %(name)s -> [%(levelname)s]: %(message)s'
DEFAULT_LOG_MODE = 'a'


class Logger:
    def __init__(self, dateFormat=DEFAULT_DATE_FORMAT, logFormat=DEFAULT_LOG_FORMAT, mode=DEFAULT_LOG_MODE):
        self._dir = None
        self._filename = None
        self._dateFormat = dateFormat
        self._logFormat = logFormat
        self._mode = mode

    def createLog(self, dir=DEFAULT_LOG_DIR_PATH, filename=DEFAULT_LOG_FILENAME):
        self._dir = Path(dir)
        self._dir.mkdir(exist_ok=True)
        self._filename = filename

    def setLogFile(self, filename):
        self._filename = filename

    def setDateFormat(self, dateFormat):
        self._dateFormat = dateFormat

    def setLogFormat(self, logFormat):
        self._logFormat = logFormat

    def setLogMode(self, mode):
        self._mode = mode

    def _getFileHandler(self):
        fileHandler = logging.FileHandler(self._dir / self._filename, encoding='utf-8', mode=self._mode)
        formatter = logging.Formatter(self._logFormat, self._dateFormat)
        fileHandler.setFormatter(formatter)
        return fileHandler

    def getLogger(self, loggerName):
        logger = logging.getLogger(loggerName)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self._getFileHandler())
        return logger


logger = Logger()
