import xml.dom.minidom as minidom

# parse an XML file by name

def parse_xml(fileName):
    doc = minidom.parse(fileName)

    raw_questions = []

    failed_questions = 0

    # iterate over all the question
    questions = doc.getElementsByTagName("post")

    print("Total raw questions: ", len(questions))
    for question in questions:
        raw_question = question.getElementsByTagName("vibe_question_json")[0]
        title = question.getElementsByTagName("Title")[0]

        try:
            question_obj = {
                "title": title.firstChild.data,
                "raw_question": raw_question.firstChild.data
            }
            raw_questions.append(question_obj)
        except:
            print("Failed to parse question: ", title.firstChild.data)
            failed_questions += 1
            pass

    print("Parsed questions: ", len(raw_questions))
    print("Failed questions: ", failed_questions)

    return raw_questions

        