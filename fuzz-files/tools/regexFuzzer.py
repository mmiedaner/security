import rstr
import argparse

parser = argparse.ArgumentParser(description='Create fuzzing strings based on regex.')
parser.add_argument('maxCycles', metavar='count', type=int, help='number of fuzzing strings to be generated')
parser.add_argument('--regex', metavar='regex', help='regular expression as string')
parser.add_argument('--out', metavar='file', help='file to write output to')
args = parser.parse_args()

target = open(args.out, 'w')

counter = 0
while (counter < args.maxCycles[0]):
    result = rstr.xeger(args.regex)
    print result
    target.write(result)
    target.write('\n')
    counter = counter+1

print 'Done!'
target.close()
