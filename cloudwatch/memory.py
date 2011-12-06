from cloudwatch.plugin import CloudWatchPlugin
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

class MemoryPlugin(CloudWatchPlugin):
    def run(self):
        output = self.run_free()
        lines = output.splitlines()
        total = float(lines[1].split()[1])
        used, free = map(int, lines[2].split()[2:4])
        
        self.put('PhysicalMemoryUsed', [used, used/total], ['Megabytes', 'Percent'])
        self.put('PhysicalMemoryFree', [free, free/total], ['Megabytes', 'Percent'])
        
    def run_free(self):
        p = Popen(['free','-m'], stdout=PIPE, stderr=STDOUT)
        (stdout, stderr) = p.communicate()
        return stdout

