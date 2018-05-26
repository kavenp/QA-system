import math
import processing as p


#Counts the number of occurences of a term in a single document
def termOccurence(term, doc):
    count = 0
    for word in doc:
        if term == word:
            count += 1
    return count


#Counts the number of occurences of a term in all documents
def termDocOccurence(term, docs):
    count = 0
    for i in range(0, len(docs)):
        doc = docs[i]
        if term in doc:
            count += 1
    return count


#Takes a document (Dict) and list of questions (List)
#Returns a dict of document vectors and a dict of question vectors
#It does one pass through each document to save on computation and returns all relevant vectors
def getVectors(doc, questions):
    #total number of docs
    docNum = len(doc)

    #dictionary of preprocessed documents
    pDoc = p.processDoc(doc)

    #create set to ignore duplicate words
    words = set()
    for key in pDoc.keys():
        para = pDoc[key]
        for word in para:
            words.add(word)
    #convert to list for easy use
    words = list(words)

    #Get document vectors
    docVecs = {}
    for key in pDoc.keys():
        para = pDoc[key]
        tf = []
        for word in words:
            freq = termOccurence(word, para)
            weight = 0
            if freq > 0:
                weight = 1 + math.log2(freq)
            tf.append(weight)
        docVecs[key] = tf

    #get query vectors
    queryVecs = {}
    for questionID, question in questions:
        query = p.processLine(question)
        queryVec = []
        for word in words:
            freq = termOccurence(word, query)
            tdf = termDocOccurence(word, pDoc)
            weight = 0
            if freq > 0:
                weight = math.log2(1 + (float(docNum) / tdf))
            queryVec.append(weight)
        queryVecs[questionID] = queryVec

    return (docVecs, queryVecs)


#Implementation of vector space model cosine similarity formula
def cosSim(v1, v2):
    num = 0
    denom1 = 0
    denom2 = 0
    for i in range(0, len(v1)):
        num += v1[i] * v2[i]
        denom1 += v1[i] ** 2
        denom2 += v2[i] ** 2
    denom1 = math.sqrt(denom1)
    denom2 = math.sqrt(denom2)
    result = float(num)/(denom1 * denom2)
    return result


#Return best index according to td-idf
def getBestIndex(docVecs, queryVec):
    #best index initialized
    best = 0
    #Starter value with first doc
    bestSim = cosSim(docVecs[0], queryVec)
    for i in range(1, len(docVecs)):
        sim = cosSim(docVecs[i], queryVec)
        if sim > bestSim:
            bestSim = sim
            best = i
    return best

