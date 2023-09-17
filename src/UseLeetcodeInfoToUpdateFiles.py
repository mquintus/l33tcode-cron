#
# Update files according to patterns in relation to the l33tcode daily challenge
#

def camelCaseWithUnderScore(orig):
    sub = orig.split('-')
    return '_'.join([s[0].upper() + s[1:].lower() for s in sub])

class UseLeetcodeInfoToUpdateFiles:
    def enhance(self, data: dict, content: str):
        replacements = {
            "date": data['date'],
            "number": data['question']['frontendQuestionId'],
            "title": data['question']['title'],
            "titleSlug": data['question']['titleSlug'],
            "myTitleSlug": data['question']['frontendQuestionId'] + '_' + data['question']['title'].replace(' ', '_'),
            "difficulty": data['question']['difficulty'],
            "content": data['content'],
            "topictag": data['question']['topicTags'][0]['name'],
            "testcases": '',
        }
        # Example topic tags are ['Dynamic Programming', 'Bit Manipulation', 'Breadth-First Search', 'Graph', 'Bitmask']
        # Some are more interesting than others. We'll prioritize "Graph" is present. Otherwise the first in the list.
        for topictag in data['question']['topicTags']:
            if topictag['name'] == 'Graph':
                replacements['topictag'] = 'Graph'
        for key, value in replacements.items():
            content = content.replace('{' + key + '}', value)
        return content.replace('\\n', '\n')


    def appendFile(
            self,
            data: dict,
            file: str,
            match: str,
            append: str,
    ):
        append = self.enhance(data, append)
        file = self.enhance(data, file)
        match = self.enhance(data, match)
        f = open(file, "r+")
        readmeFileContent = f.read()
        if match + append in readmeFileContent:
            print("Already in file:", match + append)
            return
        if match not in readmeFileContent:
            print("No match:", match)
            print("Could not add:", append)
            raise(Exception("Could not add: " + append))

        readmeFileContent = readmeFileContent.replace(match, match + append)
        f.truncate(0)
        f.seek(0)
        f.write(readmeFileContent)
        f.close()

    def prependFile(
            self,
            data: dict,
            file: str,
            match: str,
            prepend: str,
    ):
        prepend = self.enhance(data, prepend)
        file = self.enhance(data, file)
        match = self.enhance(data, match)
        f = open(file, "r+")
        readmeFileContent = f.read()
        if match + prepend in readmeFileContent:
            print("Already in file:", prepend + match)
            return
        if match not in readmeFileContent:
            print("No match:", match)
            print("Could not add:", prepend)
            raise(Exception("Could not add: " + prepend))

        readmeFileContent = readmeFileContent.replace(match, prepend + match)
        f.truncate(0)
        f.seek(0)
        f.write(readmeFileContent)
        f.close()

    def replaceFile(
            self,
            data: dict,
            file: str,
            matchbefore: str,
            matchafter: str,
            replace: str,
    ):
        replace = self.enhance(data, replace)
        file = self.enhance(data, file)
        matchbefore = self.enhance(data, matchbefore)
        matchafter = self.enhance(data, matchafter)
        f = open(file, "r+")
        readmeFileContent = f.read()
        if matchbefore + replace + matchafter in readmeFileContent:
            print("Already in file:", matchbefore + replace + matchafter)
            return
        if matchbefore not in readmeFileContent:
            raise(Exception("No match:" + matchbefore))
        if matchafter not in readmeFileContent:
            raise(Exception("No match:" + matchafter))
        p0 = readmeFileContent.find(matchbefore) + len(matchbefore)
        p1 = readmeFileContent.find(matchafter)
        readmeFileContent = readmeFileContent[:p0] + replace + readmeFileContent[p1:]
        f.truncate(0)
        f.seek(0)
        f.write(readmeFileContent)
        f.close()

    def createFile(
            self,
            data: dict,
            file: str,
            content: str,
    ):
        file = self.enhance(data, file)
        content = self.enhance(data, content)
        f = open(file, "w")
        f.write(content)
        f.close()


