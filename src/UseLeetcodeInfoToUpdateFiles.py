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
        }
        for key, value in replacements.items():
            content = content.replace('{' + key + '}', value)
        return content.replace('\\n', '\n')


    def adjustFile(
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
            return

        readmeFileContent = readmeFileContent.replace(match, match + append)
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


