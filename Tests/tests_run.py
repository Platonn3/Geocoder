import unittest
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements"])


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromName('Tests.test_database'))
    suite.addTests(loader.loadTestsFromName('Tests.test_help'))
    suite.addTests(loader.loadTestsFromName('Tests.test_parsing'))
    suite.addTests(loader.loadTestsFromName('Tests.test_requests'))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    run_tests()