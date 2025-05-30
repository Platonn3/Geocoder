import unittest


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromName('test_database'))
    # suite.addTests(loader.loadTestsFromName('test_help'))
    suite.addTests(loader.loadTestsFromName('test_parsing'))
    suite.addTests(loader.loadTestsFromName('test_requests'))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    run_tests()