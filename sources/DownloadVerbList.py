#!/usr/bin/env python3
import requests
import bs4
import time

class DownloadVerbList():

    def __init__(self):
         self.main()

    def getVerbList(self):
        print ('Getting the verb list from the website...')
        pageRequest = requests.get('http://www11.edu.fi/ymmarra/index.php?moduli=verbit', timeout=3.05)
        pageRequest.text
        pageRequest.status_code
        pageRequest.raise_for_status()
        soup = bs4.BeautifulSoup(pageRequest.text, "html.parser")
        letterList = soup.select('td > div .init')
        print ('Done')
        verbList = []
        print ('Populating the local verb list variable...')
        for i in range (len(letterList)-2): # -2 to avoid repeating 'a' and to avoid 'ä' because it has a weird URL and only one verb
            letter = letterList[i].getText().lower()
            url = 'http://www11.edu.fi/ymmarra/index.php?moduli=verbit&kirjain=' + letter
            pageRequest = requests.get(url, timeout=3.05)
            soup = bs4.BeautifulSoup(pageRequest.text, "html.parser")
            verbList.extend(soup.select('td > a[style]'))
            print (letter, '... done')
        print ('Done')
        verbList = [str(verb.getText()).lower() for verb in verbList]
        # need to convert Finnish letters so verb's urls work
        verbListWithoutDieresis = [verb.replace('ä', 'a') for verb in verbList]
        verbListWithoutDieresis = [verb.replace('ö', 'o') for verb in verbListWithoutDieresis]
        for i in range (len(verbListWithoutDieresis)):
            verb = verbListWithoutDieresis[i] 
            print (verb)
        print ('Number of verbs:', len(verbListWithoutDieresis))
        return verbList, verbListWithoutDieresis

    def downloadVerbs(self):
        verbList, verbListWithoutDieresis = self.getVerbList()
        print ('Downloading verb pages...')
        for i in range (len(verbList)):
            pageRequest = requests.get('http://www11.edu.fi/ymmarra/index.php?moduli=verbit&sana=' + verbListWithoutDieresis[i], timeout=3.05)
            soup = bs4.BeautifulSoup(pageRequest.text, "html.parser")
            # The verb should not be added to the database if it doesn't have normal personal pronouns (there are 11 of these verbs on the website)
            element = soup.select('td > pre')
            element = str(element).split()
            element = element[1:13]
            if 'minä' not in element:
                print ('WARNING: This verb does NOT have normal personal pronouns: skipping it.')
                continue
            else:
                print(verbList[i], 'has normal personal pronouns: saving it at a file...')
                file = open('verbs//' + verbList[i] + '.html', 'wb')
                for chunk in pageRequest.iter_content(100000):
                    file.write(chunk)
                file.close()
                print ('Page', i, 'done')
        print ('Verbs downloading done!')

    def main(self):
        startTime = time.clock ()
        #self.downloadVerbs()

        print ("Execution time: %.3f seconds" % (time.clock () - startTime))

if __name__=='__main__':
    DownloadVerbList()