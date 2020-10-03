#!/usr/bin/env python3

import music21
import copy

def splitPart(part):
    return music21.stream.Stream([topNotesOf(part), bottomNotesOf(part)])

def topNotesOf(stream):
    new_part = copy.deepcopy(stream).chordify()
    for chord in new_part.recurse().getElementsByClass('Chord'):
        chord.notes = (chord.notes[-1],)
    return new_part.stripTies(retainContainers=True)

def bottomNotesOf(stream):
    new_part = copy.deepcopy(stream).chordify()
    for chord in new_part.recurse().getElementsByClass('Chord'):
        chord.notes = (chord.notes[0],)
    return new_part.stripTies(retainContainers=True)

def expandAllRepeats(stream):
    expanded_parts = [part.expandRepeats() for part in stream.getElementsByClass("Part")]
    return music21.stream.Stream(expanded_parts)

def doubleLength(stream):
    all_doubled = []
    for part in stream.getElementsByClass("Part"):
        measures = part.recurse().getElementsByClass('Measure')
        measures[0].leftBarline = music21.bar.Repeat('start')
        measures[-1].rightBarline = music21.bar.Repeat('end')
        doubled_part = part.expandRepeats()
        for i, m in enumerate(doubled_part.getElementsByClass("Measure")):
            m.number = i
        all_doubled.append(doubled_part)
    return music21.stream.Stream(all_doubled)

def fractionalOffset(note):
    return note.offset - int(note.offset)

def lcdOffset(notes):
    offsets_in_192nds = [round(fractionalOffset(n)*192) for n in notes]
    # Special case
    # Return the number of entries per quarter note duration
    for d in [192, 64, 48, 32, 24, 16, 12, 8, 6, 4, 3, 2, 1]:
        if all(map(lambda nd: nd % d == 0, offsets_in_192nds)):
            return 192//d
    return 1

def getStepArrow(note, key):
    if note.isChord:
        note = note.notes[0]
    scale_index = key.getScale().getTonic().pitchClass - note.pitch.pitchClass
    ##      do di re ri mi fa fi so si la li ti
    return [0, 1, 2, 1, 3, 0, 1, 2, 0, 3,  2, 1][scale_index]

def getMeasureSteps(measure):
    key = measure.getKeySignatures()[0]
    denominator = lcdOffset(measure.notes)
    # Stepmania can't handle anything but measures of 4 :(
    # rowsCount = round(measure.duration.quarterLength * denominator)
    rowsCount = round(4 * denominator)
    rows = [['0', '0', '0', '0'] for i in range(rowsCount)]
    for note in measure.notes:
        which_row = round(note.offset * denominator)
        which_arrow = getStepArrow(note, key)
        rows[which_row][which_arrow] = '1'
    return f"// Measure {measure.number}\n" + \
        "\n".join(["".join(row) for row in rows]) + '\n, '

def joinStepStrings(string1, string2):
    new_string = ""
    for c1, c2 in zip(string1, string2):
        if "2" in [c1, c2]:
            new_string += "2"
        elif "1" in [c1, c2]:
            new_string += "1"
        else:
            new_string += c1
    return new_string

def getPartStepsString(part):
    string = ""
    part_in_four = part.makeMeasures(meterStream=music21.meter.TimeSignature('4/4'))
    for measure in part_in_four.recurse().getElementsByClass('Measure'):
        string += getMeasureSteps(measure)
    return string

def getMeasureTimeSigString(measure):
    return f"{measure.offset}={int(measure.duration.quarterLength)}=4,\n"

def getPartTimeSigString(part):
    string = ""
    for measure in part.recurse().getElementsByClass('Measure'):
        string += getMeasureTimeSigString(measure)
    return string[:-2]+";"

def getPartBpmString(part):
    string=""
    for mark in part.recurse().getElementsByClass('MetronomeMark'):
        offset = mark.activeSite.offset + mark.offset
        string += f"{offset}={mark.getQuarterBPM()},\n"
    if len(string) > 0:
        return string[:-2]+";"
    else:
        return "0.0=120.0"

c = music21.converter.parse('https://hymnal.gc.my/hymns/H551_In_the_stillness_of_the_evening/H551_In_the_stillness_of_the_evening.xml')
parts = c.parts
all_split = splitPart(parts[0]) + splitPart(parts[1])
#all_expanded = expandAllRepeats(all_split)
#all_doubled = doubleLength(all_expanded)

print(getPartTimeSigString(all_split[0]))
print(getPartBpmString(all_split[0]))

step0 = getPartStepsString(all_split[0])
step1 = getPartStepsString(all_split[1])
joined = joinStepStrings(step0, step1)
print(joined)


