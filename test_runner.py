import unittest
import sys
import multiprocessing as mp
from concurrencytest import ConcurrentTestSuite, fork_for_tests

number_of_cpu_cores = (mp.cpu_count() - 1)

if __name__ == '__main__':
    # Change the pattern to match only the test file you want to run
    test_suite = unittest.TestLoader().discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    concurrent_suite = ConcurrentTestSuite(test_suite, fork_for_tests(number_of_cpu_cores))
    ret = not runner.run(concurrent_suite).wasSuccessful()
    sys.exit(ret)
