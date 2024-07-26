import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import validators
import time

url_db = "http://www.diseasesdatabase.com/disease_index_h.asp"
database = requests.get(url_db)

basedata = BeautifulSoup(database.content, "html.parser")

correlation = sqlite3.connect('illnesses.db')
caret = correlation.cursor()

caret.execute('DROP TABLE IF EXISTS illnesses')
correlation.commit()

caret.execute('''
    CREATE TABLE IF NOT EXISTS illnesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease TEXT,
        dossier TEXT
    )         '''
)

correlation.commit()

labelStorage = []
linkStorage = []

def text_extract(linkStorage):
    labels = []
    for anchor in linkStorage:
        applicator = BeautifulSoup(anchor, "html.parser")
        f_indice = applicator.find("a")
        if f_indice:
            text = f_indice.get_text().strip()
            if text:
                label = loadBalance(text)
                labels.append(label)
    return labels

def loadBalance(text, length=20):
    return text[:length]

def url_extract(linkStorage):
    urls = []
    for anchor in linkStorage:
        pureURL = re.search(r'href="(.*?)"', anchor)
        if pureURL and validators.url(pureURL.group(1)):
            urls.append(pureURL.group(1))
    return urls

anchors = basedata.find_all("a")
for anchor in anchors:
    linkStorage.append(str(anchor))

labels = text_extract([str(anchor) for anchor in anchors])
labelStorage.extend(labels)

links = url_extract(linkStorage)
linkStorage.clear()
linkStorage.extend(links)

calibration = min(len(labelStorage), len(linkStorage))
labelStorage = labelStorage[:calibration]
linkStorage = linkStorage[:calibration]

for disease, dossier in zip(labelStorage, linkStorage):
    caret.execute('INSERT INTO illnesses (disease, dossier) VALUES (?, ?)', (disease, dossier))

correlation.commit()

promptuser = input("What are some symptoms or causative factors that you suspect or know are present?" + "\n" + "(Please format your response as you would an English list, without the 'and', like this: Chest pain, Cough, Internal bleeing, Fatigue)")

try:
    caret.execute('ALTER TABLE illnesses ADD COLUMN conditionalls TEXT')
    correlation.commit()

except sqlite3.OperationalError:
    print("Error caught. Please [consider (redeclaring && remedying the program) || checking that existing alterations are not recorded and executed again]{String column;}")
    time.sleep(1.1)
    print("\033[2J\033[H")
    pass

def diagnosis(linkformation):
    dossier = requests.get(linkformation)
    DATA = BeautifulSoup(dossier.content, "html.parser")
    '''
    ^ Diseases Actively Triaged Accurately
    '''
    
    causeffects = []
    for formation in DATA.find_all("a", href=True):
        cosort = formation.get_text(strip=True)
        if cosort in ["may be caused by or feature of", "may cause or feature"]:
            causeffects.append(formation['href'])

    for causeffect in causeffects:
        if causeffect.startswith(('http://', 'https://')) != True:
            causeffect = linkformation.rstrip('/') + '/' + causeffect.lstrip('/')

        category = requests.get(causeffect)
        DATA = BeautifulSoup(category.content, "html.parser")
        '''
        aka Diseases Actively Triaged Accurately
        '''
        
        alphabeticalink = None
        for curelation in DATA.find_all("a", href=True):
            if curelation.get_text(strip=True) == "display items sorted alphabetically":
                alphabeticalink = curelation['href']
                break

        if alphabeticalink:
            if alphabeticalink.startswith(('http://', 'https://')) != True:
                alphabeticalink = causeffect.rstrip('/') + '/' + alphabeticalink.lstrip('/')

            core = requests.get(alphabeticalink)
            DATA = BeautifulSoup(core.content, "html.parser")
            '''
            short for Diseases Actively Triaged Accurately
            '''

            lastlinks = DATA.find_all("a", href=True)
            if len(lastlinks) >= 10:
                diseaders = []
                for anchorage in lastlinks[10:]:
                    if anchorage.find_next_sibling("hr"):
                        break
                    diseaders.append(anchorage.get_text(strip=True))

                return diseaders

def transcribeData():
    caret.execute('SELECT id, conditionalls FROM illnesses')
    TOpulls = caret.fetchall()

    for TOpull in TOpulls:
        diseaders = diagnosis(TOpull)
        if diseaders:
            iterableTOdiagnose = ', '.join(diseaders)

            caret.execute('''
                UPDATE illnesses
                SET conditionalls = ?
                          ''', (iterableTOdiagnose))
            correlation.commit()

transcribeData()

def binarySieve(arresponse, x):
    i = 0
    j = len(arresponse) - 1
    
    while i <= j:
        center = i + (j - l) // 2
        if arresponse[center] == x:
            return center
        elif arresponse[center] < x:
            i = center + 1
        else:
            j = center - 1
    return -1

def diseader(inputVals):
    tuples = caret.execute('SELECT id, disease, conditionalls FROM illnesses').fetchall()

    userConditions = [x.strip().lower() for x in inputVals.split(', ')]

    matched = []
    for tuple in tuples:
        id, disease, conditionalls = tuple

        detailist = [x.strip().lower() for x in conditionalls.split(', ')]
        detailist.sort()

        for condition in userConditions:
            if binarySieve(detailist, condition) != -1:
                matched.append(disease)
                break

    correlation.close()
    return matched
    
diseasions = diseader(promptuser)

if diseasions:
    print(f"Our diseasion has reached a conclusion; You may have one or more of the following diseases or illnesses!")
    
    for disease in diseasions:
        print(disease)
    print("Be sure to take great care of yourself and consult only with professional and qualified opinions. Diseasion is not such a tool and any superstitions caused by it are all absolute misconceptions on your behalf. Do not take this literally; it is something that helps you better understand diseases and illnesses alike!")
    
else:
    print("No matching diseases found!" + "\n" "Diseasion is underconstruction to integrate non-spelling-sensitive attributes to the program most likely by using APIs!")