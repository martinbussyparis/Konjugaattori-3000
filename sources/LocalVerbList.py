#!/usr/bin/env python3
import time
import bs4
import os
import sys
from mtranslate import translate
import shelve
import Konjugaattori

class LocalVerbList():

    myKonjugaattori = Konjugaattori.Konjugaattori()

    def __init__(self):
         self.knownIssues = ()

    def getVerbPresentTime(self, verb):
        try:
            file = open('verbs//' + verb + '.html')
            soup = bs4.BeautifulSoup(file, "html.parser")
            element = soup.select('td > pre')
            elementSplit = str(element).split()
            elementSplit = elementSplit[1:13]
            # delete personal pronouns
            try:
                elementSplit.remove('minä')
                elementSplit.remove('sinä')
                elementSplit.remove('hän')
                elementSplit.remove('me')
                elementSplit.remove('te')
                elementSplit.remove('he')
            except ValueError:
                print ('ERROR: This verb does not have personal pronouns.________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________')
                sys.exit()
            return elementSplit
        except FileNotFoundError:
            return 'This verb does not exist in the database'

    def askUserVerbToConjugate(self):
        while True:
            print("\nType a verb to find:")
            verb = ""
            verb = input()
            verb = verb.lower()
            startTime = time.clock ()
            print (self.getVerbPresentTime(verb))
            print ("Execution time: %.3f seconds" % (time.clock () - startTime))

    def getVerbsAll(self):
        verbsAll = []
        verbsAll = os.listdir('verbs')
        # removing '.html' from every string in the list
        for i in range(len(verbsAll)):
            verbsAll[i] = verbsAll[i][:-5]
        return verbsAll

    def getVerbsIncludingString(self, include):
        verbs = self.getVerbsAll()
        verbsIncluding = []
        for i in range(len(verbs)):
            if include in verbs[i]:
                verbsIncluding.append(verbs[i])
        return verbsIncluding

    def getVerbsOfGroup(self, verbList, verbTypeTarget):
        newVerbList = []
        if int(verbTypeTarget) == 0:
            newVerbList = verbList
        else:
            for i in range(len(verbList)):
                verbType = self.myKonjugaattori.verbTypeFinder(verbList[i])
                if int(verbType) == int(verbTypeTarget):
                    newVerbList.append(verbList[i])
        return newVerbList

    def askUserStringToLookForInVerbs(self):
        while True:
            print ('\nType the string that must be included in the verbs you are looking for:')
            include = input()
            include = include.lower()
            print ('\nType the verb type you want (0 for all):')
            verbTypeTarget = input()
            verbTypeTarget = verbTypeTarget.lower()
            startTime = time.clock ()
            verbs = self.getVerbsIncludingString(include)
            print('\nVerbs matching this string:', len(verbs))
            verbs = self.getVerbsOfGroup(verbs, verbTypeTarget)
            print ('\nVerbs matching this string and this verb type (', len(verbs), 'verbs ):\n', verbs)
            print ('\nConjugation:')
            for i in range(len(verbs)):
                conjugatedVerbDB = self.getVerbPresentTime(verbs[i])
                conjugatedVerbKonjugaattori = self.myKonjugaattori.verbConjugatorLastAdditions(verbs[i])
                print (verbs[i])
                print ('Ymmärrä Suomea:\n', conjugatedVerbDB)
                print ('Konjugaattori:\n', conjugatedVerbKonjugaattori)
                if conjugatedVerbDB != conjugatedVerbKonjugaattori:
                    print('WARNING: the two conjugations do not match')
            print ("\nExecution time: %.3f seconds" % (time.clock () - startTime))

    def compareConjugationsSingle(self):
        while True:
            print ('\nType the verb you want to compare the conjugation of:')
            verb = input()
            verb = verb.lower()
            conjugatedVerbDB = self.getVerbPresentTime(verb)
            conjugatedVerbKonjugaattori = self.myKonjugaattori.verbConjugatorLastAdditions(verb)
            print ('Ymmärrä Suomea:\n', conjugatedVerbDB)
            print ('Konjugaattori:\n', conjugatedVerbKonjugaattori)
            if conjugatedVerbDB != conjugatedVerbKonjugaattori:
                print('WARNING: the two conjugations do not match')

    def compareConjugationsAll(self):
        startTime = time.clock ()
        verbs = self.getVerbsAll()
        incorrectVerbs = []
        for i in range(len(verbs)):
            conjugatedVerbDB = self.getVerbPresentTime(verbs[i])
            conjugatedVerbKonjugaattori = self.myKonjugaattori.verbConjugatorLastAdditions(verbs[i])
            if conjugatedVerbDB != conjugatedVerbKonjugaattori:
                print ('Verb:\n', verbs[i])
                print ('Ymmärrä Suomea:\n', conjugatedVerbDB)
                print ('Konjugaattori:\n', conjugatedVerbKonjugaattori)
                incorrectVerbs.append(verbs[i])
        print('\nNumber of verbs which do not conjugate properly:', len(incorrectVerbs), '/', len(verbs))
        percentage = 100 - (len(incorrectVerbs) / len(verbs) * 100)
        print('Percentage of correct ones: %.2f' % percentage)
        if len(incorrectVerbs) != 0:
            print('\nVerbs which do not conjugate properly:')
            print(incorrectVerbs)
        print ("\nExecution time: %.3f seconds" % (time.clock () - startTime))

    def compareConjugationsMeTe(self): # To detects the mistakes in the DB where Me and Te are reversed
        startTime = time.clock ()
        verbs = self.getVerbsAll()
        incorrectVerbs = []
        for i in range(len(verbs)):
            conjugatedVerbDB = self.getVerbPresentTime(verbs[i])
            conjugatedVerbKonjugaattori = self.myKonjugaattori.verbConjugatorLastAdditions(verbs[i])
            if conjugatedVerbDB[0] == conjugatedVerbKonjugaattori[0] and conjugatedVerbDB[3] != conjugatedVerbKonjugaattori[3]:
                print ('Ymmärrä Suomea:\n', conjugatedVerbDB)
                print ('Konjugaattori:\n', conjugatedVerbKonjugaattori)
                print('WARNING: the two conjugations do not match')
                incorrectVerbs.append(verbs[i])
        if len(incorrectVerbs) != 0:
            print('\nNumber of verbs which do not conjugate properly:', len(incorrectVerbs), '/', len(verbs))
            percentage = 100 - (len(incorrectVerbs) / len(verbs) * 100)
            print('Percentage of correct ones: %.2f' % percentage)
            print('\nVerbs which do not conjugate properly:')
            print(incorrectVerbs)
        else:
            print('Good!')
        print ("\nExecution time: %.3f seconds" % (time.clock () - startTime))

    def compareConjugationsMissingLetter(self):
        print ('\nType the letter that is missing in the verbs you are looking for:')
        letter = input()
        letter = include.lower()
        startTime = time.clock ()
        verbs = self.getVerbsAll()
        incorrectVerbs = []
        for i in range(len(verbs)):
            conjugatedVerbDB = self.getVerbPresentTime(verbs[i])
            conjugatedVerbKonjugaattori = self.myKonjugaattori.verbConjugatorLastAdditions(verbs[i])
            if conjugatedVerbDB != conjugatedVerbKonjugaattori:
                if letter in conjugatedVerbDB[0] and letter not in conjugatedVerbKonjugaattori[0]:
                    print ('Verb:\n', verbs[i])
                    print ('Ymmärrä Suomea:\n', conjugatedVerbDB)
                    print ('Konjugaattori:\n', conjugatedVerbKonjugaattori)
                    incorrectVerbs.append(verbs[i])
                    break
        if len(incorrectVerbs) != 0:
            print('\nNumber of verbs which do not conjugate properly:', len(incorrectVerbs), '/', len(verbs))
            percentage = 100 - (len(incorrectVerbs) / len(verbs) * 100)
            print('Percentage of correct ones: %.2f' % percentage)
            print('\nVerbs which do not conjugate properly:')
            print(incorrectVerbs)
        print ("\nExecution time: %.3f seconds" % (time.clock () - startTime))

    def findUnknownIssues(self):
        startTime = time.clock ()
        verbs = self.getVerbsAll()
        incorrectVerbs = []
        for i in range(len(verbs)):
            conjugatedVerbDB = self.getVerbPresentTime(verbs[i])
            conjugatedVerbKonjugaattori = self.myKonjugaattori.verbConjugatorLastAdditions(verbs[i])
            if conjugatedVerbDB != conjugatedVerbKonjugaattori:
                if verbs[i] not in self.knownIssues:
                    print ('Verb:\n', verbs[i])
                    print ('Ymmärrä Suomea:\n', conjugatedVerbDB)
                    print ('Konjugaattori:\n', conjugatedVerbKonjugaattori)
                    incorrectVerbs.append(verbs[i])
        if len(incorrectVerbs) != 0:
            print('\nNumber of verbs which do not conjugate properly that we do not already know of:', len(incorrectVerbs), '/', len(verbs))
            percentage = 100 - (len(incorrectVerbs) / len(verbs) * 100)
            print('Percentage of correct ones: %.2f' % percentage)
            print('\nVerbs which do not conjugate properly:')
            print(incorrectVerbs)
            print ("\nExecution time: %.3f seconds" % (time.clock () - startTime))
        else:
            print('We already know about all of the incorrect ones')

    def translateVerbsFromDB(self):
        verbs = self.getVerbsAll()
        verbsTranslated = []
        shelfFile = shelve.open('verbsTranslated')
        for i in range(len(verbs)):
            translation = 'to ' + translate(verbs[i], 'en', 'fi')
            verbsTranslated.append(translation)
            shelfFile[verbs[i]] = translation
            print('Verb done: ' + str(i+1) + ' / ' + str(len(verbs)))
        print(verbsTranslated)
        print(shelfFile)
        shelfFile.close()

    def printTranslatedVerbs(self):
        shelfFile = shelve.open('verbsTranslated')
        verbs = list(shelfFile.keys())
        translatedVerbs = list(shelfFile.values())
        for i in range(len(verbs)):
            print(verbs[i] + ' = ', translatedVerbs[i])
        shelfFile.close()

    def makeVerbListFile(self):
        verbs = self.getVerbsAll()
        verbsString = '\n'.join(verbs)
        file = open('UserData/verbs.txt', 'w')
        file.write(verbsString)
        file.close()

    def findVerbsOfXLetters(self):
        print("How many letters?")
        letterAmount = int(input())
        verbs = self.getVerbsAll()
        for v in verbs:
            if len(v) <= letterAmount:
                print(v)

    def askUserWhatToRun(self):
        featureList = (
            'self.askUserStringToLookForInVerbs()', 
            'self.askUserVerbToConjugate()', 
            'self.compareConjugationsSingle()', 
            'self.compareConjugationsMeTe()', 
            'self.compareConjugationsAll()', 
            'self.compareConjugationsMissingLetter()',
            'self.findUnknownIssues()',
            'self.translateVerbsFromDB()',
            'self.printTranslatedVerbs()',
            'self.makeVerbListFile()',
            'self.findVerbsOfXLetters()'
            )
        while True:
            print ('\nType the number of the feature you want to use:')
            for i in range(len(featureList)):
                print (i, '-', featureList[i])
            featureNumber = input()
            if featureNumber == '0':
                self.askUserStringToLookForInVerbs()
            elif featureNumber == '1':
                self.askUserVerbToConjugate()
            elif featureNumber == '2':
                self.compareConjugationsSingle()
            elif featureNumber == '3':
                self.compareConjugationsMeTe()
            elif featureNumber == '4':
                self.compareConjugationsAll()
            elif featureNumber == '5':
                self.compareConjugationsMissingLetter()
            elif featureNumber == '6':
                self.findUnknownIssues()
            elif featureNumber == '7':
                self.translateVerbsFromDB()
            elif featureNumber == '8':
                self.printTranslatedVerbs()
            elif featureNumber == '9':
                self.makeVerbListFile()
            elif featureNumber == '10':
                self.findVerbsOfXLetters()

    def main(self):
        self.askUserWhatToRun()
        
if __name__=='__main__':
    LocalVerbList().main()