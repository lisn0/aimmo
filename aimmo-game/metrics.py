from prometheus_client import Histogram, Gauge, Summary, Counter
import os

# This files contains the definitions of all the custom metrics we currently measure.
# Any new metrics needed should be stored here. In addition, when dealing with async code
# you should use the context manager approach instead of decorators. When using the metrics
# as decoraters do not function properly with async code.

# Do not use a metric more than once, it will probably break them. If you need to measure
# something in a similar or the same way as an existing metric, create a new one.

# Measures the time taken for the game to go through an entire turn (game runner's update method)
def GAME_TURN_PROCESSING_SECONDS():
    """ Used for measuring the time it games for the game to complete a turn. This is stored
        on a Histogram with values 1 to 5 +infinity going in steps of 0.1. """
    CUSTOM_BUCKET = [x/10 for x in range(10,51)]
    GAME_TURN_PROCESSING = Histogram('function_exec_time', 'Test metric to see if we can time a functions execution',
                        buckets=CUSTOM_BUCKET,
                        labelnames=('game_id'))
    return GAME_TURN_PROCESSING.labels('{}'.format(os.environ['GAME_ID']))