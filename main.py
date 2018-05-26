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
    num = 0
    for key in docQuesDict.keys():
        docQuestions = docQuesDict[key]
        doc = docs[key]
        docVecs, queryVecs = h.getVectors(doc, docQuestions)

        for questionID, question in docQuestions:
            queryVec = queryVecs[questionID]
            bestPara = h.getBestIndex(docVecs, queryVec)
            sentences = tokenize.sent_tokenize(doc[bestPara])
            simDict = h.sentenceSim(question, sentences)
            simKeys = list(simDict.keys())
            simKeys = sorted(simKeys, reverse=True)
            #Take the top 3 keys
            simKeys = simKeys[:3]
            bestSentsIndexes = []
            bestSents = []
            #More than one sentence of the top similarity
            for i in range(0, len(simKeys)):
                bestSentsIndexes.append(simDict[simKeys[i]])
            for bestI in bestSentsIndexes:
                temp = p.regexAscii(sentences[bestI].lower())
                bestSents.append(temp)
            quesClass = qc.classifyQuestion(p.processLineWithLem(question))
            answer = set()
            #Question cases
            if 'WHICH' in quesClass or 'WHY' in quesClass:
                #print("WHICH")
                answer.update(set(h.QSNounPhraseSimilarity(question, bestSent)))
            else:
                #print("NON-WHICH")
                #Get the all matching entities that matches the question type
                ents = h.getSentenceNER(bestSents[0])
                for word, label in ents:
                    if label in quesClass:
                        answer.add(word)

            #If answer is still empty after all the previous cases
            #Then we start trying the other high ranked similarity sentences
            if len(answer) == 0:
                #print("FIRST EMPTY")
                for sent in bestSents[1:]:
                    #If we have enough answers after a 1-2 keys break out
                    if len(answer) > 1:
                        break
                    else:
                        ents = h.getSentenceNER(sent)
                        for word, label in ents:
                            if label in quesClass:
                                answer.add(word)
            #Still empty? Use better than random searcher
            if len(answer) == 0:
                #print("SECOND EMPTY")
                for bestSent in bestSents:
                    answer.update(set(h.QSNounPhraseSimilarity(question, bestSent)))
                    #answerStr = " ".join(answer)
            #Ok, I give up, random entity
            if len(answer) == 0:
                #print("THIRD EMPTY")
                ner = h.getSentenceNER(bestSents[0])
                if len(ner) != 0:
                    nerText, tag = ner[(random.randint(0, len(ner)) - 1)]
                    answer.add(nerText)
            if len(answer) == 0:
                #print("FOURTH EMPTY")
                nps = h.getSentenceNP(bestSents[0])
                npsText = nps[(random.randint(0, len(nps)) - 1)]
                answer.add(npsText)
            if len(answer) == 0:
                #print("FIFTH EMPTY")
                toks = tokenize.word_tokenize(bestSents[0])
                answer.add(toks[(random.randint(0, len(toks))-1)])
            answer = list(answer)
            answerStr = " ".join(answer)

            print(num)
            num += 1
            #print (answer)
            print(answerStr)
            csvData.append((questionID, answerStr))

    #We have all our data
    print("Creating Excel Spreadsheet...")
    p.writeCSV(csvData, "result.csv")
    print("Finished.")

main()









