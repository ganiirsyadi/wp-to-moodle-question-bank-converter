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
    "raw_question": """<![CDATA[a:8:{s:4:"type";s:6:"single";s:4:"hint";s:0:"";s:11:"explanation";s:0:"";s:16:"original_content";s:363:"<div class="vibe_editor_rich_text">
<p style="">Jika nilai ujiannya baik Fajar akan mendapatkan hadiah. Jika fajar mendapatkan hadiah karena nilai ujiannya yang baik maka hadiah yang diterima Fajar adalah bukan mainan. Fajar mendapatkan hadiah mainan.</p>
</div>
<div class="vibe_editor_rich_text">
<p style="">Maka kesimpulan yang tepat adalah&#8230;</p>
</div>
";s:7:"content";s:363:"<div class="vibe_editor_rich_text">
<p style="">Jika nilai ujiannya baik Fajar akan mendapatkan hadiah. Jika fajar mendapatkan hadiah karena nilai ujiannya yang baik maka hadiah yang diterima Fajar adalah bukan mainan. Fajar mendapatkan hadiah mainan.</p>
</div>
<div class="vibe_editor_rich_text">
<p style="">Maka kesimpulan yang tepat adalah&#8230;</p>
</div>
";s:7:"options";a:5:{i:0;s:85:"<div class="vibe_editor_rich_text"><p style="">Nilai ujian Fajar tidak baik</p></div>";i:1;s:117:"<div class="vibe_editor_rich_text"><p style="">Nilai ujian fajar baik akan tetapi mendapatkan hadiah mainan</p></div>";i:2;s:88:"<div class="vibe_editor_rich_text"><p style="">Fajar selalu mendapatkan hadiah</p></div>";i:3;s:121:"<div class="vibe_editor_rich_text"><p style="">Fajar mendapat mainan bukan&nbsp;karena nilai ujiannya yang baik</p></div>";i:4;s:86:"<div class="vibe_editor_rich_text"><p style="">Nilai ujian Fajar selalu baik</p></div>";}s:7:"correct";s:1:"1";s:2:"id";i:4465;}]]>"""
}

def convert_raw_question_to_data(question_raw_obj: object):
    SEPARATOR = "!@!@"

    try:
        title = question_raw_obj["title"]

        question_raw = question_raw_obj["raw_question"]
        question_raw_list = re.split("s:\d+:", question_raw)

        question_id = re.findall(r"\d+", question_raw_list[-1])[0]
        question_raw_list_only_string = [x[1:].rsplit('"', 1)[0] for x in question_raw_list if re.match(r'"(.|\n)*"', x)]

        question = {}
        current_key = ""
        for string in question_raw_list_only_string:
            if string in KEYS:
                current_key = string
                question[current_key] = ""
                continue
            question[current_key] = question[current_key] + SEPARATOR + string

        question["id"] = question_id

        if "</div>" in question["options"]:

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

        print(final_question["options"])

        return final_question
    except Exception as e:
        raise e
        # return None

if __name__ == "__main__":
    convert_raw_question_to_data(test)