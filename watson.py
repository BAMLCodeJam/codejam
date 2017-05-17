__author__ = 'Maria'

import constants
from watson_developer_cloud import ConversationV1
import urllib3
import pprint
urllib3.disable_warnings()

class Watson(object):

    def __init__(self):

        self.conversation = ConversationV1(
            username=constants.WATSON['username'],
            password=constants.WATSON['password'],
            version=constants.WATSON['version'], )

        self.context = None

    def getAnswer(self, response):
        return response['output']['text'][0] if response['output']['text'] else ''

    def getIntent(self, response):
        return response['intents'][0]['intent'] if response['intents'] else ''

    def getInput(self, response):
        return response['input']['text']

    def setContext(self, response):
        self.context = response['context']

    def askWatson(self, text):
        response = self.conversation.message(workspace_id=constants.WATSON['workspaceID'], message_input={'text': text}, context=self.context)
        self.setContext(response)
        return response

if __name__ == "__main__":
    watson = Watson()
    response = watson.askWatson('hi')
    print watson.getInput(response)
    print watson.getAnswer(response)
    print watson.getIntent(response)
    pprint.pprint(response)
    response = watson.askWatson("I'm so hungry")
    print watson.getInput(response)
    print watson.getAnswer(response)
    print watson.getIntent(response)
    pprint.pprint(response)
    response = watson.askWatson('I would like some pasta')
    print watson.getInput(response)
    print watson.getAnswer(response)
    print watson.getIntent(response)
    pprint.pprint(response)
    response = watson.askWatson('Catch you later')
    print watson.getInput(response)
    print watson.getAnswer(response)
    print watson.getIntent(response)
    pprint.pprint(response)
