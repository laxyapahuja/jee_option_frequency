from bs4 import BeautifulSoup as soup
import re

def getAnswers(anskey):
    key = {}
    ansRows = anskey.find("table",{"class":"table table-bordered table-condensed"}).findAll(class_=None,recursive=False)
    for ansRow in ansRows:
        qID = ansRow.find("span",id=re.compile("QuestionNo")).contents[0]
        ans = ansRow.find("span",id=re.compile("RAnswer")).contents[0]
        key[str(qID)]=ans
    return key

def getQuestions(quespaper):
    questions_info = {}
    quesGroups = quespaper.findAll("div",{"class":"section-cntnr"})
    for i in range(len(quesGroups)):
        quesDivs = quesGroups[i].findAll("div",{"class":"question-pnl"})
        for quesDiv in quesDivs:
            qType = quesDiv.find("td",text=re.compile("Question Type")).findNext('td').contents[0]
            qID = quesDiv.find("td",text=re.compile("Question ID")).findNext('td').contents[0]
            if qType == "MCQ":
                q1 = quesDiv.find("td",text=re.compile("Option 1 ID")).findNext('td').contents[0]
                q2 = quesDiv.find("td",text=re.compile("Option 2 ID")).findNext('td').contents[0]
                q3 = quesDiv.find("td",text=re.compile("Option 3 ID")).findNext('td').contents[0]
                q4 = quesDiv.find("td",text=re.compile("Option 4 ID")).findNext('td').contents[0]
                questions_info[qID] = [q1, q2, q3, q4]
    return questions_info

def finalCoding(questions_info, key):
    frequency = {1: 0, 2: 0, 3: 0, 4:0}
    for i in key:
        try:
            frequency[questions_info[i].index(key[i])+1] +=1
        except KeyError:
            continue
    return frequency

qpaperHTML = ""
anskeyHTML = ""
with open("question_paper.html","r") as f:
    qpaperHTML = f.read()
with open("answer_key.html","r") as f:
    anskeyHTML = f.read()

quespaper = soup(qpaperHTML,"lxml")
anskey = soup(anskeyHTML,"lxml")

frequency = finalCoding(getQuestions(quespaper), getAnswers(anskey))

print(frequency)