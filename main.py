import sys
import classes
import argparse

def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Debugging output')
    parser.add_argument('-p', '--patient_name', dest='patient_name',
            type=str, help='The name of a patient', default='John Doe')
    return vars(parser.parse_args())

if __name__ == '__main__':
    args = initialize_argument_parser()
    print 'Hello world'
    print 'Your current version is', sys.version
    print 'Your current version should be 2.7.6'
    print "Let's get started, shall we?"
    print "First baby steps in the New World"
    print "Emilie"
    print "second test"
    database = classes.Database()
    print 'patient info: ', database.get_patient_info(args['patient_name'])
