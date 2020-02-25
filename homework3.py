
import re
import copy
import time
def moveNegationInwards(sentence):
    parts=sentence.split('|')
    core=''
    # using formula 'S = S[:Index] + S[Index + 1:]'
    # remove first opening bracket '('
    parts[0] = parts[0][:1] + parts[0][1 + 1:]
    # remove last closing bracket ')'
    parts[0] = parts[0][:len(parts[0])-1] + parts[0][len(parts[0]):]
    # remove negation sign '~'
    parts[0] = parts[0][1:]
    # separate clauses
    andParts=parts[0].split('&')
    #rejoin clauses using or '|' and negate every clause
    for part in andParts:
        if part.startswith('~'):
            core = f'{core}{part[1:]}|'
        else:
            core=f'{core}~{part}|'
    core=core[0:len(core)-1]
    sentence=f'{core}|{parts[1]}'
    return sentence

def removeImplication(sentence):
    parts=sentence.split('=>')
    sentence=f'~({parts[0]})|{parts[1]}'
    return sentence

def ConvertToCNF(KB):
    CNF_KB=[]
    for sentence in KB:
        if '=>' in sentence:
            newSentence=removeImplication(sentence)
            newSentence=moveNegationInwards(newSentence)
            CNF_KB.append(newSentence)
        elif '=>' not in sentence and '&' in sentence:
            parts=sentence.split('&')
            for i in parts:
                CNF_KB.append(i)
        else:
            CNF_KB.append(sentence)
    return CNF_KB

def negateQuery(query):
    if query[0]=='~':
        query=query[1:]
    else:
        query=f'~{query}'
    return query

def unify(arguments1, arguments2, substitution):
    if substitution == False:
        return False

    elif arguments1 == arguments2:
        return substitution

    elif isinstance(arguments1, str) and arguments1.islower():
        return unify_var(arguments1, arguments2, substitution)

    elif isinstance(arguments2, str) and arguments2.islower():
        return unify_var(arguments2, arguments1, substitution)

    elif isinstance(arguments1, list) and isinstance(arguments2, list):
        if arguments1 and arguments2:
            return unify(arguments1[1:], arguments2[1:], unify(arguments1[0], arguments2[0], substitution))
        else:
            return substitution
    else:
        return False

def unify_var(var, x, substitution):
    if var in substitution:
        return unify(substitution[var], x, substitution)
    elif x in substitution:
        return unify(var, substitution[x], substitution)
    else:
        substitution[var] = x
        return substitution



def convertToParsingFormKB(KB):
    clauses = []
    for sen in KB:
        parts = sen.split('|')
        for part in parts:
            clauses.append(part)

    unificationClauses = []
    allArgsAndNames = []
    negative: bool
    for clause in clauses:

        if clause[0] == '~':
            negative = True
            parts = clause[1:].split('(')
            unificationClauses.append(parts[0])
            args = parts[1][:-1].split(',')
            for ar in args:
                unificationClauses.append(ar)
            clauseDict[tuple(unificationClauses)] = negative
        else:

            negative = False
            parts = clause.split('(')
            unificationClauses.append(parts[0])
            args = parts[1][:-1].split(',')
            for ar in args:
                unificationClauses.append(ar)
            clauseDict[tuple(unificationClauses)]=negative
        allArgsAndNames.append(unificationClauses)
        unificationClauses = []
    return allArgsAndNames

def convertToParsingFormQuery(KB):
    clauses = []
    for sen in KB:
        parts = sen.split('|')
        for part in parts:
            clauses.append(part)

    unificationClauses = []
    allArgsAndNames = []
    negative: bool
    for clause in clauses:

        if clause[0] == '~':
            negative = True
            parts = clause[1:].split('(')
            unificationClauses.append(parts[0])
            args = parts[1][:-1].split(',')
            for ar in args:
                unificationClauses.append(ar)
            clauseDictQuery[tuple(unificationClauses)] = negative
        else:

            negative = False
            parts = clause.split('(')
            unificationClauses.append(parts[0])
            args = parts[1][:-1].split(',')
            for ar in args:
                unificationClauses.append(ar)
            clauseDictQuery[tuple(unificationClauses)]=negative
        allArgsAndNames.append(unificationClauses)
        unificationClauses = []
    return allArgsAndNames

def convertToParsingForm(KB):
    clauses = []
    for sen in KB:
        parts = sen.split('|')
        for part in parts:
            clauses.append(part)
    unificationClauses = []
    allArgsAndNames = []
    for clause in clauses:
        if clause[0] == '~':
            parts = clause[1:].split('(')
            unificationClauses.append(parts[0])
            args = parts[1][:-1].split(',')
            for ar in args:
                unificationClauses.append(ar)
        else:
            parts = clause.split('(')
            unificationClauses.append(parts[0])
            args = parts[1][:-1].split(',')
            for ar in args:
                unificationClauses.append(ar)
        allArgsAndNames.append(unificationClauses)
        unificationClauses = []
    return allArgsAndNames


