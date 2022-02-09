import xmlrunner
import unittest
import sys
import getopt


def main(argv):
    """
    Script to run the unit-tests in the is repository in a "discover mode"

    The unit-tests are automatically discovered recursively starting from the specified
    directory for every module. The test files must have names matching pattern specified
    when executing this script. The results of the test are stored as XML files in the
    sub-directory ('/test-reports') of the package holding the module.

    Parameters
    ----------
    argv : list
        List of flagged arguments all of which are optional
        -d <directory>
        Path to the directory which is the root of all the tests.
        Defaults to current directory.
        -p <pattern>
        File name pattern using wild cards (example: tests*.py)
        Defaults to '*_tests.py'

    Returns
    -------
    result : int
        0 - when all tests successfully passed
        1 - when one or more tests have failed

    """

    # Get the arguments
    # usage: test_runner.py -d path/to/input/folder -p search-pattern
    opts, _ = getopt.getopt(argv, 'd:p:')

    # default values for the arguments when they are not specified
    base_dir = './'
    test_dir = ''
    pattern = 'test_*'
    # pattern = '*_tests.py'

    for opt, arg in opts:
        if opt == '-d':
            test_dir = arg
        elif opt == '-p':
            pattern = arg

    output_dir = base_dir + test_dir + '/test-reports'

    input_dir = base_dir + test_dir
    print('11111111', output_dir)
    tests = unittest.TestLoader().discover(input_dir, pattern)
    result = xmlrunner.XMLTestRunner(output=output_dir).run(tests)

    return result.wasSuccessful()


if __name__ == '__main__':
    result = main(sys.argv[1:])
    sys.exit(not result)