import cProfile
from game import main

profiler = cProfile.Profile()
profiler.enable()
main(True)
profiler.disable()
profiler.print_stats(sort='cumtime')
