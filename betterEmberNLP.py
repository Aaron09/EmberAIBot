import luis # the luis package had to be slightly modified
import datetime
import dateutil.parser as dparser
from nltk.tokenize import sent_tokenize

'''
Edge case for now: does not detect more than two times in a sentence.
This occurs because LUIS cannot detect more than two datetimes in a sentence.
'''

def analyze_text():
    datetime_sentences = []
    with open('sample_text.txt', 'r') as f:
        text = f.read()
    sentences = sent_tokenize(text)
    for sentence in xrange(len(sentences)):
        sentences[sentence] = sentences[sentence].replace('\n', ' ')
    for sentence in xrange(len(sentences)):
        #if len(find_dates(sentences[sentence])) != 0:
        if find_dates(sentences[sentence]) != [['', []]]:
            datetime_sentences.append([sentences[sentence], find_dates(sentences[sentence])])
    return datetime_sentences    

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
    

    l = luis.Luis(url='https://api.projectoxford.ai/luis/v1/application?id=5d787786-7e0e-4055-9009-8eeab0baa48f&subscription-key=c4bfbca7ccc34ca8b0ab120b4a6aa56b')
    r = l.analyze(string)
    for i in xrange(len(r.entities)):
        if "datetime" in str(r.entities[i].type):
            if r.entities[i].resolution.keys() == [u'date']: 
                tempdates.append([r.entities[i].resolution.values()]) # gets date values
            if r.entities[i].resolution.keys() == [u'time']:
                temptimes.append([r.entities[i].resolution.values()]) # gets time values
    for i in xrange(len(temptimes)):
        temptime = str(temptimes[i])
        time = temptime[5:len(temptime)-3]
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
        '''array.append(date)
        array.append(times)
        print array
 #       dates.append([date, times])
        dates.append(array)
        array = []
        year = now.year
        month = now.month
        day = now.day'''
    array.append(date)
    array.append(times)
    dates.append(array)
    array = []

    return dates

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

print analyze_text()
    
