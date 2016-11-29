import luis # the luis package had to be slightly modified
import datetime
import dateutil.parser as dparser
import isodate
from nltk.tokenize import sent_tokenize

'''
Edge case for now: does not detect more than two times in a sentence.
This occurs because LUIS cannot detect more than two datetimes in a sentence.
'''

def analyze_text(): 
    datetime_sentences = []
    datetimeSentences = {}
    dictWithEntities = {}
    with open('sample_text.txt', 'r') as f:
        text = f.read()
    sentences = sent_tokenize(text) # finding each sentence in the email with nltk
    for sentence in xrange(len(sentences)):
        sentences[sentence] = sentences[sentence].replace('\n', ' ') # replace newline characters in a sentences with a space for easier formatting
    for sentence in xrange(len(sentences)):
        times = ""
        if find_dates(sentences[sentence]) != [['', []]]: # if the sentence contains a date and/or a time, do the following:
            date = find_dates(sentences[sentence])[0][0]
            time = find_dates(sentences[sentence])[0][1]
            entity = find_dates(sentences[sentence])[0][2]
            for timestring in xrange(len(time)):
                times += time[timestring]
                if timestring != len(time) - 1: times += ", "  # creates a string with all the times. formats correctly if there is more than one time.
            if date != "": datetimeSentences[sentences[sentence]] = date # if there is a date, create a key and corresponding value in the dictionary
            if str(time) != "[]": datetimeSentences[sentences[sentence]] = times # if there is a time, create a key and corresponding value in the dictionary
            #datetime_sentences.append([sentences[sentence], find_dates(sentences[sentence])])
            dictWithEntities[entity] = datetimeSentences
            datetimeSentences = {}
            
    return dictWithEntities    

def find_dates(string):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    current_date = datetime.datetime.now()
    tempdates = []
    dates = []
    times = []
    temptimes = []
    time = ""
    array = []
    date = ""
    entity = ""
    

    l = luis.Luis(url='https://api.projectoxford.ai/luis/v1/application?id=5d787786-7e0e-4055-9009-8eeab0baa48f&subscription-key=c4bfbca7ccc34ca8b0ab120b4a6aa56b')
    r = l.analyze(string)
    for i in xrange(len(r.entities)):
        if "datetime" in str(r.entities[i].type):
            if r.entities[i].resolution.keys() == [u'date']:
                entity = r.entities[i].entity
                tempdates.append([r.entities[i].resolution.values()]) # gets date values    ''' tempdates.append([r.entities[i].entity])
            if r.entities[i].resolution.keys() == [u'time']:
                entity = r.entities[i].entity
                temptimes.append([r.entities[i].resolution.values()]) # gets time values
    for i in xrange(len(temptimes)):
        temptime = str(temptimes[i])
        time = temptime[5:len(temptime)-3]
        if len(time) == 2: time += ":00"
        times.append(time)
    for j in xrange(len(tempdates)):

        readdate = tempdates[j]
        readdate = str(readdate)
        tempdate = dparser.parse(readdate,fuzzy=True)
        readday = tempdate.day
        readyear = tempdate.year
        readmonth = tempdate.month
        if is_int(readday) and day > int(readday):
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
        if readmonth != "XX" and int(readmonth) < month: year += 1
        if readyear == "XXXX": readyear = year
        if readmonth == "XX": readmonth = month
        date = str(readyear) + "-" + str(readmonth)+ "-" + str(readday)
    array.append(date)
    array.append(times)
    array.append(entity)
    dates.append(array)
    #print dates
    array = []

    return dates

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

print analyze_text()
    
