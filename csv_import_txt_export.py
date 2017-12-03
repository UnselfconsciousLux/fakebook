import csv
import sys
files = []
for i in range(len(files)):
    file_name_output = files[i] + '.txt'
    try:
        output_file = open(file_name_output, 'w')  # Open the file for writing
    except IOError:  # ERROR!
        sys.exit(1)
    with open((files[i] + '.csv'), 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            output_file.write(row)
        output_file.close()