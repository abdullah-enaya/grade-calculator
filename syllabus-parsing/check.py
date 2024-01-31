import json
import pypdf
import os
import regex

directory = 'syllabi'

with open('all_syllabi.json', "r") as infile:
    data = infile.read()

data = json.loads(data)

for course in data['courses']:
    total_weight = 0
    for assignment in course['assignments']:
        total_weight += float(assignment['weight'])
    if not 0.99 <= total_weight <= 1.01:
        print(f"{course['courseName']} had weight {total_weight}")
