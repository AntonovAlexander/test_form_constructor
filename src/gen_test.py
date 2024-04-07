# -*- coding:utf-8 -*-
from __future__ import division
import csv
import shutil

import example_test
from example_test import *

test_name = "example_test1"
printable_test_name = "Example test for demonstration of library functions"
dir_name = "example_test"

with open('group_info.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file, delimiter=';')

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Process each row
        print("Generating test:: ID: " + row[0] + ", Name: " + row[1])
        testgen = example_test(test_name, printable_test_name, row[0], row[1])
        testgen.writeFiles(dir_name)

shutil.copyfile("FileSaver.js", dir_name + "/forms/FileSaver.js")
