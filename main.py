import json
from xml_processor import parse_xml
from converter import convert_raw_question_to_data
from xml_generator import generate_xml

raw_question_list = parse_xml("data.xml")

processed_question_list = []

for raw_question in raw_question_list:
    processed_question = convert_raw_question_to_data(raw_question)
    if processed_question and " - " in processed_question["title"]:
        number = int(processed_question["title"].split(" - ")[1].split("No. ")[1])
        processed_question["number"] = number
        processed_question_list.append(processed_question)
    else:
        print("Invalid title: ", raw_question["title"])

print("Processed questions: ", len(processed_question_list))

grouped_questions = {}

for processed_question in processed_question_list:
    title = processed_question["title"].split(" - ")[0].strip().replace("  ", " ")
    if title not in grouped_questions:
        grouped_questions[title] = []
    grouped_questions[title].append(processed_question)

for title in grouped_questions:
    grouped_questions[title] = sorted(grouped_questions[title], key=lambda x: x["number"])

# normalized number start from 1
for title in grouped_questions:
    for index, question in enumerate(grouped_questions[title]):
        question["number"] = index + 1

# count question for each title

# sort title
sorted_titles = sorted(grouped_questions.keys(), key=lambda x: x.split(" ")[0])
for title in sorted_titles:
    print(f'{title}\t:', len(grouped_questions[title]))

print("Total questions: ", len(processed_question_list))


    
with open("data.json", "w") as f:
    json.dump(grouped_questions, f, indent=4, sort_keys=True)

for title in grouped_questions:
    generate_xml(grouped_questions[title], title)
