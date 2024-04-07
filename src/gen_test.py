# -*- coding:utf-8 -*-
from __future__ import division
import csv

import example_test
from example_test import *

with open('group_info.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file, delimiter=';')

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Process each row
        print("Generating test:: ID: " + row[0] + ", Name: " + row[1])
        testgen = example_test("test1", row[0], row[1])
        testgen.writeFiles("example_test")

