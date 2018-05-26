import nltk
import string
import json
import pandas


#---------------------------------------------JSON processing-----------------------------------------------------------


#path to data files directory
filePath = 'project_files/'

#data filenames
documentsPath = filePath + 'documents.json'
testPath = filePath + 'testing.json'
trainPath = filePath + 'training.json'

#Function that loads json files
def jsonLoader(jsonFile):
    with open(jsonFile) as jsonData:
        return json.load(jsonData)


def getDocs():
    docData = {}
    docs = jsonLoader(documentsPath)
    for doc in docs:
        docid = doc['docid']
        text = doc['text']
        docData[docid] = text
    return docData

docData = getDocs()
print(docData[0])

def getTest():
    questions = []
    test = jsonLoader(testPath)
    for testData in test:
        question = testData['question']
        docid = testData['docid']
        questionID = testData['id']
        questions.append((question, docid, questionID))
    return questions


def getTraining():
    training = []
    trainingData = jsonLoader(trainPath)
    for data in trainingData:
        question = data['question']
        text = data['text']
        answer_loc = data['answer_paragraph']
        docid = data['docid']
        training.append((question, text, answer_loc, docid))
    return training


#----------------------------------------------Word processing------------------------------------------------------


#set of stopwords
stopwords = set(nltk.corpus.stopwords.words('english'))

#set of punctuation
punctuation = set(string.punctuation)

stemmer = nltk.stem.PorterStemmer()
lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

#Lemmatizer
def lemmatize(word):
    lemma = lemmatizer.lemmatize(word, 'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word, 'n')
    return lemma


#Processes a single line i.e. Paragraph, sentence or question
def processLine(line):
    words = []
    line = nltk.word_tokenize(line)
    for word in line:
        stemWord = stemmer.stem(lemmatize(word.lower()))
        if word not in punctuation and word not in stopwords:
            words.append(stemWord)
    return words


#Process document which is a dictionary of lines
def processDoc(doc):
    processed = {}
    for i in range(0, len(doc)):
        processed[i] = processLine(doc[i])
    return processed


#-------------------------------------------------Excel Outputting------------------------------------------------------


#Function to write ids and answers to a csv file
def writeCSV(content, writeFile):
    ids = []
    answers = []
    for id, answer in content:
        ids.append(id)
        answers.append(answer)
    dFrame = pandas.DataFrame({'id': ids, 'answer': answers})
    dFrame.to_csv(writeFile, index=False, sep=',')