from cloudwatch import CloudWatchPlugin
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

class VerticaPlugin(CloudWatchPlugin):
    RESOURCES_QUERY = ('select * from monitor.resources '
                       'where node_name = (select node_name from current_session)')
    
    def __init__(self, database, username='dbadmin', password='', *args, **kwargs):
        self.vsql = '/opt/vertica/bin/vsql'
        self.database = database
        self.username = username
        self.password = password
    
    def run(self):
        resources = self.run_vsql(self.RESOURCES_QUERY)[0]
        
        # memory
        mem_total = float(resources['memory_total_mb'])
        mem_inuse = float(resources['memory_inuse_mb'])
        self.put('VerticaMemoryReserved', [mem_inuse, mem_inuse/mem_total], ['Megabytes', 'Percent'])
        
        # threads
        thread_limit = float(resources['thread_limit'])
        thread_count = float(resources['thread_count'])
        self.put('VerticaThreads', [thread_count, thread_count/thread_limit], ['Count', 'Percent'])

        open_file_limit = float(resources['open_file_limit'])
        open_file_count = float(resources['open_file_count'])
        self.put('VerticaOpenFileHandles', [open_file_count, open_file_count/open_file_limit], ['Count', 'Percent'])
        
        
    def run_vsql(query):
        args = [
            self.vsql,
            '-d', self.database,
            '-U', self.username,
            '-w', self.password,
            '-c', query,
            '-Pfooter' # disable row count
            '-A', '-F', '\t' # unaligned, tab delimited
        ]
        p = Popen(args, stdout=PIPE, stderr=STDOUT)
        (stdout, stderr) = p.communicate()
        rows = [ x.split('\t') for x in stdout.splitlines() ]
        return [ dict(zip(rows[0], row)) for row in rows[1:] ]

