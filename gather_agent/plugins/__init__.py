#!python
from conf.config import use_plugins
import importlib

class plugins_manager(object):
    def process(self):
        data = {}
        for plugin in use_plugins:
            module = importlib.import_module(f'plugins.{plugin}')
            cls = getattr(module, f'gather_{plugin}')
            data[plugin] = cls().start()
        print(data)
