import math
import processing as p
import spacy

#------------------------------------------------TF-IDF------------------------------------------------------------------

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
        query = p.processLineWithStemmer(question)
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


#----------------------------------------------------Linguistic Features------------------------------------------------


nlp = spacy.load('en_core_web_lg')

#Takes a question and list of sentences
#Compares the name entities of both to get a similarity value and stores it in a dictionary with similarity value as key
#The sentence indexes are stored as values so we can find the sentences again
def sentenceSim(question, sentences):
    simDict = {}
    questionEnt = nlp(question)
    for i in range(0, len(sentences)):
        sentence = sentences[i]
        sentenceNLP = nlp(sentence)
        similarity = questionEnt.similarity(sentenceNLP)
        simDict[similarity] = i
    return simDict


#Takes a sentence and runs it through the spacy entity recognizer
#Returns a tuple containing the entity and the entity label
def getSentenceNER(sentence):
    sentenceNLP = nlp(sentence)
    ents = [(e.text, e.label_) for e in sentenceNLP.ents]
    return ents

#POS tagger
def getSentencePOS(sentence):
    sentenceNLP = nlp(sentence)
    toks = [(token.text, token.pos_, token.tag_) for token in sentenceNLP]
    return toks

#NP chunker
def getSentenceNP(sentence):
    sentenceNLP = nlp(sentence)
    chunks = [chunk.text for chunk in sentenceNLP.noun_chunks]
    return chunks


#Default answer finder if question tagging fails to find anything good
#Mainly based on finding noun chunks and locality.
#Returns a list of the noun chunks in the sentence that are closest to the noun chunks in the question
#This function is mainly to be used on 'why' and 'which' questions where there are no obvious head words
def QSNounPhraseSimilarity(question, sentence):
    quesNLP = nlp(question)
    senNLP = nlp(sentence)
    #Boundary of similarity considered to be 'close enough'
    simBound = 0.8
    #list of similar NP indexes in sentence chunk list, initialized as set so there are no duplicate indexes stored
    simList = set()
    #Convert the generators to list of chunks
    qChunks = list(quesNLP.noun_chunks)
    senChunks = list(senNLP.noun_chunks)
    sChunkLen = len(senChunks)
    for qNP in qChunks:
        for i in range(0, sChunkLen):
            if qNP.similarity(senChunks[i]) > simBound:
                simList.add(i)
    simList = list(simList)
    #print (simList)
    #Create a list of all the closest noun phrases in sentence, only 1 index away
    npList = []
    if len(simList) != 0:
        for simIndex in simList:
            if ((simIndex < (sChunkLen - 1)) and (simIndex > 0)):
                npList.append(senChunks[simIndex-1].text)
                npList.append(senChunks[simIndex+1].text)
            elif (simIndex == 0):
                npList.append(senChunks[simIndex].text)
            elif (simIndex == (sChunkLen - 1)):
                npList.append(senChunks[simIndex-1].text)
    return npList

#tok1 = 'underdeveloped countries'
#tok2 = 'developing countries'
#tok1nlp = nlp(tok1)
#tok2nlp = nlp(tok2)

#for tok11 in tok1nlp.noun_chunks:
#    for tok22 in tok2nlp.noun_chunks:
#        print(tok11.text, tok22.text, tok11.similarity(tok22))

ques = "Which studio produced 'Super 8'?"
sent = "Spielberg served as an uncredited executive producer on The Haunting, The Prince of Egypt, Just Like Heaven, Shrek, Road to Perdition, and Evolution. He served as an executive producer for the 1997 film Men in Black, and its sequels, Men in Black II and Men in Black III. In 2005, he served as a producer of Memoirs of a Geisha, an adaptation of the novel by Arthur Golden, a film to which he was previously attached as director. In 2006, Spielberg co-executive produced with famed filmmaker Robert Zemeckis a CGI children's film called Monster House, marking their eighth collaboration since 1990's Back to the Future Part III. He also teamed with Clint Eastwood for the first time in their careers, co-producing Eastwood's Flags of Our Fathers and Letters from Iwo Jima with Robert Lorenz and Eastwood himself. He earned his twelfth Academy Award nomination for the latter film as it was nominated for Best Picture. Spielberg served as executive producer for Disturbia and the Transformers live action film with Brian Goldner, an employee of Hasbro. The film was directed by Michael Bay and written by Roberto Orci and Alex Kurtzman, and Spielberg continued to collaborate on the sequels, Transformers: Revenge of the Fallen and Transformers: Dark of the Moon. In 2011, he produced the J. J. Abrams science fiction thriller film Super 8 for Paramount Pictures."
#print (getSentencePOS(ques))
#print(getSentenceNER(ques))
#print(getSentenceNP(ques))
#print (getSentencePOS(sent))
#print(getSentenceNER(sent))
#print(getSentenceNP(sent))
#print(QSNounPhraseSimilarity(ques, sent))
#bad = "Equivalently, the smallness of the Planck constant reflects the fact that everyday objects and systems are made of a large number of particles. For example, green light with a wavelength of 555 nanometres (the approximate wavelength to which human eyes are most sensitive) has a frequency of 7014540000000000000\u2660540 THz (7014540000000000000\u2660540\u00d71012 Hz). Each photon has an energy E = hf = 6981358000000000000\u26603.58\u00d710\u221219 J. That is a very small amount of energy in terms of everyday experience, but everyday experience is not concerned with individual photons any more than with individual atoms or molecules. An amount of light compatible with everyday experience is the energy of one mole of photons; its energy can be computed by multiplying the photon energy by the Avogadro constant, NA \u2248 7023602200000000000\u26606.022\u00d71023 mol\u22121. The result is that green light of wavelength 555 nm has an energy of 7005216000000000000\u2660216 kJ/mol, a typical energy of everyday life."
#bad2 = "The assumption that black-body radiation is thermal leads to an accurate prediction: the total amount of emitted energy goes up with the temperature according to a definite rule, the Stefan\u2013Boltzmann law (1879\u201384). But it was also known that the colour of the light given off by a hot object changes with the temperature, so that \"white hot\" is hotter than \"red hot\". Nevertheless, Wilhelm Wien discovered the mathematical relationship between the peaks of the curves at different temperatures, by using the principle of adiabatic invariance. At each different temperature, the curve is moved over by Wien's displacement law (1893). Wien also proposed an approximation for the spectrum of the object, which was correct at high frequencies (short wavelength) but not at low frequencies (long wavelength). It still was not clear why the spectrum of a hot object had the form that it has (see diagram)."
#bad = p.regexAscii(bad)
#bad2 = p.regexAscii(bad2)
#print(bad)
#print(bad2)
#test = "naively"
#print(p.processLineWithStemmer(sent))
#print(ques.replace("'",""))

