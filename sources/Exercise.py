#!/usr/bin/env python3
from colorama import init
from colorama import Fore, Back, Style
import logging
import random
import shelve

import Konjugaattori, TodayShelf, Profile

class Exercise():
    myKonjugaattori = Konjugaattori.Konjugaattori()
    myTodayShelf = TodayShelf.TodayShelf()
    myProfile = Profile.Profile()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    logging.disable(logging.WARNING)
    lastVerbsAsked = []
    userVerbsToLearn = []
    userName = ''
    firstTimeToday = True
    poolSystemExplanationDone = False

    def __init__(self):
        init(autoreset=True)
        self.main()

    def getVerbList(self):
        verbList = []
        file = open('data/verbs.txt')
        verbList = file.readlines()
        for i in range(len(verbList)):
            if '\n' in verbList[i]:
                verbList[i] = verbList[i][:len(verbList[i])-1]
        file.close()
        return verbList

    def pickNewVerb(self):
        if len(self.userVerbsToLearn) == 0:
            self.myProfile.defineUserName(self.userName)
            poolList = self.myProfile.readPools()
            wantedVerbTypeList = self.askUserVerbType()
            if wantedVerbTypeList != 'menu':
                # Make a pool of verbs of the required verb types from all the 3 verb pools (but prioritise pools 1 and 2 over 0):
                print("Creating the verb list...")
                self.userVerbsToLearn = []
                for i in range(len(poolList)-1): # -1 because we don't care about pool 3 here
                    self.userVerbsToLearn.append([])
                    for j in range(len(poolList[i])):
                        if self.myKonjugaattori.verbTypeFinder(poolList[i][j]) in wantedVerbTypeList and not self.myTodayShelf.isVerbInTodayShelf(poolList[i][j], self.userName):
                            self.userVerbsToLearn[i].append(poolList[i][j])
                print("List created.")
                numberChosenVerbs = 0
                for pool in self.userVerbsToLearn:
                    numberChosenVerbs += len(pool)
                print('Number of verbs you still have to practise from this selection:', numberChosenVerbs)
            else:
                randomVerb = 'menu'
        if not 'wantedVerbTypeList' in locals():
            wantedVerbTypeList = []
        if wantedVerbTypeList != 'menu':
            numberChosenVerbs = 0
            for pool in self.userVerbsToLearn:
                numberChosenVerbs += len(pool)
            # Check if the remaining verbs are not all among the 3 last asked verbs:
            if numberChosenVerbs > 0 and numberChosenVerbs <= 3:
                fine = False
                for i in range(len(self.userVerbsToLearn)):
                    for j in range(len(self.userVerbsToLearn[i])):
                        if self.userVerbsToLearn[i][j] not in self.lastVerbsAsked[:3]:
                            fine = True
                            break
                            break
                if not fine:
                    numberChosenVerbs = 0
            if numberChosenVerbs == 0:
                print('There is no verb you can practice from this selection anymore today. Choose another verb type to study or come back tomorrow.')
                result = self.askUserToConjugate(self.userName)
            if not 'result' in locals():
                result = ''
            if result != 'menu':
                # Prioritise verbs from highest pool first:
                for i in range(len(self.userVerbsToLearn)):
                    myPool = self.userVerbsToLearn[len(self.userVerbsToLearn)-1-i]
                    if len(myPool) > 0:
                        randomVerb = myPool[random.randint(0, len(myPool)-1)]
                        while randomVerb in self.lastVerbsAsked[:3]:
                            randomVerb = myPool[random.randint(0, len(myPool)-1)]
                        break
            else:
                randomVerb = 'menu'
        if not 'randomVerb' in locals():
            randomVerb = 'menu'
        return randomVerb

    def formatUserAnswer(self, userConjugation):
        userConjugation = userConjugation.lower()
        userConjugation = userConjugation.split()
        # Check how many persons the user has given
        try:
            if userConjugation[0] == 'qwer':
                userConjugation = ['cheatCodeUsed', 'cheatCodeUsed', 'cheatCodeUsed', 'cheatCodeUsed', 'cheatCodeUsed', 'cheatCodeUsed']
        except IndexError: # Empty answer
            for i in range(6):
                userConjugation.append('none')
        if len(userConjugation) > 6:
            print("Be careful, you have answered more than 6 persons. Let's truncate your answer to 6 persons only.")
            userConjugation = userConjugation[:6]
        elif len(userConjugation) < 6 and userConjugation[0] != 'menu' and userConjugation[0] != 'ignore':
            print(Fore.RED + "Notice you have answered fewer than 6 persons.\n")
            # Fill the missing persons:
            for i in range(6 - len(userConjugation)):
                userConjugation.append('none')
        return userConjugation

    def checkUserAnswer(self, userConjugation, verb):
        self.myKonjugaattori.showSteps = False
        conjugatedVerb = self.myKonjugaattori.verbConjugatorLastAdditions(verb)
        if userConjugation == conjugatedVerb or userConjugation == ['cheatCodeUsed', 'cheatCodeUsed', 'cheatCodeUsed', 'cheatCodeUsed', 'cheatCodeUsed', 'cheatCodeUsed']:
            correct = True
            print (Fore.GREEN + 'Correct!')
        elif userConjugation[0] == 'menu':
            correct = 'menu'
        elif userConjugation[0] == 'ignore':
            self.myProfile.riseVerbInPools(verb, True)
            self.deleteVerbFromUserVerbs(verb)
            correct = False
        else:
            correct = False
            self.printCorrection(userConjugation, conjugatedVerb)
        return correct

    def askUserToConjugate(self, userName):
        self.userName = userName
        self.userVerbsToLearn = [] # resetting
        ignoreFeatureHintShown = False
        while True:
            verb = self.pickNewVerb()
            if verb == 'menu':
                break
            # Explanation about the pools of verb if first time for user (score = 0)
            myScore = self.myProfile.calculateScores()
            if not myScore:
                myScore = 0
            else:
                myScore = myScore.get(userName)
            if myScore == 0 and not self.poolSystemExplanationDone:
                print('''\nHow does the verb pool system work?
There are 4 pools of verbs:''')
                colors = [Fore.RED, Fore.MAGENTA, Fore.LIGHTBLUE_EX, Fore.CYAN]
                for i in range(len(colors)):
                    print('- ' + colors[i] + 'Pool ' + colors[i] + str(i))
                print('''When you start learning, all the verbs are in Pool 0.
Everytime you answer a verb properly, it goes to the next pool. 
The only exception to this is that a verb can't move up by more than one pool on the same day. You have to exercise regularly to learn.
When a verb gets to Pool 3, it is considered to be learnt permanently.''')
                self.poolSystemExplanationDone = True

            print('\nConjugate ' + Fore.CYAN + verb + ' (' + self.getVerbTranslation(verb) + '):')
            if self.firstTimeToday:
                print("(Type the six persons of the conjugated verb separated by spaces, like so: ... ... ... ... ... ...)")
                self.firstTimeToday = False
            if not ignoreFeatureHintShown:
                print('(type "ignore" to stop learning this verb)')
                ignoreFeatureHintShown = True
            self.lastVerbsAsked.append(verb)
            userConjugation = self.formatUserAnswer(input())
            correct = self.checkUserAnswer(userConjugation, verb)
            if correct == 'menu':
                break
            elif correct:
                self.deleteVerbFromUserVerbs(verb)
                self.myProfile.riseVerbInPools(verb)
                self.myTodayShelf.addVerbToTodayShelf(verb, self.userName)

    def deleteVerbFromUserVerbs(self, verb):
        for i in range(len(self.userVerbsToLearn)):
            if verb in self.userVerbsToLearn[i]:
                del self.userVerbsToLearn[i][self.userVerbsToLearn[i].index(verb)]
                break

    def askUserVerbType(self):
        print('\nWhich verb type do you want to study?') 
        verbTypeList = (
                ' All', 
                ' -a/ä',
                ' -da/dä',
                ' -la/lä/ra/rä/na/nä/',
                ' -ta/tä + -eta/etä verbs which do not mean a change of state',
                ' -ita/itä',
                ' -eta/etä (only includes verbs which mean a change of state)',
                ' -hda/hdä (nähdä, tehdä, etc.)',
                ' -olla',
                ' -vitä (hävitä, levitä, selvitä, etc.)',
                '-juosta',
                '-sta/stä (type 3-verbs which do not get gradated)',
                'Common verb types',
                'Special verb types',
                'Verbs with consonant gradation (verb types 1, 3, 4 and 6)',
                'Verbs without consonant gradation'
                )
        for i in range(len(verbTypeList)):
            if i == 0:
                myString = Fore.RED + '        ' + str(i) + ': ' + verbTypeList[i]
            elif i > 0 and i <= 6:
                myString = Fore.LIGHTBLUE_EX + '        ' + str(i) + ': ' + verbTypeList[i]
            elif i >= 7 and i <= 11:
                myString = Fore.CYAN + '        ' + str(i) + ': ' + verbTypeList[i]
            elif i >= 12:
                myString = Fore.GREEN + '        ' + str(i) + ': ' + verbTypeList[i]
            if i == 1:
                myString = '    Common verb types:\n' + myString
            elif i == 7:
                myString = '    Special verb types:\n' + myString
            elif i == 12:
                myString = '    Combinations of verb types:\n' + myString
            print(myString)
        userInput = input()
        while not userInput.isdecimal() or int(userInput) < 0 or int(userInput) > len(verbTypeList)-1:
            if userInput == 'menu':
                return 'menu'
            print('Invalid input. Write a number between 0 and ' + str(len(verbTypeList)-1))
            userInput = input()
        # Make a list of wanted verb types from the user answer:
        userInput = int(userInput)
        verbTypesList = []
        if userInput == 0:
            verbTypesList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        elif userInput >= 1 and userInput <= 11:
            verbTypesList.append(userInput)
        elif userInput == 12:
            verbTypesList = [1, 2, 3, 4, 5, 6]
        elif userInput == 13:
            verbTypesList = [7, 8, 9, 10, 11]
        elif userInput == 14:
            verbTypesList = [1, 3, 4, 6]
        elif userInput == 15:
            verbTypesList = [2, 5, 7, 8, 9, 10, 11]
        return verbTypesList

    def printCorrection(self, userConjugation, conjugatedVerb):
        print(Fore.RED + 'Wrong!')
        conjugatedVerbWithCorrection = ['', '', '', '', '', '']
        for i in range(6):
            # Before comparing the conjugations, we need to make sure all the strings have the same length (for the same persons)
            if len(userConjugation[i]) < len(conjugatedVerb[i]):
                userConjugation[i] = userConjugation[i] + (len(conjugatedVerb[i])-len(userConjugation[i])) * '*'
            elif len(userConjugation[i]) > len(conjugatedVerb[i]):
                conjugatedVerb[i] = conjugatedVerb[i] + (len(userConjugation[i])-len(conjugatedVerb[i])) * '*'
                userConjugation[i] = userConjugation[i][0:len(conjugatedVerb[i])] + userConjugation[i][len(conjugatedVerb[i]):].upper()
        for i in range(6):
            for j in range(len(conjugatedVerb[i])):
                if userConjugation[i][j] != conjugatedVerb[i][j]:
                    conjugatedVerbWithCorrection[i] = conjugatedVerbWithCorrection[i]+ conjugatedVerb[i][j].upper()
                    userConjugation[i] = userConjugation[i][0:j] + userConjugation[i][j].upper() + userConjugation[i][j+1:]
                else:
                    conjugatedVerbWithCorrection[i] = conjugatedVerbWithCorrection[i] + conjugatedVerb[i][j]

        # Converting lists to strings:
        userConjugation = str(userConjugation)
        conjugatedVerbWithCorrection = str(conjugatedVerbWithCorrection)

        # Calculate the percentage of errors by counting the uppercase keys
        conjugatedVerbWithCorrectionLettersOnly = conjugatedVerbWithCorrection.replace('[', '')
        conjugatedVerbWithCorrectionLettersOnly = conjugatedVerbWithCorrectionLettersOnly.replace(']', '')
        conjugatedVerbWithCorrectionLettersOnly = conjugatedVerbWithCorrectionLettersOnly.replace("'", '')
        conjugatedVerbWithCorrectionLettersOnly = conjugatedVerbWithCorrectionLettersOnly.replace(',', '')
        conjugatedVerbWithCorrectionLettersOnly = conjugatedVerbWithCorrectionLettersOnly.replace(' ', '')
        lettersCountTotal = len(conjugatedVerbWithCorrectionLettersOnly)
        # Delete lowercase letters to count incorrect letters:
        #lettersCountIncorrect = 0
        #for i in range(lettersCountTotal):
        #    if conjugatedVerbWithCorrectionLettersOnly[i].isupper() == True:
        #        lettersCountIncorrect += 1
        #percentage = 100 - (lettersCountIncorrect / lettersCountTotal * 100)
        #print('Success: %.0f' % percentage + ' %')
        # Colour formatting:
        userConjugationColoured = ''
        for i in range(len(userConjugation)):
            if userConjugation[i] == '*':
                userConjugationColoured += Fore.RED + userConjugation[i]
            elif userConjugation[i].isupper():
                userConjugationColoured += Fore.RED + userConjugation[i].lower()
            else:
                userConjugationColoured += Fore.RESET + userConjugation[i]
        conjugatedVerbWithCorrectionColoured = ''
        for i in range(len(conjugatedVerbWithCorrection)):
            if conjugatedVerbWithCorrection[i] == '*':
                conjugatedVerbWithCorrectionColoured += Fore.GREEN + conjugatedVerbWithCorrection[i]
            elif conjugatedVerbWithCorrection[i].isupper():
                conjugatedVerbWithCorrectionColoured += Fore.GREEN + conjugatedVerbWithCorrection[i].lower()
            else:
                conjugatedVerbWithCorrectionColoured += Fore.RESET + conjugatedVerbWithCorrection[i]

        print('You answer:', userConjugationColoured)
        print('Correction:', conjugatedVerbWithCorrectionColoured)

    def getVerbTranslation(self, verb):
        shelfFile = shelve.open('data\\verbsTranslated')
        verbs = list(shelfFile.keys())
        translatedVerbs = list(shelfFile.values())
        verbIndex = verbs.index(verb)
        translation = translatedVerbs[verbIndex]
        shelfFile.close()
        return translation

    def main(self):
        #self.askUserToConjugate()
        pass

if __name__=='__main__':
    Exercise()