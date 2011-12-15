from boto import connect_cloudwatch, connect_ec2
from datetime import datetime
import requests

UNITS = (
    'Seconds',
    'Microseconds',
    'Milliseconds',
    'Bytes',
    'Kilobytes',
    'Megabytes',
    'Gigabytes',
    'Terabytes',
    'Bits',
    'Kilobits',
    'Megabits',
    'Gigabits',
    'Terabits',
    'Percent',
    'Count',
    'Bytes/Second',
    'Kilobytes/Second',
    'Megabytes/Second',
    'Gigabytes/Second',
    'Terabytes/Second',
    'Bits/Second',
    'Kilobits/Second',
    'Megabits/Second',
    'Gigabits/Second',
    'Terabits/Second',
    'Count/Second',
    'None',
)

class CloudWatchPlugin(object):
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, namespace='EC2+', dimensions=None):
        self.conn = connect_cloudwatch(aws_access_key_id, aws_secret_access_key)
        self.namespace = namespace
        self.dimensions = dimensions or {}
        self.dimensions.update(self.get_instance_dimensions())
        print 'Init plugin with InstanceId: ' + str(self.dimensions.get('InstanceId', 'Unknown'))

    def get_instance_dimensions(self):
        dimensions = {}
        instance_id = self.get_instance_id()
        if instance_id:
            dimensions['InstanceId'] = instance_id
        return dimensions

    def get_instance_id(self):
        try:
            return requests.get('http://169.254.169.254/latest/meta-data/instance-id', timeout=1).content
        except Exception:
            return None
        
    def run(self):
        pass

    def put(self, name, value, unit, timestamp=None):
        timestamp = timestamp or datetime.utcnow()
        self.conn.put_metric_data(self.namespace, name, value, timestamp, unit, self.dimensions)
