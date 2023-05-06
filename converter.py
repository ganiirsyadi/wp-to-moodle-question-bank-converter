import re
from bs4 import BeautifulSoup

KEYS = [
    "type",
    "hint",
    "explanation",
    "original_content",
    "content",
    "options",
    "correct",
    "id",
]
    
test = {
    "title": "020 Grammar - No. 2",
    "raw_question": """<![CDATA[a:7:{s:4:"type";s:6:"single";s:11:"explanation";s:0:"";s:16:"original_content";s:201:"<div class="vibe_editor_rich_text">
<p style="">Not until Grandma Moses, the famous painter of primitive an reached the age of 76 ………. her unique depictions of everyday life on a farm</p>
</div>
";s:7:"content";s:201:"<div class="vibe_editor_rich_text">
<p style="">Not until Grandma Moses, the famous painter of primitive an reached the age of 76 ………. her unique depictions of everyday life on a farm</p>
</div>
";s:7:"options";a:4:{i:0;s:75:"<div class="vibe_editor_rich_text"><p style="">she began to paint</p></div>";i:1;s:79:"<div class="vibe_editor_rich_text"><p style="">did she begin to paint</p></div>";i:2;s:78:"<div class="vibe_editor_rich_text"><p style="">as she began to paint</p></div>";i:3;s:74:"<div class="vibe_editor_rich_text"><p style="">to begin to paint</p></div>";}s:7:"correct";s:1:"2";s:2:"id";i:4627;}]]>"""
}

def convert_raw_question_to_data(question_raw_obj: object):
    SEPARATOR = "!@!@"

    try:
        title = question_raw_obj["title"]

        question_raw = question_raw_obj["raw_question"]
        question_raw_list = re.split("s:\d+:", question_raw)

        question_id = re.findall(r"\d+", question_raw_list[-1])[0]
        question_raw_list_only_string = [x.split(";")[0][1:-1] for x in question_raw_list if re.match(r'"(.|\n)*"', x)]

        question = {}
        current_key = ""
        for string in question_raw_list_only_string:
            if string in KEYS:
                current_key = string
                question[current_key] = ""
                continue
            question[current_key] = question[current_key] + SEPARATOR + string

        question["id"] = question_id

        if "div" in question["options"]:

            soup = BeautifulSoup(question["options"], "html.parser")

            question["options"] = [str(x) for x in soup.findAll("div")]
        else:
            question["options"] = [x for x in question["options"].split(SEPARATOR) if x != ""]

        final_question = {}

        for key in question:
            old_value = question[key]
            if type(old_value) == str:
                new_value = old_value.replace(SEPARATOR, "")
                final_question[key] = new_value
            else:
                final_question[key] = question[key]

        final_question["title"] = title

        return final_question
    except Exception as e:
        print("Error when convert question: ", question_raw_obj)
        raise e
        # return None
    
convert_raw_question_to_data(test)