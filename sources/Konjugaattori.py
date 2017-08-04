#!/usr/bin/env python3
import logging
from colorama import init
from colorama import Fore, Back, Style

class Konjugaattori():

    def __init__(self):
        init(autoreset=True)
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
        logging.disable(logging.WARNING)
        self.consonantCoupleDictionaryStrong = {'tt': 't', 'kk': 'k', 'pp': 'p', 't': 'd', 'p': 'v', 'k': '', 
                                                'nt': 'nn', 'rt': 'rr', 'mp': 'mm', 'nk': 'ng', 'lt': 'll', 'ht': 'hd', 
                                                'lke': 'lje', 'rke': 'rje', 'hke': 'hje', 'lk': 'l', 
                                                'ntt': 'nt', 'rtt': 'rt', 'nkk': 'nk', 'rpp': 'rp', 'ltt': 'lt', 
                                                'hk': 'h', 'rkk': 'rk', 'rk': 'r'}
        self.consonantCoupleDictionaryWeak = {'t': 'tt', 'k': 'kk', 'p': 'pp', 'd': 't', 'v': 'p', 
                                              'nn': 'nt', 'rr': 'rt', 'mm': 'mp', 'ng': 'nk', 'll': 'lt', 'hd': 'ht', 
                                              'lje': 'lke', 'rje': 'rke', 'hje': 'hke', 'nt': 'ntt', 
                                              'h': 'hk', 'rk': 'rkk'}
        self.etaVerbsType4 = ('hävetä', 'herjetä', 'kiivetä', 'langeta', 'poiketa', 'puhjeta', 'ruveta', 'teljetä', 'todeta', 
                              'liueta', 'kalveta', 'laimeta') # If a verb of type 6 doesn't mean a change, it will be conjugated like a normal verb type-4 verb.
        # verbs based on loan words which don't get gradated
        self.verbsBasedOnUngradatableWords = ('avata', 'ehkäistä', 'erikoistua', 'ihailla', 'kävellä', 'kohota', 'kokeilla', 'kuivata', 'kuvailla', 'kuvata', 
                                              'mokata', 'rukoilla', 'sivellä', 'povata', 'ravata', 'tuhota', 'vaivata', 'vihata')
        # verbs based on loan words which get gradated even if they shouldn't
        self.verbsBasedOnLoanWordsWhichGradate = {'karata': 'karka', 'kelvata': 'kelpa', 'kyetä': 'kyke', 'paeta': 'pake',
                                                  'pelätä': 'pelkä', 'vaieta': 'vaike'}
        self.showSteps = False
        self.stepsAlreadyPrinted = []
        self.main()

    def printSteps(self, myString):
        if self.showSteps:
            if myString not in self.stepsAlreadyPrinted:
                print(myString)
                self.stepsAlreadyPrinted.append(myString)

    def verbTypeFinder(self, verb):
        self.printSteps(Fore.LIGHTBLUE_EX + '\nVerb Type')
        if verb[len(verb)-4:] == "olla":
            self.printSteps('    - ends with -olla' + '\n    --> ' + str(8))
            return 8 # Creating a new specific group for Olla and potential verbs ending the same way
        elif verb[len(verb)-6:] == "juosta":
            self.printSteps('    - ends with -juosta' + '\n    --> ' + str(10))
            return 10 # Creating a new specific group for Juosta and potential verbs ending the same way
        elif verb[len(verb)-3:] == "hda" or verb[len(verb)-3:] == "hdä":
            self.printSteps('    - ends with -hda/hdä (nähdä, tehdä, etc.)' + '\n    --> ' + str(7))
            return 7 # Creating a new group for verbs ending in -hda, like nähdä and tehdä
        elif verb[len(verb)-4:] == "vitä":
            self.printSteps('    - ends with -vitä (hävitä, levitä, selvitä, etc.)' + '\n    --> ' + str(9))
            return 9 # Creating a new group for verbs ending in -vitä, like hävitä, levitä and selvitä. They don't belong to verb type 5, like they should. Instead, they conjugate like verb type 4, but without consonant gradation.
        elif verb[len(verb)-2:] == "da" or verb[len(verb)-2:] == "dä":
            self.printSteps('    - ends with -da/dä' + '\n    --> ' + str(2))
            return 2
        elif verb[len(verb)-2:] == "la" or verb[len(verb)-2:] == "lä":
            self.printSteps('    - ends with -la/lä/ra/rä/na/nä' + '\n    --> ' + str(3))
            return 3
        elif verb[len(verb)-2:] == "ra" or verb[len(verb)-2:] == "rä":
            self.printSteps('    - ends with -la/lä/ra/rä/na/nä' + '\n    --> ' + str(3))
            return 3
        elif verb[len(verb)-2:] == "na" or verb[len(verb)-2:] == "nä":
            self.printSteps('    - ends with -la/lä/ra/rä/na/nä' + '\n    --> ' + str(3))
            return 3
        elif verb[len(verb)-3:] == "sta" or verb[len(verb)-3:] == "stä":
            self.printSteps('    - ends with -sta/stä (type 3-verbs which do not get gradated)' + '\n    --> ' + str(11))
            return 11 # New verb type for verbs ending in -sta/stä, which conjugate like verb type 3 verbs but don't get gradated
        elif verb[len(verb)-3:] == "ita" or verb[len(verb)-3:] == "itä":
            self.printSteps('    - ends with -ita/itä' + '\n    --> ' + str(5))
            return 5
        elif verb[len(verb)-3:] == "eta" or verb[len(verb)-3:] == "etä":
            if verb in self.etaVerbsType4: # If a verb of type 6 doesn't mean a change, it will be conjugated like a normal verb type-4 verb.
                self.printSteps('    - ends with -ta/tä or -eta/etä and do not mean a change of state' + '\n    --> ' + str(4))
                return 4
            else:
                self.printSteps('    - ends with -eta/etä and means a change of state' + '\n    --> ' + str(6))
                return 6
        elif verb[len(verb)-2:] == "ta" or verb[len(verb)-2:] == "tä":
            self.printSteps('    - ends with -ta/tä or -eta/etä and do not mean a change of state' + '\n    --> ' + str(4))
            return 4
        elif verb[len(verb)-1:] == "a" or verb[len(verb)-1:] == "ä":
            self.printSteps('    - ends with -a/ä' + '\n    --> ' + str(1))
            return 1
        else:
            return 0

    def verbStrengthFinder(self, verb):
        self.printSteps(Fore.LIGHTBLUE_EX + '\nVerb Vowel Strength (if contains "a", "o" or "u")')
        if "a" in verb or "o" in verb or "u" in verb:
            self.printSteps('    --> strong')
            return "strong"
        else:
            self.printSteps('    --> Weak')
            return "weak"

    def verbTypeConsonantStrengthFinder(self, verb):
        self.printSteps(Fore.CYAN + '\nVerb Type Consonant Strength')
        verbType = self.verbTypeFinder(verb)
        if verbType == 1:
            self.printSteps('    - verb type 1')
            self.printSteps('    --> strong')
            return "Strong (verb type 1)"
        elif verbType == 3 or verbType == 4 or verbType == 6:
            self.printSteps('    - verb type 3, 4 or 6')
            self.printSteps('    --> weak')
            return "Weak (verb type 3, 4 or 6)"
        elif verbType == 2 or verbType == 5:
            self.printSteps('    - no consonant gradation for verb types 2 and 5')
            self.printSteps('    --> none   ')
            return "no consonant gradation for verb types 2 and 5"
        else:
            self.printSteps('    - irrelevant to special verb types created for this program')
            self.printSteps('    --> none   ')
            return "None (special verb type created for this program)"

    def stemFinder(self, verb):
        verbType = self.verbTypeFinder(verb)
        if verbType == 0:
            return False
        else:
            verbStrength = self.verbStrengthFinder(verb)
            self.printSteps(Fore.LIGHTBLUE_EX + '\nStem')
            myVerb = '    - ' + verb
            if verbStrength == "strong":
                if verbType == 1:
                    self.printSteps(myVerb + ' - 1 letter (verb type 1)')
                if verbType == 2:
                    self.printSteps(myVerb + ' - 2 letters (verb type 3)')
                if verbType == 3:
                    self.printSteps(myVerb + ' - 2 letters + "e" (verb type 3)')
                if verbType == 4:
                    self.printSteps(myVerb + ' - 2 letters + "a" (verb type 4)')
                if verbType == 5:
                    self.printSteps(myVerb + ' - 2 letters + "tse" (verb type 5)')
                if verbType == 6:
                    self.printSteps(myVerb + ' - 2 letters + "ne" (verb type 6)')
                if verbType == 7:
                    self.printSteps(myVerb + ' - 3 letters + "e" (verb type 7)')
                if verbType == 8:
                    self.printSteps(myVerb + ' - 2 letters + "e" (verb type 8)')
                if verbType == 10:
                    self.printSteps(myVerb + ' - 2 letters + "e" (verb type 10)')
                if verbType == 11:
                    self.printSteps(myVerb + ' - 2 letters + "e" (verb type 11)')
                switcher = {
                    0: "?",
                    1: verb[:len(verb)-1],
                    2: verb[:len(verb)-2],
                    3: verb[:len(verb)-2] + "e",
                    4: verb[:len(verb)-2] + "a",
                    5: verb[:len(verb)-2] + "tse",
                    6: verb[:len(verb)-2] + "ne",
                    7: verb[:len(verb)-3] + "e",
                    8: verb[:len(verb)-2] + "e",
                    10: verb[:len(verb)-2] + "e",
                    11: verb[:len(verb)-2] + "e"
                }
            else:
                if verbType == 1:
                    self.printSteps(myVerb + ' - 1 letter (verb type 1)')
                if verbType == 2:
                    self.printSteps(myVerb + ' - 2 letters (verb type 2)')
                if verbType == 3:
                    self.printSteps(myVerb + ' - 2 letters + "e" (verb type 3)')
                if verbType == 4:
                    self.printSteps(myVerb + ' - 2 letters + "ä" (verb type 4)')
                if verbType == 5:
                    self.printSteps(myVerb + ' - 2 letters + "tse" (verb type 5)')
                if verbType == 6:
                    self.printSteps(myVerb + ' - 2 letters + "ne" (verb type 6)')
                if verbType == 7:
                    self.printSteps(myVerb + ' - 3 letters + "e" (verb type 7)')
                if verbType == 9:
                    self.printSteps(myVerb + ' - 2 letters + "ä" (verb type 9)')
                if verbType == 11:
                    self.printSteps(myVerb + ' - 2 letters + "e" (verb type 11)')
                switcher = {
                    0: "?",
                    1: verb[:len(verb)-1],
                    2: verb[:len(verb)-2],
                    3: verb[:len(verb)-2] + "e",
                    4: verb[:len(verb)-2] + "ä",
                    5: verb[:len(verb)-2] + "tse",
                    6: verb[:len(verb)-2] + "ne",
                    7: verb[:len(verb)-3] + "e",
                    9: verb[:len(verb)-2] + "ä",
                    11: verb[:len(verb)-2] + "e"
                }
            self.printSteps('    --> ' + switcher.get(verbType))
            return switcher.get(verbType)

    def gradatableStemFinder(self, verb):
        self.printSteps(Fore.CYAN + '\nGradatable Stem')
        verbType = self.verbTypeFinder(verb)
        myVerb = '    - ' + verb
        if verbType == 1:
                    self.printSteps(myVerb + ' - 1 letter (verb type 1) ')
        if verbType == 3:
                    self.printSteps(myVerb + ' - 3 letters (verb type 3) ')
        if verbType == 4:
                    self.printSteps(myVerb + ' - 2 letters (verb type 4) ')
        if verbType == 6:
                    self.printSteps(myVerb + ' - 2 letters (verb type 6) ')
        switcher = {
                0: "?",
                1: verb[:len(verb)-1], 
                3: verb[:len(verb)-3],
                4: verb[:len(verb)-2],
                6: verb[:len(verb)-2],
            }
        myReturn = str(switcher.get(verbType))
        # - consonant gradation cannot affect the -EPÄ prefix
        if myReturn.startswith('epä'):
            myReturn = myReturn[3:]
            self.printSteps('    - consonant gradation cannot affect the -EPÄ prefix. Removing it.')
        myString = myReturn
        if myString == 'None':
            myString = 'irrelevant to verb types created for this program'
        self.printSteps('    --> ' + myString + ' ') # the additional white space is to trick printSteps to think that it is not the same string as before (which can happen with "kirjoittaa", for example).
        return myReturn

    def verbConjugator(self, verb):
        self.printSteps(Fore.LIGHTMAGENTA_EX + '\nBasic Conjugation (without consonant gradation)')
        verbType = self.verbTypeFinder(verb)
        verbStrength = self.verbStrengthFinder(verb)
        stem = self.stemFinder(verb)
        self.printSteps('    - verb Vowel Strength is ' + Fore.LIGHTBLUE_EX + verbStrength + Fore.RESET + ': adding corresponding personal endings.')
        if verbStrength == "strong":
            conjugatedVerb = [stem + "n", stem + "t", stem + "", stem + "mme", stem + "tte", stem + "vat"]
        else:
            conjugatedVerb = [stem + "n", stem + "t", stem + "", stem + "mme", stem + "tte", stem + "vät"]

        # Careful: Olla case
        if verbType == 8:
            conjugatedVerb[2] = "on"
            conjugatedVerb[5] = "ovat"

        myStep = ''
        if verbType == 8:
            myStep += '    - exception for verb type 8: third and sixth persons are atypical\n'
        for i in range(6):
                myStep += '\n    ' + str(i+1) + ' - ' + conjugatedVerb[i]
        self.printSteps(myStep)
        return conjugatedVerb

    def isLetterAVowel(self, letter):
        if letter == "a" or letter == "ä" or letter == "e" or letter == "i" or letter == "o" or letter == "ö" or letter == "u" or letter == "y":
            return True
        else:
            return False

    def verbConjugatorWithGradation(self, verb):
        conjugatedVerb = self.verbConjugator(verb)
        oldConjugatedVerb = list(conjugatedVerb)
        stem = self.stemFinder(verb)
        gradatableStem = self.gradatableStemFinder(verb)
        verbType = self.verbTypeFinder(verb)
        verbTypeConsonantStrength = self.verbTypeConsonantStrengthFinder(verb)
        self.printSteps(Fore.GREEN + '\nConsonant Gradation')
        # "Note that consonant gradation affects only the last consonants of the verb stem". Bullshit!
        # (http://www.worddive.com/grammar/en/finnish-grammar/3-consonant-gradation-in-verbs/)
        # Counter example: Kuunnella –> kuuntelen
        # Instead, the rule seems to be:
        # Conditions for consonant gradation:
        # - affects only the last consonant(s) of the verb "gradatable stem"
        # - can't affect the first syllabe of the stem
        # - consonant couple includes all the adjacent consonants
        # - cannot affect the -EPÄ prefix
        #   (Ex: T in Katsoa doesn't gradate to D, because the consonant couple is actually not gradatable (TS)

        if verb in self.verbsBasedOnUngradatableWords:
            self.printSteps("   - this verb is based on a word that doesn't gradate.")
        else:
            # If the stem ends with a triple vowel, a "k" is added between the first and the second vowels of the trio.
            # This rule doesn't seem to affect verb type 2 and 5
            # Ex: Maata.
            if verbType != 2 and verbType != 5 and self.isLetterAVowel(stem[len(stem)-1]) and self.isLetterAVowel(stem[len(stem)-2]) and self.isLetterAVowel(stem[len(stem)-3]):
                self.printSteps("    - the stem ends with a triple vowel and the verb type is not 2 or 5\n        --> adding a k between the first and the second vowels of the trio.")
                for i in range(len(conjugatedVerb)):
                    conjugatedVerb[i] = conjugatedVerb[i][:len(stem)-2] + "k" + conjugatedVerb[i][len(stem)-2:]

            # verbs based on loan words which get gradated even if they shouldn't
            elif verb in self.verbsBasedOnLoanWordsWhichGradate.keys():
                self.printSteps("    - this verb belongs to the list of verbs based on loan words which get gradated when they wouldn't otherwise.")
                self.printSteps("        --> gradatable stem: " + gradatableStem)
                newStem = self.verbsBasedOnLoanWordsWhichGradate[verb][:len(self.verbsBasedOnLoanWordsWhichGradate[verb])]
                self.printSteps("        --> gradated stem: " + newStem)
                for i in range(len(conjugatedVerb)):
                    conjugatedVerb[i] = newStem + conjugatedVerb[i][len(verb)-2:]

            elif verbType == 1 or verbType == 3 or verbType == 4 or verbType == 6:
                self.printSteps("    - this verb belongs to the verb type 1, 3, 4 or 6, so it can be subject to consonant gradation.")
                # Plan:
                # - ignore the -EPÄ prefix in the search of consonant couples
                # - look the last consonant in the verb stem. Start at the end of the verb stem.
                # - check if the previous letter is a consonant too. Add it to the couple if it is
                # - check if the consonant couple is gradatable
                #   - if it is, gradate it with the function ConsonantCoupleGradator() and break the loop
                #   - if it is NOT, there is no gradation to be applied.

                # Look for the last consonant:
                consonantCouple = ""
                iterator = iter(range(len(gradatableStem)-1))
                for i in iterator:
                    # - look the last consonant in the verb stem. Start at the end of the verb stem.
                    if not self.isLetterAVowel(gradatableStem[len(gradatableStem)-i-1]):
                        consonantCouple = gradatableStem[len(gradatableStem)-i-1]
                        consonantCouplePosition = len(gradatableStem)-i-1
                        # - check if the previous letter is a consonant too. Add it to the couple if it is
                        if not self.isLetterAVowel(gradatableStem[len(gradatableStem)-i-2]):
                            consonantCouple = gradatableStem[len(gradatableStem)-i-2] + consonantCouple
                            consonantCouplePosition = len(gradatableStem)-i-2
                            next(iterator) # to ignore the next iteration of the loop, because we have just considered this letter already
                            # - check if the previous letter is a consonant too. Add it to the couple if it is
                            if not self.isLetterAVowel(gradatableStem[len(gradatableStem)-i-3]):
                                consonantCouple = gradatableStem[len(gradatableStem)-i-3] + consonantCouple
                                consonantCouplePosition = len(gradatableStem)-i-3
                    
                            # if consonant couple is RK-RJ or LK-LJ, check if next letter is a E. If not, this couple is not gradatable:
                            if consonantCouple in ('rk', 'rj', 'lk', 'lj') and gradatableStem[consonantCouplePosition+2] == 'e':
                                # Type-3 verbs do not follow this rule
                                if not verbType == 3:
                                    consonantCouple = consonantCouple + 'e'
                            # if consonant couple is HK-HJ, check if next letter is a E. If not, this couple is not gradatable:
                            elif consonantCouple in ('hk', 'hj') and gradatableStem[consonantCouplePosition+2] == 'e':
                                # Type-3 verbs do not follow this rule
                                if not verbType == 3:
                                    consonantCouple = consonantCouple + 'e'
                        #print ("Consonant couple found:", consonantCouple)
                        # - check if the consonant couple is gradatable
                        if not self.isConsonantCoupleGradatable(consonantCouple, verb):
                            #print ("This consonant couple is NOT gradatable with this verb type")
                            break # I thought that we had to check previous couples if the last one was not gradatable, but I was wrong. Do not continue, but break the for loop.
                        else:
                            consonantCoupleGradated = self.consonantCoupleGradator(consonantCouple, verb)
                            #print ("Gradated consonant couple:", consonantCoupleGradated)
                            if verbType == 1:     
                                self.printSteps("    - verb type 1: the gradation doesn't affect the third and sixth persons.")
                                if verb[:3] == 'epä':
                                    for i in range(len(conjugatedVerb)):
                                        if i != 2 and i != 5: # does NOT affect 3rd persons
                                            conjugatedVerb[i] = conjugatedVerb[i][:consonantCouplePosition+3] + consonantCoupleGradated + conjugatedVerb[i][consonantCouplePosition+len(consonantCouple)+3:]
                                else:
                                    for i in range(len(conjugatedVerb)):
                                        if i != 2 and i != 5: # does NOT affect 3rd persons
                                            conjugatedVerb[i] = conjugatedVerb[i][:consonantCouplePosition] + consonantCoupleGradated + conjugatedVerb[i][consonantCouplePosition+len(consonantCouple):]
                            else: # verb type 3, 4 or 6
                                self.printSteps("    - verb type 3, 4 and 6: the gradation affects every person.")
                                if verb[:3] == 'epä':
                                    for i in range(len(conjugatedVerb)):
                                        conjugatedVerb[i] = conjugatedVerb[i][:consonantCouplePosition+3] + consonantCoupleGradated + conjugatedVerb[i][consonantCouplePosition+len(consonantCouple)+3:]
                                else:
                                    for i in range(len(conjugatedVerb)):
                                        conjugatedVerb[i] = conjugatedVerb[i][:consonantCouplePosition] + consonantCoupleGradated + conjugatedVerb[i][consonantCouplePosition+len(consonantCouple):]
                            break
                    else:
                        continue

            elif verbType == 7:
                #print ("verb type 7 3-vowel case -> adding a k to the third persons")
                self.printSteps("   - verb type 7: adding a k to the third and the sixth persons between the first and the second of the 3 last vowels.")
                conjugatedVerb[2] = conjugatedVerb[2][:len(stem)-1] + "k" + conjugatedVerb[2][len(stem)-1:]
                conjugatedVerb[5] = conjugatedVerb[5][:len(stem)-1] + "k" + conjugatedVerb[5][len(stem)-1:]

            elif verbType == 2 or verbType == 5 or verbType == 8 or verbType == 9 or verbType == 10 or verbType == 11:
                self.printSteps("   - no consonant gradation for verb types 2, 5, 8, 9, 10 and 11.")
                # no consonant gration for these types
                pass

            else: # not Finnish verb
                conjugatedVerb = '?'

        if conjugatedVerb != oldConjugatedVerb:
            myStep = ''
            for i in range(6):
                    myStep += '\n    ' + str(i+1) + ' - ' + conjugatedVerb[i]
            self.printSteps(myStep)
        else:
            self.printSteps('    --> none  ')
        return conjugatedVerb

    def isConsonantCoupleGradatable(self, consonantCouple, verb):
        verbTypeConsonantStrength = self.verbTypeConsonantStrengthFinder(verb)
        if consonantCouple in self.consonantCoupleDictionaryStrong.keys() and verbTypeConsonantStrength == "Strong (verb type 1)":
            self.printSteps('    - ' + consonantCouple + ' is gradatable')
            return True
        elif consonantCouple in self.consonantCoupleDictionaryWeak.keys() and verbTypeConsonantStrength == "Weak (verb type 3, 4 or 6)":
            self.printSteps('    - ' + consonantCouple + ' is gradatable')
            return True
        else:
            self.printSteps('    - ' + consonantCouple + ' is NOT gradatable')
            return False

    def consonantCoupleGradator(self, consonantCouple, verb):
        verbTypeConsonantStrength = self.verbTypeConsonantStrengthFinder(verb)
        # Strong
        if verbTypeConsonantStrength == "Strong (verb type 1)":
            if consonantCouple in self.consonantCoupleDictionaryStrong.keys():
                gradation = str(self.consonantCoupleDictionaryStrong[consonantCouple])
                self.printSteps('    - ' + consonantCouple + ' --> ' + gradation)
                return gradation
        # Weak
        elif verbTypeConsonantStrength == "Weak (verb type 3, 4 or 6)":
            if consonantCouple in self.consonantCoupleDictionaryWeak.keys():
                gradation = str(self.consonantCoupleDictionaryWeak[consonantCouple])
                self.printSteps('    - ' + consonantCouple + ' --> ' + gradation)
                return gradation

    def verbConjugatorLastAdditions(self, verb):
        stem = self.stemFinder(verb)
        if not stem:
            self.printSteps('\n' + Fore.RED + "This verb couldn't be a Finnish verb. It doesn't fit into any of the verb types.")
        else:
            verbType = self.verbTypeFinder(verb)
            conjugatedVerb = self.verbConjugatorWithGradation(verb)
            newConjugatedVerb = list(conjugatedVerb)
            self.printSteps(Fore.LIGHTYELLOW_EX + '\nLast Additions')
            if verbType != 4 and verbType != 8 and verbType != 9:
                if not self.isLetterAVowel(newConjugatedVerb[2][-2]) or not self.isLetterAVowel(newConjugatedVerb[2][-1]):
                    self.printSteps("    - verb type is not 4, 8 or 9: doubling the last letter for the third person, unless there are already 2 vowels at the end.")
                    newConjugatedVerb[2] = newConjugatedVerb[2] + newConjugatedVerb[2][-1]
            if (verbType == 4 or verbType == 9) and verb[-3] != 'a' and verb[-3] != 'ä':
                self.printSteps("    - verb types 4 and 9: doubling last vowel for the third person, unless there is already twice the letter A.")
                newConjugatedVerb[2] = newConjugatedVerb[2] + stem[-1]
            if verb == 'liukua':
                self.printSteps("    - for the verb liukua, we need to add an apostrophe between both K, except for the the third and the sixth persons.")
                for i in range(len(newConjugatedVerb)):
                    if i != 2 and i != 5:
                        newConjugatedVerb[i] = newConjugatedVerb[i][:3] + "'" + newConjugatedVerb[i][3:]
            if verbType == 10:
                self.printSteps("    - verb type 10: adding a K after the third letter.")
                for i in range(len(newConjugatedVerb)):
                    newConjugatedVerb[i] = newConjugatedVerb[i][:3] + "k" + newConjugatedVerb[i][3:]

            if newConjugatedVerb == conjugatedVerb:
                self.printSteps('    --> no last addition')
            else:
                conjugatedVerb = newConjugatedVerb
                myStep = ''
                for i in range(6):
                        myStep += '\n    ' + str(i+1) + ' - ' + conjugatedVerb[i]
                self.printSteps(myStep)
            return conjugatedVerb          

    def askUserVerbToConjugate(self):
        while True:
            print("\nType a verb to conjugate:")
            verb = ""
            verb = input()
            verb = verb.lower()
            finalConjugatedVerb = self.verbConjugatorLastAdditions(verb)
            print("Conjugated verb (with consonant gradation): ", finalConjugatedVerb)

    def menu(self):
        while True:
            print(Fore.RED + '\nDebug menu')
            print('(You can type "menu" at any time to go back to the main menu)')
            print('\nType a verb:')
            verb = input()
            self.showSteps = True
            self.stepsAlreadyPrinted = []
            conjugatedVerb = self.verbConjugatorLastAdditions(verb)

    def main(self):
        #self.menu()
        return

if __name__=='__main__':
    Konjugaattori()