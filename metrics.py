# metrics.py
import time
from collections import defaultdict

class Metrics:
    def __init__(self):
        self.node_counts = defaultdict(int)   # per-key call counts
        self.prune_counts = defaultdict(int)  # (used by alpha-beta, harmless here)
        self.move_times = []                  # list of per-move durations (sec)

    def reset(self):
        self.node_counts.clear()
        self.prune_counts.clear()
        self.move_times.clear()

    def inc(self, key: str):
        self.node_counts[key] += 1

    def inc_prune(self, key: str):
        self.prune_counts[key] += 1

    # Usage:
    #   end = METRICS.time_block()
    #   ... do work ...
    #   end()
    def time_block(self):
        start = time.perf_counter()
        def _end():
            self.move_times.append(time.perf_counter() - start)
        return _end

METRICS = Metrics()

def count_nodes(key: str):
    """Decorator: increments a node counter every call to the wrapped function."""
    def _deco(fn):
        def _wrapper(*args, **kwargs):
            METRICS.inc(key)
            return fn(*args, **kwargs)
        return _wrapper
    return _deco
