#!/usr/bin/env python3
import logging, shelve, datetime as DT, os
from colorama import init
from colorama import Fore, Back, Style

import Profile

class TodayShelf():
    myProfile = Profile.Profile()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    logging.disable(logging.WARNING)
    myAppDataFolder = os.getenv('APPDATA') + '\\Konjugaattori 3000\\'
    userName = 'test'

    def __init__(self):
        self.main()

    def addVerbToTodayShelf(self, verb, userName):
        if os.path.isfile(os.path.join(self.myAppDataFolder + userName + '//todayShelf.dat')):
            logging.warning('Checking if verb is not already in Today Shelf...')
            if not self.isVerbInTodayShelf(verb, userName):
                shelfFile = shelve.open(os.path.join(self.myAppDataFolder + userName + '//todayShelf'), writeback = True)
                shelfFile['verbsRisenToday'].append(verb)
                shelfFile.close()
                logging.warning('Verb added to Today Shelf')
            else:
                logging.warning('Verb is already in Today Shelf.')
        else:
            logging.warning('Shelf file does not exist')
            self.resetTodayShelf(userName)
            self.addVerbToTodayShelf(verb, userName)

    def formatDateOrTime(self, toFormat): # Formatting date and time to avoid bugs
        if len(toFormat) == 0:
            toFormat = "00"
        if len(toFormat) == 1:
            toFormat = "0" + toFormat
        return toFormat

    def getTodayString(self):
        dateTimeNow = DT.datetime.now ()
        month = self.formatDateOrTime(str(dateTimeNow.month))
        day = self.formatDateOrTime(str(dateTimeNow.day))
        dateString = str(dateTimeNow.year) + month + day
        return dateString

    def resetTodayShelf(self, userName):
        shelfFile = shelve.open(os.path.join(self.myAppDataFolder + userName + '//todayShelf'), writeback = True)
        shelfFile['verbsRisenToday'] = []
        today = self.getTodayString()
        shelfFile['today'] = [today]
        shelfFile.close()
        logging.warning('Today shelf reset')

    def isShelfUpToDate(self, userName):
        if os.path.isfile(os.path.join(self.myAppDataFolder + userName + '//todayShelf.dat')):
            shelfFile = shelve.open(os.path.join(self.myAppDataFolder + userName + '//todayShelf'))
            today = self.getTodayString()
            if shelfFile['today'][0] == today:
                shelfFile.close()
                logging.warning('Shelf file exists')
                return True
            else:
                shelfFile.close()
                logging.warning('Shelf file exists')
                return False
        else:
            logging.warning('Shelf file does NOT exist')
            self.resetTodayShelf(userName)
            return False

    def isVerbInTodayShelf(self, verb, userName):
        if os.path.isfile(os.path.join(self.myAppDataFolder + userName + '//todayShelf.dat')):
            shelfFile = shelve.open(os.path.join(self.myAppDataFolder + userName + '//todayShelf'))
            if verb in shelfFile['verbsRisenToday']:
                return True
            else:
                return False
            shelfFile.close()
        else:
            logging.warning('Shelf file does not exist')
            self.resetTodayShelf(userName)
            return False

    def menu(self):
        #self.myProfile.profileCheck()
        while True:
            featureList = (
                'addVerbToTodayShelf', 
                'resetTodayShelf',
                'isShelfUpToDate',
                'isVerbInTodayShelf',
                )
            print(Fore.RED + '\nDebug menu')
            print('(You can type "menu" at any time to go back to the main menu)')
            print('\nType the number of the feature you want to use:')
            for i in range(len(featureList)):
                print (i, '-', featureList[i])
            featureNumber = input()
            if featureNumber == '0':
                self.addVerbToTodayShelf('juoda', self.userName)
            elif featureNumber == '1':
                self.resetTodayShelf(self.userName)
            elif featureNumber == '2':
                print(self.isShelfUpToDate(self.userName))
            elif featureNumber == '3':
                print(self.isVerbInTodayShelf('juoda', self.userName))

    def main(self):
        #self.menu()
        pass

if __name__=='__main__':
    TodayShelf()