def standardize(KB):
    for statement in range(len(KB)):
        lst = []
        parts = KB[statement].split(' | ')
        for part in parts:
            lst.extend(part[part.index('(') + 1:part.index(')')].split(','))
        lst = list(set(lst))
        for prt in range(len(lst)):
            if lst[prt][0].islower():
                KB[statement] = KB[statement].replace(("(" + lst[prt]), ("(" + lst[prt] + str(statement)))
                KB[statement] = KB[statement].replace((lst[prt] + ")"), (lst[prt]+ str(statement) + ")"))
                KB[statement] = KB[statement].replace(("," + lst[prt] + ","), ("," + lst[prt]+ str(statement) + ","))
    return KB



def doResolution(sentence,query,subst,KB):

    remainingQueries=[]
    print('sentence:',sentence)
    print('query:',query)
    print('substitute:',subst)
    for i, j in subst.items():
        if i in sentence:
            sentence=re.sub(r'\b{0}\b'.format(i),j,sentence)
        elif i in query:
            query=re.sub(r'\b{0}\b'.format(i), j, query)
    sentenceParts=sentence.split('|')
    #print('sen',sentenceParts)
    queryParts=query.split('|')
    for qu in queryParts:
        if qu[0]=='~':
            if qu[1:] in sentenceParts:
                sentenceParts.remove(qu[1:])
            else:
                remainingQueries.append(qu)
        else:
            if f'~{qu}' in sentenceParts:
                sentenceParts.remove(f'~{qu}')
            else:
                remainingQueries.append(qu)
    newSentenceParts=sentenceParts[:]
    # print('newsen',sentenceParts)
    # print('new',newSentenceParts)
    for rq in remainingQueries:
        newSentenceParts.append(rq)
    result='|'.join(newSentenceParts)
    print('you get:',result)
    print("-----")
    # for i in KB:
    #     print(i)
    print("---------------------------------")

    return result

def resolution(q1, KB, t):
    #print(KB)
    if q1 == None or q1 == "":
        return True
    if q1 not in KB:
        KB.append(q1)
    else:
        return False
    #KB.sort(key=len)

    for sent in range(len(KB)):
        if ((time.time() - t) > 2):
            return False
        for params in convertToParsingFormKB([KB[sent]]):
            for qparams in convertToParsingFormQuery([q1]):
                if params==qparams:
                    if (clauseDict[tuple(params)]==True and clauseDictQuery[tuple(qparams)]==False )\
                    or (clauseDict[tuple(params)]==False and clauseDictQuery[tuple(qparams)]==True ):
                        newSentence = doResolution(KB[sent], q1, {}, KB)
                        if resolution(newSentence, KB, t):
                            return True

                elif params[0]==qparams[0]:
                    if (clauseDict[tuple(params)] == True and clauseDictQuery[tuple(qparams)] == False) \
                    or (clauseDict[tuple(params)] == False and clauseDictQuery[tuple(qparams)] == True):
                        resolvingSentence=KB[sent]
                            #print('pq',params, qparams)
                            #flag=1
                            #myClause=params
                            #print('g',myClause)
                            #print(convertToParsingForm([q1])[0],myClause)
                            #break
                # if flag==1:
                #     break
                        Query=qparams
                        sentenceFromKb=params

                        if sentenceFromKb:
                            ans = unify(Query, sentenceFromKb, {})
                            if ans:
                                newSentence=doResolution(resolvingSentence,q1,ans,KB)
                                if resolution(newSentence, KB, t):
                                    return True

    return False



f = open('input.txt', 'r')
NumOfQueries= f.readline()
Queries=[]
for i in range(int(NumOfQueries)):
    qu=f.readline()
    qu=qu.strip()
    Queries.append(qu)
NumOfSentences=f.readline()
KB=[]

for j in range(int(NumOfSentences)):
    sentence=f.readline()
    sentence=sentence.replace(" ", "")
    sentence=sentence.strip()
    KB.append(sentence)
f.close()




KB=ConvertToCNF(KB)
KB=standardize(KB)

f = open('output.txt', 'w')
for t in Queries:
    query=negateQuery(t)
    clauseDict = {}
    clauseDictQuery = {}
    Base=copy.deepcopy(KB)

    a=resolution(query,Base, time.time())
    if a==True:
        print('result','TRUE')
        f.write('TRUE')
    else:
        print('result', 'FALSE')
        f.write('FALSE')
    f.write("\n")
f.close()
