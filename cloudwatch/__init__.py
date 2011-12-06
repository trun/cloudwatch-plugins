from cloudwatch.plugin import CloudWatchPlugin
from cloudwatch.memory import MemoryPlugin
from cloudwatch.redis import RedisQueuePlugin
from cloudwatch.vertica import VerticaPlugin

__version__ = '0.9.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = [
    'CloudWatchPlugin',
    'MemoryPlugin',
    'RedisQueuePlugin',
    'VerticaPlugin',
]
