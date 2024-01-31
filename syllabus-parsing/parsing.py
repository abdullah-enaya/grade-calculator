import json
import pypdf
import os
import regex

# strings = ["Assignment", "Class Participation", "Quiz", "Final Exam", "Term Test", "Other", "Presentations"]  ?

directory = 'syllabi'

out_final = {"session": "Winter 2024", "courses": []}

for entry in os.scandir(directory):
    filepath = entry.path
    if filepath.endswith(".pdf"):
        pdf_reader = pypdf.PdfReader(filepath)

        whole_text = '\n'.join(page.extract_text() for page in pdf_reader.pages)

        # NICE ones:

        # match = re.findall('Type\nDescription\nDue Date\nWeight(?s:.)*Total\n100%', first_three_pages)

        try:
            # match3 = regex.findall('(?:\n.*){3}\n[0-9|.]+%', whole_text, overlapped=True)

            match_string = \
                r'(?m)(?<=^Type\nDescription\nDue Date\nWeight\n(?s:.)*)' \
                r'^(?:Lab|Assignment|Class Participation|Quiz|Final Exam|Term Test|Other|Presentations)\n' \
                r'(?s:.)*?' \
                r'^\d+\.?\d*%\n' \
                r'(?=(?s:.)*^Total\n100%$)'

            # match_string = \
            #     r'(?m)(?<=Type(?s:.)*)' \
            #     r'(?:Lab|Assignment|Class Participation|Quiz|Final Exam|Term Test|Other|Presentations)\n' \
            #     r'(?s:.)*?' \
            #     r'^\d+\.?\d*%\n'

            match4 = regex.findall(match_string, whole_text)

            table4: list[list[str]] = []
            for item in match4:
                table4.append(item.strip().split('\n'))

            # type_index = table2[0].index('Type')
            # description_index = table2[0].index('Description')
            # due_date_index = table2[0].index('Due Date')
            # weight_index = table2[0].index('Weight')

            out = {'courseName': filepath.split("/")[-1].strip(".pdf"), 'assignments': []}

            print(len(table4))
            if len(table4) == 0:
                print(filepath + " has no matches.")
                print(whole_text)
                continue

            total_weight = 0
            for row in table4:
                # row[0] contains the generic name, row[-1] contains the weight, row [-2] MIGHT contain the date,
                # row[1:-2] might contain description. so length at least 2?
                assert len(row) >= 2

                weight = float(row[-1][:-1]) / 100
                total_weight += weight
                if len(row) == 2:
                    name = row[0]
                elif regex.match(r'\d{4}-\d{2}-\d{2}|On-going|TBA', row[-2]):
                    print(row[-2] + ' is a date')
                    assert len(row) >= 3
                    generic_name = row[0]
                    other = ' '.join(row[1:-2])
                    name = generic_name + ": " + other
                else:
                    print(row[-2] + ' is NOT a date')
                    generic_name = row[0]
                    
                    other = ' '.join(row[1:-1])
                    name = generic_name + ": " + other

                entry = {"name": name, "weight": weight}
                out['assignments'].append(entry)
            if not 0.99 <= total_weight <= 1.01:
                print(f"{out['courseName']} had weight {total_weight}")
                print(out)
                print(whole_text)

        except Exception as e:
            print(e.__str__() + ": " + filepath)
            continue

        out_final["courses"].append(out)

        json_object = json.dumps(out, indent=4)

        with open('syllabi_json/' + out['courseName'] + '.json', "w") as outfile:
            outfile.write(json_object)


json_object2 = json.dumps(out_final, indent=4)

with open('all_syllabi.json', "w") as outfile:
    outfile.write(json_object2)
