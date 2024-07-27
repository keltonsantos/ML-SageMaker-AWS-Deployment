#Classification Function
import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer
from sagemaker.predictor import Predictor

# Fill this in with the name of your deployed model
ENDPOINT = 'mlflow-project'

def lambda_handler(event, context):
    # Decode the image data
    body =event['body']
    image = base64.b64decode(body['image_data'])

    # Instantiate a Predictor
    predictor = Predictor(ENDPOINT)
    
    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction:
    inferences = predictor.predict(image)
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences.decode('utf-8')  # Decode to UTF-8 string
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }