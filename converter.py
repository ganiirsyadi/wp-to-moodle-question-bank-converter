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
    "raw_question": """<![CDATA[a:8:{s:4:"type";s:6:"single";s:4:"hint";s:1:" ";s:11:"explanation";s:0:"";s:16:"original_content";s:1098:"<p><u><strong>(Text for questions 41-50)</strong></u></p>
<p><img decoding="async" loading="lazy" class="alignnone wp-image-12328" src="https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-460x350.png" alt="" width="758" height="577" srcset="https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-460x350.png 460w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-1024x779.png 1024w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-768x584.png 768w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-50x38.png 50w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-600x456.png 600w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-120x91.png 120w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-310x236.png 310w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44.png 1093w" sizes="(max-width: 758px) 100vw, 758px" /></p>
<p>&#8211;</p>
<p>According to the passage, astronauts exercises can also be beneficial for people who &#8230;</p>
";s:7:"content";s:1098:"<p><u><strong>(Text for questions 41-50)</strong></u></p>
<p><img decoding="async" loading="lazy" class="alignnone wp-image-12328" src="https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-460x350.png" alt="" width="758" height="577" srcset="https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-460x350.png 460w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-1024x779.png 1024w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-768x584.png 768w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-50x38.png 50w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-600x456.png 600w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-120x91.png 120w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44-310x236.png 310w, https://jelajahstudies.com/wp-content/uploads/2021/06/Screenshot-44.png 1093w" sizes="(max-width: 758px) 100vw, 758px" /></p>
<p>&#8211;</p>
<p>According to the passage, astronauts exercises can also be beneficial for people who &#8230;</p>
";s:7:"options";a:4:{i:0;s:37:"want to avoid possible heart failure.";i:1;s:42:"are too busy to exercise on a daily basis.";i:2;s:48:"wish to be prospective astronauts in the future.";i:3;s:53:"have to stay in their beds for a long period of time.";}s:7:"correct";s:1:"4";s:2:"id";i:12331;}]]>"""
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
        raise e
        # return None
    
convert_raw_question_to_data(test)