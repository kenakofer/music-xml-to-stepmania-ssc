from string import Template
from test import *
import os
from sys import argv

class SccFile:

    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    TEMPLATE_FILE_PATH = SCRIPT_DIR + "/ssc.template"
    TEMPLATE = Template(open(TEMPLATE_FILE_PATH).read())

    def exportFromXml(xml_input_path, **options):
        score = loadXml(xml_input_path)
        parts = score.parts
        all_split = splitPart(parts[0]) + splitPart(parts[1])
        beat_length = getBeatLength(all_split)
        rows_per_beat = getRowsPerBeat(all_split, beat_length)

        easy_notes = rowsToString(getPartRowsWithHolds(all_split[0], rows_per_beat, beat_length = beat_length), rows_per_beat)
        easy_meter = estimateDifficultyMeter(easy_notes, parts[0])

        medium_notes = rowsToString(getPartRowsWithHolds(all_split[:2], rows_per_beat, beat_length = beat_length), rows_per_beat)
        medium_meter = estimateDifficultyMeter(medium_notes, parts[0])

        default_options = {
            'title': score.recurse().getElementsByClass('TextBox')[0].content,
            'subtitle': '',
            'artist': '',
            'music': xml_input_path.split("/")[-1].split(".")[0] + ".mp3",
            'offset': '-0.1',
            'bpms': getPartBpmString(all_split[0], beat_length = beat_length),
            'scroll_speed': '1.0',
            'easy_meter': easy_meter,
            'easy_notes': easy_notes,
            'medium_meter': medium_meter,
            'medium_notes': medium_notes,
        }

        output_string = SccFile.TEMPLATE.substitute({**default_options, **options})
        return output_string

if __name__ == "__main__":
    print(SccFile.exportFromXml(argv[1]))

## Example invocations:
#python3 ssc_file.py 'https://hymnal.gc.my/hymns/S036_Jesus,_tempted_in_the_desert/S036_Jesus,_tempted_in_the_desert.xml'
#python3 ssc_file.py 'https://hymnal.gc.my/hymns/H551_In_the_stillness_of_the_evening/H551_In_the_stillness_of_the_evening.xml'
#python3 ssc_file.py 'https://hymnal.gc.my/hymns/H118_Praise_God_from_whom/H118_Praise_God_from_whom.xml'
#python3 ssc_file.py 'https://hymnal.gc.my/hymns/H513_To_go_to_heaven/H513_To_go_to_heaven.xml'
#python3 ssc_file.py 'https://hymnal.gc.my/hymns/H493_I_heard_the_voice_of_Jesus_say/H493_I_heard_the_voice_of_Jesus_say.xml'
#python3 ssc_file.py 'https://hymnal.gc.my/hymns/H514_Lord,_I_am_fondly,_earnestly/H514_Lord,_I_am_fondly,_earnestly.xml'
