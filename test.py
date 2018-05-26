import processing as p
import helpers as h

docs = p.getDocs()
ques = p.getTest()

docIDQuestions = {}
for question, docid, questionID in ques:
    if docid in docIDQuestions.keys():
        docIDQuestions[docid].append((questionID, question))
    else:
        docIDQuestions[docid] = [(questionID, question)]

for key in docIDQuestions.keys():
    questions = docIDQuestions[key]
    doc = docs[key]
    docVecs, queryVecs = h.getVectors(doc, questions)
    for questionID, question in questions:
        queryVec = queryVecs[questionID]
        bestIndex = h.getBestIndex(docVecs, queryVec)
        print ("Question: %s" % question)
        #print ("DocId: %s" % docid)
        print ("QuestionID: %s" % questionID)
        print ("Best Index: %d" %bestIndex)