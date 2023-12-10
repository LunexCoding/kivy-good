from kivy.utils import platform

from app import MyApp
from logger import logger


_log = logger.getLogger(__name__)

if platform == "android":
     from android.permissions import request_permissions, Permission
     request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])


if __name__ == '__main__':
    try:
        MyApp().run()
    except Exception as e:
        _log.error(e)
