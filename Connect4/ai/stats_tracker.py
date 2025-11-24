import time

class AlgorithmStats:
    """Tracks statistics for algorithm execution"""
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.nodes_expanded = 0
        self.nodes_pruned = 0
        self.start_time = None
        self.end_time = None
        self.execution_time = 0
    
    def start_timer(self):
        self.start_time = time.time()
    
    def stop_timer(self):
        self.end_time = time.time()
        self.execution_time = self.end_time - self.start_time
    
    def increment_nodes(self):
        self.nodes_expanded += 1
    
    def increment_pruned(self):
        self.nodes_pruned += 1
    
    def get_stats(self):
        return {
            'nodes_expanded': self.nodes_expanded,
            'nodes_pruned': self.nodes_pruned,
            'execution_time': self.execution_time,
            'nodes_per_second': self.nodes_expanded / self.execution_time if self.execution_time > 0 else 0
        }

# Global stats tracker
stats = AlgorithmStats()