#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Import standard libraries
import json

# 3rd-party Libraries
import requests

# Custom Libraries
from test import APITest


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PredictionAPITest(APITest):

   def getAPIEndpoint(self, **kwargs):
      return f'/prediction'



   def getTestStatus(self
      ,  apiResponse
   ):
      test_status = {
            'status'    : 'UNKNOWN'
         ,  'err_reason': 'Unknown'
      }
      responseData = None

      try:
         status_code = apiResponse.status_code
      except Exception as err:
         status_code               = None
         test_status['status']     = 'FAILURE'
         test_status['err_reason'] = f'Failed to retrieved the status_code:\n{str(err)}'

      if status_code is not None:

         if (self.expected_code != status_code):
            test_status['status']     = 'FAILURE'
            test_status['err_reason'] = 'The status_code returned by the API is not the one expected.'
         else:
            try:
               responseData = apiResponse.json()
            except Exception:
               responseData = None

            test_status['status']     = 'SUCCESS'
            test_status['err_reason'] = None

      return status_code, test_status, responseData



   def run(self):

      # Retrieving the features associated to this test
      features = None
      if self.runParams:
         features = self.runParams.get('features')

      # Retrieving the model_id associated to this test
      modelId = self.runParams.get('model_id')

      if modelId is None:
         raise ValueError('ERROR: Failed to retrieve the model instance for the test.')

      apiCnx = self.getAPICnx()

      # requête
      apiResponse = requests.post(
         #   url     =
         apiCnx
         ,  headers = {
                  'Content-Type': 'application/json'
               ,  'Authentication': self.runParams.get('Authentication')
            }
         ,  data    = json.dumps(
               {
                     'model_id': modelId
                  ,  'features': features
               }
            )
      )

      status_code, test_status, responseData = self.getTestStatus(apiResponse = apiResponse)

      self.printTestResult(
            apiCnx       = apiCnx
         ,  status_code  = status_code
         ,  test_status  = test_status
         ,  responseData = responseData
      )

