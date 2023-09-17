import requests
import json
import logging

class DailyChallengeLib:
    def _getQuestionOfTodayContent(self, titleSlug: str) -> str:
        print("Get question content for " + titleSlug)
        url = 'https://leetcode.com/graphql'
        queryJson = {
            "operationName": "questionContent",
            "query":  " query questionContent($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    content\n    mysqlSchemas\n  }\n}\n    ",
            "variables":  {"titleSlug": titleSlug},
            "titleSlug": titleSlug
        }
        r2 = requests.get(url, json=queryJson)
        answer2 = json.loads(r2.text)
        content = answer2['data']['question']['content']
        print(len(content), "chars!")
        return content

    def _getQuestionOfTodayMetaData(self) -> dict:
        url = 'https://leetcode.com/graphql'
        query = '''query questionOfToday {
            activeDailyCodingChallengeQuestion {
                date
                userStatus
                link
                question {
                    acRate
                    difficulty
                    freqBar
                    frontendQuestionId: questionFrontendId
                    isFavor
                    paidOnly: isPaidOnly
                    status
                    title
                    titleSlug
                    hasVideoSolution
                    hasSolution
                    topicTags {
                        name
                        id
                        slug
                    }
                }
            }
        }
        '''
        r = requests.get(url, json={'query': query})
        answer = json.loads(r.text)
        data = answer['data']['activeDailyCodingChallengeQuestion']

        number = data['question']['frontendQuestionId']
        data['myTitleSlug'] = number + '_' + data['question']['title'].replace(' ', '_')
        return data

    def retrieve(self) -> dict:
        data = self._getQuestionOfTodayMetaData()
        data['content'] = self._getQuestionOfTodayContent(data['question']['titleSlug'])
        return data
