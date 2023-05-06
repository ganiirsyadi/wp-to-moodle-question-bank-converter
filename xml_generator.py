from lxml import etree as ET
from bs4 import BeautifulSoup

test1 = {
      "type": "single",
      "hint": " ",
      "explanation": "",
      "original_content": "\n<p>Emission nebula, clouds of high temperature gas, are usually red because hydrogen, the most common gas in the universe, most commonly emits red light.</p>\n",
      "content": "\n<p>Emission nebula, clouds of high temperature gas, are usually red because hydrogen, the most common gas in the universe, most commonly emits red light.</p>\n",
      "options": ["high", "commonly emits", "because", "Nebula"],
      "correct": "4",
      "id": "21062",
      "title": "027 Grammar - No. 40",
      "number": 40
    }

test2 = {
      "type": "single",
      "hint": " ",
      "explanation": "",
      "original_content": "<div class=\"vibe_editor_media\"><img loading=\"lazy\" class=\"\" title=\"soal-41\" src=\"https://jelajahstudies.com/wp-content/uploads/2021/01/Soal-41.png\" width=\"504\" height=\"40\" /></div>\n",
      "content": "<div class=\"vibe_editor_media\"><img loading=\"lazy\" class=\"\" title=\"soal-41\" src=\"https://jelajahstudies.com/wp-content/uploads/2021/01/Soal-41.png\" width=\"504\" height=\"40\" /></div>\n",
      "options": [
        "<div class=\"vibe_editor_rich_text\"><p style=\"\">-3</p></div>",
        "<div class=\"vibe_editor_rich_text\"><p style=\"\">-2</p></div>",
        "<div class=\"vibe_editor_rich_text\"><p style=\"\">1</p></div>",
        "<div class=\"vibe_editor_rich_text\"><p style=\"\">2</p></div>",
        "<div class=\"vibe_editor_rich_text\"><p style=\"\">3</p></div>"
      ],
      "correct": "5",
      "id": "3171",
      "title": "Kuantitatif - No. 41",
      "number": 1
}

obj_list = {
    "questions": [test1, test2]
}

def is_html(content):
    return bool(BeautifulSoup(content, "html.parser").find())

def is_english(title):
    keywords = ["Reading", "Grammar", "Eng"]
    for keyword in keywords:
        if keyword in title:
            return True
    return False

def generate_xml(question_obj_list, group):
    document = ET.Element('quiz')
    et = ET.ElementTree(document)


    # category
    question_category = ET.SubElement(document, 'question')
    question_category.set('type', "category")

    category = ET.SubElement(question_category, 'category')
    category_text = ET.SubElement(category, 'text')
    category_text.text = group

    for question_obj in question_obj_list:
        english_question = is_english(question_obj['title'])

        question = ET.SubElement(document, 'question')
        question.set('type', "multichoice")

        name = ET.SubElement(question, 'name')
        text = ET.SubElement(name, 'text')
        text.text = question_obj['title']

        question_text = ET.SubElement(question, 'questiontext')
        question_text.set('format', "html")
        
        content = question_obj['content']

        question_text.text = ET.CDATA(content) if is_html(content) else content

        general_feedback = ET.SubElement(question, 'generalfeedback')
        general_feedback.set('format', "html")
        general_feedback.text = ET.CDATA("Feedback")
    
        default_grade = ET.SubElement(question, 'defaultgrade')
        default_grade.text = "1.0000000" if english_question else "4.0000000"

        penalty = ET.SubElement(question, 'penalty')
        penalty.text = "0.0000000"

        hidden = ET.SubElement(question, 'hidden')
        hidden.text = "0"

        idnumber = ET.SubElement(question, 'idnumber')
        idnumber.text = question_obj['id']

        single = ET.SubElement(question, 'single')
        single.text = "true"

        shuffleanswers = ET.SubElement(question, 'shuffleanswers')
        shuffleanswers.text = "false"

        answernumbering = ET.SubElement(question, 'answernumbering')
        answernumbering.text = "abc"

        showstandardinstruction = ET.SubElement(question, 'showstandardinstruction')
        showstandardinstruction.text = "0"

        correctfeedback = ET.SubElement(question, 'correctfeedback')
        correctfeedback.set('format', "html")
        correctfeedback.text = ET.CDATA("Answer is correct")

        partiallycorrectfeedback = ET.SubElement(question, 'partiallycorrectfeedback')
        partiallycorrectfeedback.set('format', "html")
        partiallycorrectfeedback.text = ET.CDATA("Answer is partially correct")

        incorrectfeedback = ET.SubElement(question, 'incorrectfeedback')
        incorrectfeedback.set('format', "html")
        incorrectfeedback.text = ET.CDATA("Answer is incorrect")

        ET.SubElement(question, 'shownumcorrect')

        incorrect_answer_point = "0" if english_question else "-25"
        correct_answer = int(question_obj['correct']) - 1 # 0 based index

        for i, option in enumerate(question_obj['options']):

            answer = ET.SubElement(question, 'answer')
            answer.set('fraction', incorrect_answer_point if i != correct_answer else "100")
            answer.set('format', "html")

            answer_text = ET.SubElement(answer, 'text')
            answer_text.text = ET.CDATA(option) if is_html(option) else option

            answer_feedback = ET.SubElement(answer, 'feedback')
            answer_feedback.set('format', "html")

            ET.SubElement(answer_feedback, 'text')

    et.write("./categories/" + group + ".xml", encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    key = "questions"
    generate_xml(obj_list[key], key)