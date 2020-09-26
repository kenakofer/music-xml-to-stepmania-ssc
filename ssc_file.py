class SccFile:
    NO_ACTION = "0"
    TAP = "1"
    HOLD_START = "2"
    END = "3"
    ROLL_START = "4"
    MINE = "M"
    AUTO_KEY = "K" # Newer versions
    LIFT = "L" # Newer versions
    FAKE = "F" # Newer versions

    def __init__(self, title):
        self.fields = {
            "version": "0.83",
            "title": title,
            "subtitle": "",
            "artist": "",
            "titletranslit": "",
            "subtitletranslit": "",
            "artisttranslit": "",
            "genre": "",
            "origin": "",
            "credit": "",
            "banner": "",
            "background": "",
            "previewid": "",
            "jacket": "",
            "cdimage": "",
            "diskimage": "",
            "lyricspath": "",
            "cdtitle": "",
            "music": "",
            "offset": 0.0,
            "samplestart": 0.0,
            "samplelength": 7.0,
            "selectable": "",
            "bpms": {},
            "stops": {},
            "delays": {},
            "warps": {},
            "timesignatures": {0.0: "4=4"},
            "tickcounts": {0.0: 4},
            "combos": {0.0: 1},
            "speeds": {0.0: "1.000=0.000=0"},
            "scrolls": {0.0: 1},
            "fakes": {},
            "labels": {0.0: "Song Start"},
            "bgchanges": {},
            "keysounds": {},
            "attacks": {},
            "stops": {},
            "notedata_by_difficulty": {
                "Easy": {
                    "chartname": "",
                    "stepstype": "dance-single",
                    "description": "",
                    "meter": "2",
                    "radarvalues": [],
                    "credit": "",
                    "notes": [[NO_ACTION * 4] * 4]
                },
                "Medium": {
                    "chartname": "",
                    "stepstype": "dance-single",
                    "description": "",
                    "meter": "4",
                    "radarvalues": [],
                    "credit": "",
                    "notes": [[NO_ACTION * 4] * 4]
                },
                "Hard": {
                    "chartname": "",
                    "stepstype": "dance-single",
                    "description": "",
                    "meter": "6",
                    "radarvalues": [],
                    "credit": "",
                    "notes": [[NO_ACTION * 4] * 4]
                }
            }
        }

    def exportSccString(self):
        string = ""
        for key in self.fields:
            if key == "notedata_by_difficulty":
                continue
            string += f"#{key.upper()}:"
            value = self.fields[key]
            if isinstance(value, dict):
                pass # TODO finish 



