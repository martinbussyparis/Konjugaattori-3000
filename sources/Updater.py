#!/usr/bin/env python3
import logging
import requests
import os
import sys
import subprocess
import bs4

class Updater():

    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    logging.disable(logging.WARNING)
    currentVersion = '3018.1'

    def __init__(self):
        self.main()

    def checkForUpdates(self):
        print('Checking for updates...')
        latestVersion = None
        try:
            pageRequest = requests.get('http://martinbussy.com/konjugaattori-3000/', timeout=3.05)
            pageRequest.text
            pageRequest.status_code
            pageRequest.raise_for_status()
            soup = bs4.BeautifulSoup(pageRequest.text, "html.parser")
            h3Elements = soup.select('h3[style]')
            latestVersion = str(h3Elements[0])
            latestVersion = latestVersion[32:]
            latestVersion = latestVersion.replace(' (latest)</h3>', '')
            print('Current version: ' + self.currentVersion)
            print('Latest version: ' + latestVersion)
        except requests.exceptions.ConnectionError:
            print('Connection Error. Your internet connection is probably down. Impossible to check the latest version: skipping update checking.')
        except requests.exceptions.Timeout:
            print('Timeout Error. The website is down. Impossible to check the latest version: skipping update checking.')
        if latestVersion == None:
            return True
        else:
            if latestVersion == self.currentVersion:
                print('Already up to date.')
                return True
            else:
                print('There is a new version of Konjugaattori 3000 to download!')
                # Check that we are running from an install directory and not from the source directory:
                if os.path.exists('Exercise.py'):
                    print('Update impossible. The current directory is the source one!')
                    return True
                else:
                    try: 
                        file = self.downloadInstallFile()
                        if file != None:
                            self.installUpdate(file)
                    except:
                        print('Impossible to check the latest version: skipping update checking.')
                        print("Unexpected error:", sys.exc_info()[0])

    def downloadInstallFile(self):
        print('\nDownloading update...')
        try:
            print(self.getReleaseNotes())
        except UnicodeEncodeError:
            print('There are forbidden characters in the release notes. Tell Martin to fix these! Cannot get release notes.')
        try:
            res = requests.get('http://martinbussy.com/wp-content/uploads/2017/03/Konjugaattori_3000.zip', timeout=3.05)
            res.raise_for_status()
            file = os.path.join(os.environ['USERPROFILE'] + '\Desktop' + '\Konjugaattori_3000.zip')
            print('---\nPath:', file)
            if os.path.exists(file):
                print('There is an old update on your desktop. Deleting it...')
                os.remove(file)
                print('Old update delete.')
            playFile = open(file, 'wb')
            for chunk in res.iter_content(100000):
                playFile.write(chunk)
            playFile.close()
            print('Update downloaded.')
            return file
        except requests.exceptions.HTTPError:
            print('Cannot download. Does the file exist on the website?')
        except requests.exceptions.ConnectionError:
            print('Connection Error. Your internet connection is probably down. Cannot download.')
        except requests.exceptions.Timeout:
            print('Timeout Error. The website is down. Cannot download.')

    def installUpdate(self, file):
        print('\n*** Instructions ***')
        print("- Extract the new archive and run the new shortcut 'Konjugaattori 3000.lnk'")
        print("- Don't worry, your progression has been saved.")
        print('\nClosing this instance of the program...')
        os._exit(1)

    def getReleaseNotes(self):
        print('Getting Release Notes...')
        try:
            pageRequest = requests.get('http://martinbussy.com/konjugaattori-3000/', timeout=3.05)
            pageRequest.text
            pageRequest.status_code
            pageRequest.raise_for_status()
            soup = bs4.BeautifulSoup(pageRequest.text, "html.parser")
            elements = soup.find_all()
            startFound = False
            for i in range(len(elements)):
                if 'Release notes' in elements[i] and not startFound:
                    startIndex = i
                    startFound = True
                    continue
                if '#endOfReleaseNotes' in elements[i]:
                    endIndex = i
                    break
            elements = elements[startIndex:endIndex]
            elementsText = []
            for e in elements:
                elementsText += [e.getText()]
            elementsTextString = '\n'.join(elementsText)
            elementsTextString = elementsTextString.replace('\n\n', '\n')
            elementsTextString = elementsTextString.replace('\n', '\n   -')
            elementsText = elementsTextString.split('\n')
            elementsTextDuplicates = elementsText
            elementsText = []
            for i in elementsTextDuplicates: # removes duplicates
                if not i in elementsText:
                    elementsText.append(i)
            elementsTextString = '\n'.join(elementsText)
            replacements = {'Release notes': '\n*** Release notes ***', 
                            '-New Features': '\nNew Features:',
                            '-Improvements': '\nImprovements:',
                            '-Bug Fixes': '\nBug Fixes:'
                            }
            for i in replacements.items():
                elementsTextString = elementsTextString.replace(i[0], i[1])
            elementsTextString = '\nPlease have a look at the release notes while the update is being downloaded.\n' + elementsTextString + '\n'
            return elementsTextString
        except requests.exceptions.ConnectionError:
            print('Connection Error. Your internet connection is probably down. Cannot get release notes.')
            elementsTextString = ''
            return elementsTextString
        except requests.exceptions.Timeout:
            print('Timeout Error. The website is down. Cannot get release notes.')
            elementsTextString = ''
            return elementsTextString

    def main(self):
        pass

if __name__=='__main__':
    Updater()