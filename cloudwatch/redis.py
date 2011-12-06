import redis
from cloudwatch import CloudWatchPlugin
from datetime import datetime

class RedisQueuePlugin(CloudWatchPlugin):
    def __init__(self, *args, **kwargs):
        self.redis = redis.Redis()
        self.queues = args
        super().__init__(**kwargs)
    
    def run(self):
        for queue in self.queues:
            self.put('RedisQueueSize', self.redis.llen(queue), 'Count')
