import json
from constants import WATSON_VISUAL_REC
from watson_developer_cloud import VisualRecognitionV3

class WatsonImgRec(object):

    def __init__(self):

        self.classifier = VisualRecognitionV3(
            url=WATSON_VISUAL_REC['url'],
            version=WATSON_VISUAL_REC['version'],
            api_key=WATSON_VISUAL_REC['api_key'], )
    
    @staticmethod
    def imagesSet():
        return [
            {'image_id': 0, 'path': 'https://s-i.huffpost.com/gen/4451422/images/o-FOOD-facebook.jpg'},
            {'image_id': 1, 'path': 'http://cdn.akc.org/content/hero/puppy-boundaries_header.jpg'},
            {'image_id': 2, 'path': 'https://image.freepik.com/free-vector/writting-pencil-design_1095-187.jpg'},
            ]
    
    @staticmethod
    def task():
        return 'Food'

    def classifyImg(self, request, images, image_id):

        test_url = self.getImageUrl(images, image_id)
        url_result = self.classifier.classify(parameters=json.dumps({'url': test_url}))
        rightWord = any(['food' in className['class'] for className in url_result['images'][0]['classifiers'][0]['classes']])

        if rightWord:
            return 'Well done!'
        else:
            return 'Please try again'

    def getImageUrl(self, images, image_id):
        return [img['path'] for img in images if img['image_id']==int(image_id)][0]
        