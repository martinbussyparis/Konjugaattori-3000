#!/usr/bin/env python3
import logging, os, requests, bs4, operator, getpass
from colorama import init
from colorama import Fore, Back, Style
from passlib.hash import pbkdf2_sha256

class Profile():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    logging.disable(logging.WARNING)
    myAppDataFolder = os.getenv('APPDATA') + '\\Konjugaattori 3000\\'
    userName = ''
    userDirectory = ''
    poolAmount = 4
    poolName = ['Not learnt           ', 'Started learning     ', 'Almost learnt        ', 'Permanently learnt   ']
    poolDescription = ['never answered correctly', 'answered correctly once', 'answered correctly twice', 'answered correctly three times']
    userNames = []
    passwords = {}

    def __init__(self):
        init(autoreset=True)
        self.main()

    def defineUserName(self, userName):
        self.userName = userName

    def printPoolsStatistics(self):
        poolList = self.readPools()
        print('\nThere are', str(self.poolAmount), 'pools of verbs. Here are how many verbs each of them currently contains:')
        colors = [Fore.RED, Fore.MAGENTA, Fore.LIGHTBLUE_EX, Fore.CYAN]
        for i in range(self.poolAmount):
            print(i, '-', colors[i] + self.poolName[i] + Fore.RESET + ': ' + str(len(poolList[i])) + ' verbs     (' + self.poolDescription[i] + ')')
        return

    def riseVerbInPools(self, verb, ignore=False):
        poolList = self.readPools()
        # Find which pool the verb is in:
        for i in range(self.poolAmount):
            if verb in poolList[i]:
                poolContainingVerb = i
                break
        # Rise the verb if not already in the top pool:
        if poolContainingVerb != self.poolAmount-1:
            if not ignore:
                self.addToPool(verb, poolContainingVerb+1, poolList)
            else:
                self.addToPool(verb, 3, poolList)
            self.removeFromPool(verb, poolContainingVerb, poolList)
        self.uploadScore()

    def printPools(self, poolList):
        for i in range(self.poolAmount):
            print(poolList[i])

    def readPools(self):
        poolList = []
        for i in range(self.poolAmount):
            self.userDirectory = os.path.join(self.myAppDataFolder + self.userName)
            pool = open(self.userDirectory + '//userVerbPool_0' + str(i) + '.txt')
            poolList.append(pool.readlines())
            for j in range(len(poolList[i])):
                if '\n' in poolList[i][j]:
                    poolList[i][j] = poolList[i][j][:len(poolList[i][j])-1]
            pool.close()
        return poolList

    def addToPool(self, verb, poolNumber, poolList):
        poolFile = open(self.userDirectory + '//userVerbPool_0' + str(poolNumber) + '.txt', 'w')
        if verb not in poolList[poolNumber]:
            poolList[poolNumber].append(verb)
            print('Added "' + verb + '" to pool ' + str(poolNumber))
        poolString = '\n'.join(poolList[poolNumber])
        poolFile.write(poolString)
        poolFile.close()

    def removeFromPool(self, verb, poolNumber, poolList):
        poolFile = open(self.userDirectory + '//userVerbPool_0' + str(poolNumber) + '.txt', 'w')
        if verb in poolList[poolNumber]:
            del poolList[poolNumber][poolList[poolNumber].index(verb)]
        poolString = '\n'.join(poolList[poolNumber])
        poolFile.write(poolString)
        poolFile.close()

    def resetVerbPools(self):
        verbList = []
        file = open('data/verbs.txt')
        verbList = file.readlines()
        for i in range(len(verbList)):
            if '\n' in verbList[i]:
                verbList[i] = verbList[i][:len(verbList[i])-1]
        file.close()
        verbListString = '\n'.join(verbList)
        # Populate first pool
        pool_00 = open(self.userDirectory + '//userVerbPool_00.txt', 'w')
        pool_00.write(verbListString)
        pool_00.close()
        # Empty all the others
        for i in range(self.poolAmount-1):
            pool = open(self.userDirectory + '//userVerbPool_0' + str(i+1) + '.txt', 'w')
            pool.write('')
            pool.close()
        self.uploadScore()
        print('All verb pools have been reset.')

    def getOnlineScores(self):
        try:
            pageRequest = requests.get('http://martinbussy.com/konjugaattori_3000/getscores.php', timeout=3.05)
        except requests.exceptions.ConnectionError:
            print('Connection Error. Your internet connection is probably down. Cannot get online scores.')
            scores = False
            return scores
        except requests.exceptions.Timeout:
            print('Timeout Error. The online database is down. Cannot get online scores.')
            scores = False
            return scores
        pageRequest.text
        soup = bs4.BeautifulSoup(pageRequest.text, "html.parser")
        scores = str(soup)
        scores = scores.split('_')[:-1]
        for i in range(len(scores)):
            if i % 2 != 0:
                scores[i] = scores[i].split('|')
        for i in range(len(scores)):
            if i % 2 != 0:
                for j in range(len(scores[i])):
                    scores[i][j] = scores[i][j].split(',')
        for i in range(len(scores)):
            if i % 2 != 0:
                for j in range(len(scores[i])):
                    for k in range(len(scores[i][j])):
                        if scores[i][j][k] == '':
                            del scores[i][j][k]
        scores = dict(scores[i:i+2] for i in range(0, len(scores), 2))
        return scores        

    def calculateScores(self):
        scores = self.getOnlineScores()
        if scores:
            # Convert values to int:
            for v in scores.values():
                for i in range(len(v)):
                    v[i] = len(v[i])
            # Weigh scores per pool:
            for v in scores.values():
                for i in range(len(v)):
                    v[i] = v[i]*i
            # Add up all pool scores:
            for k, v in scores.items():
                sum = 0
                for i in range(len(v)):
                    sum += v[i]
                scores[k] = sum
        return scores

    def printScores(self, verbList):
        scores = self.calculateScores()
        if scores:
        # Get the length of the longest name:
            longestNameLength = 0
            for k in scores.keys():
                if len(k) > longestNameLength:
                    longestNameLength = len(k)
            scores = sorted(scores.items(), key=operator.itemgetter(1)) # makes a sorted list of tuples from the dictionary
            scores = scores[::-1] # reverse order
            # Convert list of tuples to list of strings:
            newScores = []
            for i in range(len(scores)):
                for j in range(len(scores[i])):
                    newScores.append(scores[i][j])
            scores = newScores
            print('\n')
            print(' Scores '.center(longestNameLength + 13, '=') + '\n')
            # Prints explanation:
            print('Score calculation:')
            print('Pool 0' + ': number of verbs '+ Fore.RED + 'x 0')
            print('Pool 1' + ': number of verbs '+ Fore.MAGENTA + 'x 1')
            print('Pool 2' + ': number of verbs '+ Fore.LIGHTBLUE_EX + 'x 2')
            print('Pool 3' + ': number of verbs '+ Fore.CYAN + 'x 3\n')
            verbNumber = len(verbList)
            maxScore = verbNumber * 3
            print('Current number of verbs: ' + str(verbNumber))
            print('Current maximum possible score: ' + str(maxScore) + '\n')
            print('Current Master of Finnish Conjugation: ' + Fore.GREEN + scores[0] + '\n')
            if len(scores) == 0:
                print('No one has learnt anything yet. What a bunch of noobs.')
            else:
                for i in range(len(scores)):
                    if i % 2 == 0:
                        if i == 0:
                            print(scores[i].ljust(longestNameLength + 5, '.') + Fore.GREEN + str(scores[i+1]).rjust(8))
                        else:
                            print(scores[i].ljust(longestNameLength + 5, '.') + str(scores[i+1]).rjust(8))
        else:
            pass

    def uploadScore(self):
        pools = self.readPools()
        newPools = []
        for p in pools:
            newPools.append(','.join(p))
        pools = newPools
        verbs = '&pool00=' + pools[0] + '&pool01=' + pools[1] + '&pool02=' + pools[2] + '&pool03=' + pools[3]
        try:
            pageRequest = requests.get('http://martinbussy.com/konjugaattori_3000/savescores.php?name=' + self.userName + verbs, timeout=3.05)
        except requests.exceptions.ConnectionError:
            print('Connection Error. Your internet connection is probably down. Score not uploaded.')
        except requests.exceptions.Timeout:
            print('Timeout Error. The online database is down. Score not uploaded.')

    def getUserNames(self):
        #print('Getting online profiles...')
        try:
            pageRequest = requests.get('http://martinbussy.com/konjugaattori_3000/getpasswords.php', timeout=3.05)
            pageRequest.text
            soup = bs4.BeautifulSoup(pageRequest.text, "html.parser")
            table = str(soup).split('|')[:-1]
            self.userNames = []
            for i in range(len(table)):
                if i % 2 == 0:
                    self.userNames.append(table[i].lower())
            self.passwords = dict(table[i:i+2] for i in range(0, len(table), 2))
        except requests.exceptions.ConnectionError:
            print('Connection Error. Your internet connection is probably down. Cannot get online profiles.')
        except requests.exceptions.Timeout:
            print('Timeout Error. The online database is down. Cannot get online profiles.')

    def profileCheck(self):
        while True:
            featureList = (
                'Use an existing profile', 
                'Create a new profile'
                )
            print(Fore.LIGHTBLUE_EX + '\nProfile')
            for i in range(len(featureList)):
                print (i, '-', featureList[i])
            featureNumber = input()
            if featureNumber == '0':
                if self.profileLoad():
                    break
            elif featureNumber == '1':
                if self.profileCreate():
                    break
        return self.userName

    def profileLoad(self):
        while True:
            print("\nWhat is your user name?")
            self.userName = input()
            if not self.userName.isalnum():
                print("Your username must contain only letters and numbers and can't be empty")
                continue
            else:
                # Check if the user exists locally:
                profileExistenceLocal = os.path.isdir(self.myAppDataFolder + self.userName)
                if profileExistenceLocal:
                    print('Welcome back ' + Fore.LIGHTYELLOW_EX + self.userName + Fore.RESET + '!')
                    if self.isPasswordCorrect():
                        if self.checkLatestProfile():
                            return True
                            break
                else:
                    print("The user name " + self.userName + " doesn't exist on this computer. Let's check if it exists in the online database...")
                    # Check if the user exists online:
                    if self.userName.lower() in self.userNames:
                        print('The user name ' + self.userName + ' could be found in the online database.')
                        self.downloadOnlineProfile(self.userName)
                        if self.isPasswordCorrect():
                            return True
                            break
                    else:
                        print('The profile ' + self.userName + ' cannot be found on this computer or online.')
                        return False

    def downloadOnlineProfile(self, profileName):
        # Download the verb pools:
        print('Downloading your verb pools...')
        verbs = self.getOnlineScores()
        if verbs:
            verbs = verbs.get(self.userName)
            for i in range(len(verbs)):
                verbs[i] = '\n'.join(verbs[i])
            self.userDirectory = os.path.join(self.myAppDataFolder + self.userName)
            # Create folders if needed (Konjugaattori 3000 included!)
            if not os.path.exists(self.userDirectory):
                os.makedirs(self.userDirectory)
            # Delete old content:
            for file in os.listdir(self.userDirectory):
                filePath = os.path.join(self.userDirectory, file)
                if os.path.isfile(filePath):
                    os.unlink(filePath)
            # Creating new content:
            for i in range(self.poolAmount):
                pool = open(self.userDirectory + '//userVerbPool_0' + str(i) + '.txt', 'w')
                pool.write(verbs[i])
                pool.close()
            print('Downloaded.')
            # Download the password:
            print('Saving your hashed password...')
            passwordFile = open(os.path.join(self.userDirectory + '\\password.txt'), 'w')
            passwordFile.write(self.passwords.get(self.userName))
            passwordFile.close()
            print('Saved.')
        else:
            print('Online profile download failed.')

    def checkLatestProfile(self): # Determines which one of the local profile and the online profile is the latest one and replace the local one if needed
        if self.userNames:
            onlineProfileExists = self.userName.lower() in self.userNames
            if onlineProfileExists:
                print("\nYour profile also exists in the online database. Let's check your score on both profiles...")
                # Checking local score:
                poolList = self.readPools()
                localScore = 0
                for i in range(self.poolAmount):
                    localScore += len(poolList[i]) * i
                # Checking online score:
                scores = self.calculateScores()
                onlineScore = scores.get(self.userName)
                # Compare both:
                if localScore == onlineScore:
                    print("The local score and the online score are the same. You're good to go.")
                else:
                    # Asking user which one to keep:
                    print("Local score: " + str(localScore))
                    print("Online score: " + str(onlineScore))
                    print("Which one do you want to keep? The other one will be replaced.")
                    answer = ''
                    while answer != 'local' and answer != 'online':
                        print("Type 'local' or 'online':")
                        answer = input()
                    if answer == 'local':
                        print('Replacing online version with local version...')
                        self.uploadScore()
                    else:
                        print('Replacing local version with online version...')
                        self.downloadOnlineProfile(self.userName)
            else: # Online profile doesn't exist. Let's create it:
                print('Uploading local profile...')
                self.uploadScore()
                passwordFile = open(os.path.join(self.userDirectory + '\\password.txt'))
                hash = passwordFile.read()
                passwordFile.close()
                try:
                    pageRequest = requests.get('http://martinbussy.com/konjugaattori_3000/savepassword.php?name=' + self.userName + '&password=' + hash, timeout=3.05)
                except requests.exceptions.ConnectionError:
                    print('Connection Error. Your internet connection is probably down. Cannot upload local profile.')
                except requests.exceptions.Timeout:
                    print('Timeout Error. The online database is down. Cannot upload local profile.')
                print('Local profile uploaded.')
            return True
        else:
            # No internet connection
            return True

    def isPasswordCorrect(self):
        self.userDirectory = os.path.join(self.myAppDataFolder + self.userName)
        passwordFile = open(os.path.join(self.userDirectory + '\\password.txt'))
        hash = passwordFile.read()
        while True:
            print('\nEnter your password:')
            password = getpass.getpass()
            if pbkdf2_sha256.verify(password, hash):
                return True
            else:
                print('\nWrong password')
                continue

    def profileCreate(self):
        while True:
            print("\nPlease choose a user name:")
            myInput = input()
            if not myInput.isalnum():
                print("Your username must contain only letters and numbers and can't be empty")
                continue
            else:
                self.userName = myInput
                # Check if this user exists locally:
                profileExistenceLocal = os.path.isdir(self.myAppDataFolder + self.userName)
                if profileExistenceLocal:
                    print('The user name ' + self.userName + ' already exists on this computer. Please choose another one.')
                else:
                    print("The user name " + self.userName + " doesn't exist on this computer. Let's check if it exists in the online database...")
                    # Check if the user exists online:
                    if self.userName.lower() in self.userNames:
                        print('The user name ' + self.userName + ' already exists in the online database. Please choose another one.')
                    else:
                        print('The user name ' + self.userName + ' does not exist in the online database. You may use this one.')
                        while True:
                            print('Please choose a password:')
                            passwordA = getpass.getpass()
                            print('Type it one more time:')
                            passwordB = getpass.getpass()
                            if passwordB != passwordA:
                                print('You have just typed two different passwords. Try again.')
                                continue
                            else:
                                break
                        # Create new profile:
                        print('Creating new profile...')
                        self.userDirectory = os.path.join(self.myAppDataFolder + self.userName)
                        os.makedirs(self.userDirectory)
                        passwordFile = open(os.path.join(self.userDirectory + '\\password.txt'), 'w')
                        hash = pbkdf2_sha256.hash(passwordA)
                        passwordFile.write(hash)
                        passwordFile.close()
                        try:
                            pageRequest = requests.get('http://martinbussy.com/konjugaattori_3000/savepassword.php?name=' + self.userName + '&password=' + hash, timeout=3.05)
                        except requests.exceptions.ConnectionError:
                            print('Connection Error. Your internet connection is probably down. Cannot upload new profile.')
                        except requests.exceptions.Timeout:
                            print('Timeout Error. The online database is down. Cannot upload new profile.')
                        self.resetVerbPools()
                        self.uploadScore()
                        self.resetVerbPools()
                        print('Profile created. Welcome ' + Fore.LIGHTYELLOW_EX + self.userName + Fore.RESET + '!\nPlease remember your user name and your password.')
                        return True

    def menu(self):
        while True:
            featureList = (
                'profileCreate', 
                'profileLoad',
                'profileCheck',
                'saveScore',
                'printScores',
                'resetVerbPools',
                'getUserNames'
                )
            print(Fore.RED + '\nDebug menu - Profile')
            print('(You can type "menu" at any time to go back to the main menu)')
            print('\nType the number of the feature you want to use:')
            for i in range(len(featureList)):
                print (i, '-', featureList[i])
            featureNumber = input()
            if featureNumber == '0':
                self.profileCreate()
            elif featureNumber == '1':
                self.profileLoad()
            elif featureNumber == '2':
                self.profileCheck()  
            elif featureNumber == '3':
                self.uploadScore()
            elif featureNumber == '4':
                self.printScores()
            elif featureNumber == '5':
                self.resetVerbPools(True)
            elif featureNumber == '6':
                self.getUserNames()

    def main(self):
        self.getUserNames()
        #self.menu()
        pass

if __name__=='__main__':
    Profile()