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
            #print(simDict)
            bestSentsIndexes = []
            bestSents = []
            #More than one sentence of the top similarity
            for i in range(0, len(simKeys)):
                bestSentsIndexes.append(simDict[simKeys[i]])
            for bestI in bestSentsIndexes:
                #temp = p.regexAscii(sentences[bestI].lower())
                bestSents.append(sentences[bestI])
            #print(bestSents)
            quesClass = qc.classifyQuestion(p.processLineWithLem(question))

            if len(quesClass) > 0:
                answer = set()
                #Question cases
                if 'WHY' in quesClass:
                    #print("WHICH")
                    for sent in bestSents:
                        if len(answer) > 0:
                            break
                        else:
                            tempQS = set(h.QSNounPhraseSimilarity(question, bestSents[0]))
                            if len(tempQS) == 0:
                                pass
                            else:
                                answer.update(tempQS)
                else:
                    #print("NON-WHICH")
                    #Get the all matching entities that matches the question type
                    for sent in bestSents:
                        if len(answer) > 0:
                            break
                        else:
                            ents = h.getSentenceNER(sent)
                            for word, label in ents:
                                if label in quesClass:
                                    answer.add(word)
            else:
                answer = set()
                #Use all entities in best sentence to try for an answer
                ner = h.getSentenceNER(bestSents[0])
                for word, label in ner:
                    answer.add(word)
            # Still empty? Use better than locality searcher
            if len(answer) == 0:
                for sent in bestSents:
                    if len(answer) > 0:
                        break
                    else:
                        tempQS = set(h.QSNounPhraseSimilarity(question, bestSents[0]))
                        if len(tempQS) == 0:
                            pass
                        else:
                            answer.update(tempQS)
            # Ok, I give up, all random
            ran = random.randint(0,1)
            #Get random half of noun phrases from best sentence
            if len(answer) == 0:
                #print(bestSents)
                nps = h.getSentenceNP(bestSents[0])
                npsH = len(nps)/2
                if ran:
                    temp = nps[int(npsH):]
                else:
                    temp = nps[:int(npsH)]
                if len(temp) == 0:
                    pass
                else:
                    answer.update(set(temp))
            #If that still doesn't work take random half of nouns from best sentence
            if len(answer) == 0:
                postagged = h.getSentencePOS(bestSents[0])
                nouns = []
                for noun, tag in postagged:
                    if tag in ['NN', 'NNP', 'NNPS', 'NNS']:
                        if noun not in nouns:
                            nouns.append(noun)
                nounH = len(nouns)/2
                if ran:
                    temp = nouns[nounH:]
                else:
                    temp = nouns[:nounH]
                if len(temp) == 0:
                    pass
                else:
                    answer.update(set(temp))

            answer = list(answer)
            #print (answer)
            answerStr = " ".join(answer)

            print(questionID)
            num += 1
            #print (answer)
            print(answerStr)
            csvData.append((questionID, answerStr))

    #We have all our data
    print("Creating Excel Spreadsheet...")
    p.writeCSV(csvData, "result.csv")
    print("Finished.")

main()









