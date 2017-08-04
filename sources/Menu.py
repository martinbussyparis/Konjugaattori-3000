#!/usr/bin/env python3
import logging
from colorama import init
from colorama import Fore, Back, Style

import Updater, Konjugaattori, Profile, Exercise, TodayShelf

class Menu():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    logging.disable(logging.WARNING)
    myUpdater = Updater.Updater()
    myKonjugaattori = Konjugaattori.Konjugaattori()
    myProfile = Profile.Profile()
    myExercise = Exercise.Exercise()
    myTodayShelf = TodayShelf.TodayShelf()
    userName = False

    def __init__(self):
        self.main()

    def challengeKonjugaattori(self):
        while True:
            print('\nType a verb you would like to challenge Konjugaattori 3000 with (even made-up Finnish verbs should work):')
            verb = ''
            while len(verb) < 4:
                verb = input()
                if len(verb) < 4:
                    print('A Finnish verb cannot be shorter than 4 letters. Try again:')
            if verb == 'menu':
                self.menu()
            self.myKonjugaattori.showSteps = True
            self.myKonjugaattori.stepsAlreadyPrinted = []            
            self.myKonjugaattori.verbConjugatorLastAdditions(verb)

    def listConsonantCouples(self):
        strong = self.myKonjugaattori.consonantCoupleDictionaryStrong
        weak = self.myKonjugaattori.consonantCoupleDictionaryWeak
        print(Fore.MAGENTA + 'Strong consonants:')
        for k, v in sorted(strong.items()):
            print(k.ljust(4) + ' --> ' + v)
        print('\n' + Fore.CYAN + 'Weak consonants:')
        for k, v in sorted(weak.items()):
            print(k.ljust(4) + ' --> ' + v)

    def conjugationRules(self):
        print(Fore.LIGHTBLUE_EX + '\nVerb Type')
        verbTypes = ['a/ä', 'da/dä', 'la/lä/ra/rä/na/nä', 'ta/tä or -eta/etä and do not mean a change of state',
                     'ita/itä', 'eta/etä and means a change of state', 'hda/hdä (nähdä, tehdä, etc.)', 'olla',
                     'vitä (hävitä, levitä, selvitä, etc.)', 'juosta', 'sta/stä (type 3-verbs which do not get gradated)']
        for i in range(len(verbTypes)):
            if i == 0:
                print('\nCommon verb types:')
            if i == 6:
                print('\nA few more verb types were created for this program to fit all the irregular verbs:')
            print(str('- ' + str(i + 1)).ljust(7) + str(': ends with -' + verbTypes[i]).rjust(7))
        print("\nExamples of -ETA/ETÄ verbs which get conjugated like verb type-4 verbs because they don't mean a change of state:")
        for i in self.myKonjugaattori.etaVerbsType4:
            print('- ' + i)
        print(Fore.LIGHTBLUE_EX + '\nVerb Vowel Strength\n')
        print('- Strong'.ljust(15) + ': contains "a", "o" or "u"'.rjust(15))
        print('- Weak'.ljust(15) + ': does NOT contain any "a", "o" or "u"'.rjust(15))
        print(Fore.LIGHTBLUE_EX + '\nStem')
        print('\nIf verb vowel strength is ' + Fore.LIGHTBLUE_EX + 'strong:')
        verbTypes = {'01': '1 letter',
                     '02': '2 letters',
                     '03': '2 letters + "e"',
                     '04': '2 letters + "a"',
                     '05': '2 letters + "tse"',
                     '06': '2 letters + "ne"',
                     '07': '3 letters + "e"',
                     '08': '2 letters + "e"',
                     '10': '2 letters + "e"',
                     '11': '2 letters + "e"',}
        for k, v in sorted(verbTypes.items()):
            if str(k).startswith('0'):
                k = k[1:]
            print(('- verb type ' + k).ljust(20) + (': stem = verb - ' + v).rjust(20))
        print('\nIf verb vowel strength is ' + Fore.LIGHTBLUE_EX + 'weak:')
        verbTypes = {'01': '1 letter',
                     '02': '2 letters',
                     '03': '2 letters + "e"',
                     '04': '2 letters + "ä"',
                     '05': '2 letters + "tse"',
                     '06': '2 letters + "ne"',
                     '07': '3 letters + "e"',
                     '09': '2 letters + "ä"',
                     '11': '2 letters + "e"',}
        for k, v in sorted(verbTypes.items()):
            if str(k).startswith('0'):
                k = k[1:]
            print(('- verb type ' + k).ljust(20) + (': stem = verb - ' + v).rjust(20))
        print(Fore.LIGHTMAGENTA_EX + '\nBasic Conjugation (without consonant gradation)')
        print('\nAddition of the personal endings:')
        pronouns = ['minä', 'sinä', 'hän/se', 'me', 'te', 'he/ne']
        endings = ['n', 't', '', 'mme', 'tte', 'vat/vät']
        for i in range(6):
            print('- ' + pronouns[i].ljust(10) + ': '.rjust(10) + endings[i])
        print(Fore.CYAN + '\nGradatable Stem\n')
        verbTypes = {'1': '1 letter',
                     '3': '3 letters',
                     '4': '2 letters',
                     '6': '2 letters'}
        for k, v in sorted(verbTypes.items()):
            print(('- verb type ' + k).ljust(20) + (': gradatable stem = verb - ' + v).rjust(20))
        print("\n- Verb types 2 and 5 are not subject to consonant gradation")
        print("- The gradatable stem is irrelevant to the special verb types created for this program")
        print("- The consonant gradation does not affect the -epä prefix, so it has to be removed to form the gradatable stem")
        print(Fore.CYAN + '\nVerb Type Consonant Strength')
        verbTypes = {'1': 'strong',
                     '3, 4, 6': 'weak',
                     '2, 5': 'no consonant gradation for verb types 2 and 5',
                     'special': 'irrelevant to special verb types created for this program'}
        for k, v in sorted(verbTypes.items()):
            print('- verb type(s) ' + k.ljust(20) + ': ' + v)
        print(Fore.GREEN + '\nConsonant Gradation - Main Rules\n')
        print("Basic rules of consonant gradation:")
        rules = ["Consonant gradation only affects verb types 1, 3, 4, 6 and 7",
                'Consonant gradation affects only the last consonant(s) of the "gradatable stem"',
                "Consonant gradation can't affect the first syllabe of the stem",
                'Consonants must be only considered as groups of adjacent consonants (example: to check if "katsoa" is gradatable, look at "ts" instead of "t")',
                "Consonant gradation doesn't affect the -EPÄ prefix",
                "Consonant gradation affects all persons for verb types 3, 4 and 6, but doesn't affect the third persons (singular and plural) for the verb type 1",]
        for i in rules:
            print('- ' + i)
        print("\nThese verbs would get gradated otherwise, but they are based on Finnish words which don't get gradated (because most of them are loan words from other languages):")
        for i in self.myKonjugaattori.verbsBasedOnUngradatableWords:
            print('- ' + i)
        print("\nThese verbs would NOT get gradated otherwise, but they are based on Finnish words which get gradated (because most of them are loan words from other languages):")
        for k, v in sorted(self.myKonjugaattori.verbsBasedOnLoanWordsWhichGradate.items()):
            print('- ' + k.ljust(15) + '- gradated verb stem: ' + v)
        print(Fore.GREEN + '\nConsonant Gradation - Consonant Couples')
        print('\nList of all the consonant couples')
        print("\nIf the verb type consonant strength is" + Fore.MAGENTA + " strong:")
        for k, v in sorted(self.myKonjugaattori.consonantCoupleDictionaryStrong.items()):
            print(k.ljust(4) + ' --> ' + v)
        print("\nIf the verb type consonant strength is" + Fore.CYAN + " weak:")
        for k, v in sorted(self.myKonjugaattori.consonantCoupleDictionaryWeak.items()):
            print(k.ljust(4) + ' --> ' + v)
        print("\nThese consonant couples are the only ones to also contain a vowel. Also, they don't affect verb type-3 verbs:")
        eCouples = {'lke': 'lje', 'rke': 'rje', 'hke': 'hje', 'lje': 'lke', 'rje': 'rke', 'hje': 'hke'}
        for k, v in sorted(eCouples.items()):
            print('- ' + k.ljust(10) + ': ' + v)
        print("\nMost consonant couples go both ways, from strong to weak and from weak to strong, but some go only one way:")
        print("- One-way example:")
        print("    --> rk - r (strong to weak only)")
        print(Fore.GREEN + '\nConsonant Gradation - K Addition\n')
        print('The addition of the letter K (which is different to the doubling of the letter K) is sometimes due to consonant gradation, but it is really hard to detect. Here are the rules:')
        print('\n- If the verb stem ends with a triple vowel and the verb type is not 2 or 5, a "K" is added between the first and the second vowels of the trio.')
        print('    --> Example: Maata - Verb stem: Maaa - Gradated verb stem: Makaa')
        print("\n- For all verb type-7 verbs, the letter K must be added to the third persons (singular and plural) between the first and the second letter of the vowel trio")
        print('    --> Example: Nähdä - Verb stem: Näe - Gradated verb stem: Näke')
        print("\nOther cases of addition of the letter K exist, but they don't belong to consonant gradation, so they will be considered at the next step.")
        print(Fore.LIGHTYELLOW_EX + '\nLast Additions')
        print("\n- If the verb type is not 4, 8 or 9: the last letter for the third person must be doubled, unless there are already 2 vowels at the end.")
        print('    --> Example: Nukku --> Nukkuu (Infinitive: Nukkua)')
        print("\n- If the verb type is 4 or 9: last vowel for the third person must be doubled, unless there is already twice the letter A.")
        print('    --> Example: Häviä --> Häviää (Infinitive: Hävitä)')
        print("\n- If the verb is 'liukua', an apostrophe is added between both K, except for the the third and the sixth persons.")
        print("    --> Example: Liuun --> Liu'un")
        print("\n- If the verb type is 10: a K must be added after the third letter.")
        print('    --> Example: Juosen --> Juoksen (Infinitive: Juosta)')

    def menu(self):
        while True:
            featureList = (
                Fore.CYAN + 'Exercise',
                Fore.GREEN + 'Conjugation rules',
                Fore.GREEN + 'List of consonant couples',
                Fore.GREEN + 'Challenge Konjugaattori 3000 with any verb',
                Fore.LIGHTBLUE_EX + 'See your progress',
                Fore.LIGHTBLUE_EX + 'Reset your whole progression',
                Fore.RED + 'Scoreboard'
                )
            print(Fore.LIGHTBLUE_EX + '\nMain menu - ' + Fore.LIGHTYELLOW_EX + self.userName)
            print('(You can type "menu" at any time to go back to the main menu)')
            print('\nType the number of the feature you want to use:')
            for i in range(len(featureList)):
                print (i, '-', featureList[i])
            featureNumber = input()
            if featureNumber == '0':
                self.myExercise.askUserToConjugate(self.userName)
            elif featureNumber == '1':
                self.conjugationRules()
            elif featureNumber == '2':
                self.listConsonantCouples()
            elif featureNumber == '3':
                self.challengeKonjugaattori()
            elif featureNumber == '4':
                self.myProfile.printPoolsStatistics()
            elif featureNumber == '5':
                # User confirmation
                print('Are you sure you want to reset your progression? All the verbs would go back to the first pool.')
                print('0 - Cancel')
                print('1 - Confirm')
                userInput = ''
                while True:
                    userInput = input()
                    if userInput == '0':
                        break
                    elif userInput == '1':
                        self.myProfile.resetVerbPools()
                        self.myTodayShelf.resetTodayShelf(self.userName)
                        break
            elif featureNumber == '6':
                self.myProfile.printScores(self.myExercise.getVerbList())

    def main(self):
        if self.myUpdater.checkForUpdates():
            self.userName = self.myProfile.profileCheck()
            if self.userName:
                self.myTodayShelf.isShelfUpToDate(self.userName)
                self.menu()

if __name__=='__main__':
    Menu()