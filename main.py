import processing as p
import helpers as h
import questionclassifier as qc
from nltk import tokenize
import random

def main():
    docs = p.getDocs()
    questions = p.getTest()

    #Dictionary with docid as key and the value being questions for that document as list
    docQuesDict = {}

    for question, docid, questionID in questions:
        if docid in docQuesDict.keys():
            docQuesDict[docid].append((questionID, question))
        else:
            docQuesDict[docid] = [(questionID, question)]

    #List to store the id, answer pairs that will be written to the csv
    csvData = []
    for key in docQuesDict.keys():
        docQuestions = docQuesDict[key]
        doc = docs[key]
        docVecs, queryVecs = h.getVectors(doc, docQuestions)

        for questionID, question in docQuestions:
            queryVec = queryVecs[questionID]
            bestPara = h.getBestIndex(docVecs, queryVec)
            sentences = tokenize.sent_tokenize(doc[bestPara])
            simDict = h.sentenceSim(question, sentences)
            bestSent = sentences[max(simDict.keys())]

            quesClass = qc.classifyQuestion(question)
            answer = []
            #Default cases
            if 'WHICH' in quesClass or 'WHY' in quesClass:
                answer = h.QS(question, bestSent)

            for key











