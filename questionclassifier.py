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

        if word == 'when':
            classified.add('TIME')
            classified.add('DATE')

        if word in ['who', 'whom', 'whose']:
            classified.add('PERSON')

        if word == 'what':
            if index == len(questionTags) - 1:
                #Should not consider this
                pass
            else:
                if questionTags[index + 1][1] == 'NN':
                    if questionTags[index + 1][0] in ['year', 'month', 'day', 'age', 'century', 'time', 'second',
                                                      'minute']:
                        classified.add('TIME')
                        classified.add('DATE')
                    if questionTags[index + 1][0] in ['city', 'street', 'town', 'country', 'state', 'road', 'suburb',
                                                      'area', 'place', 'location']:
                        classified.add('LOC')
                        classified.add('GPE')
                    if questionTags[index + 1][0] in ['percentage', 'number', 'value', 'amount', 'rank']:
                        classified.add('PERCENT')
                        classified.add('CARDINAL')
                        classified.add('MONEY')
                        classified.add('QUANTITY')
                    if questionTags[index + 1][0] in ['team', 'publication', 'organization', 'company',
                                                      'government', 'university', 'party', 'kingdom', 'club']:
                        classified.add('ORG')
                if questionTags[index + 1][1] in ['JJ', 'JJR', 'JJS']:
                    j = index + 1
                    while j < len(questionTags) and questionTags[j][1] != 'NN':
                        j += 1
                    if j < len(questionTags) and questionTags[j][1] != 'NN':
                        if questionTags[j][0] in ['year', 'month', 'day', 'age', 'century', 'time', 'second', 'minute']:
                            classified.add('DATE')
                            classified.add('TIME')
                        if questionTags[j][0] in ['city', 'street', 'town', 'country', 'state', 'road', 'suburb',
                                                  'area', 'place', 'location']:
                            classified.add('LOC')
                            classified.add('GPE')
                        if questionTags[j][0] in ['percentage', 'number', 'place', 'value', 'amount', 'rank']:
                            classified.add('PERCENT')
                            classified.add('CARDINAL')
                            classified.add('MONEY')
                            classified.add('QUANTITY')
                        if questionTags[j][0] in ['team', 'publication', 'organization', 'company', 'government',
                                                  'university', 'newspaper', 'party', 'kingdom', 'club']:
                            classified.add('ORG')

        if word == 'which':
            if index == len(questionTags) - 1:
                #Should not consider this
                pass
            else:
                #Obvious cases for time and location and organizations
                if questionTags[index + 1][0] in ['year', 'month', 'day', 'age', 'century', 'time', 'second', 'minute']:
                    classified.add('DATE')
                    classified.add('TIME')
                if questionTags[index + 1][0] in ['city', 'street', 'town', 'country', 'state', 'road', 'suburb',
                                                  'area', 'place', 'location']:
                    classified.add('LOC')
                    classified.add('GPE')
                if questionTags[index + 1][0] in ['team', 'publication', 'organization', 'company', 'government',
                                                  'university', 'newspaper', 'party', 'kingdom', 'club']:
                    classified.add('ORG')
            #In the case where none match the obvious cases
            classified.add('WHICH')

        if word == 'why':
            if index == len(questionTags) - 1:
                #Should not consider this
                pass
            else:
                #No easy obvious head words for why questions
                classified.add('WHY')

        if word == 'how':
            if questionTags[index + 1][0] in ['many', 'far', 'long', 'old']:
                classified.add('DATE')
                classified.add('TIME')
                classified.add('CARDINAL')
                classified.add('QUANTITY')
                classified.add('PERCENT')
            if questionTags[index + 1][0] in ['much']:
                if index + 2 < len(questionTags) and questionTags[index + 2][0] in ['money']:
                    classified.add('MONEY')
                else:
                    classified.add('MONEY')
                    classified.add('CARDINAL')
                    classified.add('QUANTITY')
    return classified
