import unittest

import test_help
import test_parsing
import test_requests

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(test_help))
    suite.addTests(loader.loadTestsFromModule(test_parsing))
    suite.addTests(loader.loadTestsFromModule(test_requests))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)