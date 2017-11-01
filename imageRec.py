import json
from watson_developer_cloud import VisualRecognitionV3

test_url = 'http://www.veronapizza.co.uk/wp-content/uploads/2017/01/pizza_trad_pepperoni.png'
visual_recognition = VisualRecognitionV3('2017-08-09', api_key='64a5583a8517eea1f0c020161c1b65f09b0cc07e')

url_result = visual_recognition.classify(images_url=test_url)
print(json.dumps(url_result, indent=2))

