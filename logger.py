from pathlib import Path
from log import Logger


_FILENAME = "log.md"
_DIR = Path("logs")


logger = Logger()
logger.createLog(_DIR, _FILENAME)
