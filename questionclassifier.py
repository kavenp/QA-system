import nltk
import nltk.tag


def classifyQuestion(question):
    questionTags = nltk.pos_tag(question)
    classified = set()

    for index in range(0, len(questionTags)):
        word, tag = questionTags[index]

        #Many cases, go into each case depending on the first 'wh' or 'hw' question marker
        if word == 'where':
            classified.add('LOC')
            classified.add('GPE')

        elif word == 'when':
            classified.add('TIME')
            classified.add('DATE')

        elif word in ['who', 'whom', 'whose']:
            classified.add('PERSON')

        elif word == 'what':
            if index == len(questionTags) - 1:
                #Should not consider this
                pass
            else:
                if questionTags[index + 1][1] == 'NN':
                    if questionTags[index + 1][0] in ['year', 'month', 'day', 'age', 'century', 'time', 'second',
                                                      'minute']:
                        classified.add('TIME')
                        classified.add('DATE')
                    elif questionTags[index + 1][0] in ['city', 'street', 'town', 'country', 'state', 'road', 'suburb',
                                                      'area', 'place', 'location']:
                        classified.add('LOC')
                        classified.add('GPE')
                    elif questionTags[index + 1][0] in ['percentage']:
                        classified.add('PERCENT')
                        classified.add('CARDINAL')
                    elif questionTags[index + 1][0] in ['number', 'rank', 'amount', 'value']:
                        classified.add('MONEY')
                        classified.add('CARDINAL')
                        classified.add('QUANTITY')
                    elif questionTags[index + 1][0] in ['team', 'publication', 'organization', 'company',
                                                      'government', 'university', 'party', 'kingdom', 'club']:
                        classified.add('ORG')
                    else:
                        pass
                if questionTags[index + 1][1] in ['JJ', 'JJR', 'JJS']:
                    j = index + 1
                    while j < len(questionTags) and questionTags[j][1] not in ['NN', 'NNS', 'NNP', 'NNPS']:
                        j += 1
                    if j < len(questionTags) and questionTags[j][1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                        if questionTags[j][0] in ['year', 'month', 'day', 'age', 'century', 'time', 'second', 'minute']:
                            classified.add('DATE')
                            classified.add('TIME')
                        elif questionTags[j][0] in ['city', 'street', 'town', 'country', 'state', 'road', 'suburb',
                                                    'area', 'place', 'location']:
                            classified.add('LOC')
                            classified.add('GPE')
                        elif questionTags[j][0] in ['percentage']:
                            classified.add('PERCENT')
                            classified.add('CARDINAL')
                        elif questionTags[j][0] in ['number', 'rank', 'amount', 'value']:
                            classified.add('MONEY')
                            classified.add('CARDINAL')
                            classified.add('QUANTITY')
                        elif questionTags[j][0] in ['team', 'publication', 'organization', 'company', 'government',
                                                    'university', 'newspaper', 'party', 'kingdom', 'club']:
                            classified.add('ORG')
                        else:
                            pass
        elif word == 'which':
            if index == len(questionTags) - 1:
                #Should not consider this
                pass
            else:
                #Obvious cases for time and location and organizations
                if questionTags[index + 1][0] in ['year', 'month', 'day', 'age', 'century', 'time']:
                    classified.add('DATE')
                    classified.add('TIME')
                elif questionTags[index + 1][0] in ['city', 'street', 'town', 'country', 'state']:
                    classified.add('LOC')
                    classified.add('GPE')
                elif questionTags[index + 1][0] in ['team', 'publication', 'organization', 'company', 'government',
                                                    'university', 'newspaper']:
                    classified.add('ORG')
                else:
                    pass

        elif word == 'how':
            if questionTags[index + 1][0] in ['many', 'far', 'long', 'old']:
                classified.add('DATE')
                classified.add('TIME')
                classified.add('CARDINAL')
                classified.add('QUANTITY')
                classified.add('PERCENT')
            elif questionTags[index + 1][0] in ['much']:
                if index + 2 < len(questionTags) and questionTags[index + 2][0] in ['money']:
                    classified.add('MONEY')
                else:
                    classified.add('MONEY')
                    classified.add('CARDINAL')
                    classified.add('QUANTITY')

        elif word == 'why':
            if index == len(questionTags) - 1:
                #Should not consider this
                pass
            else:
                #No easy obvious head words for why questions
                classified.add('WHY')
        else:
            #Not a question
            pass

    return classified

