#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Libraires
import base64

# 3rd-party Libraries
import requests

# Custom Libraries
from test import APITest


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class AuthentAPITest(APITest):


   def getAPIEndpoint(self, **kwargs):
      return '/authent'



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

      username = None
      password = None

      if self.runParams:
         username = self.runParams.get('username')
         password = self.runParams.get('password')

      apiCnx = self.getAPICnx()

      authentKey = str(username) + ':' + str(password)
      authentKey = authentKey.encode("ascii")

      # requête
      apiResponse = requests.get(
            url = apiCnx
         ,  headers = {
                  'Content-Type': 'application/json'
               ,  'Authentication': base64.b64encode(authentKey)
            }
      )

      status_code, test_status, responseData = self.getTestStatus(apiResponse = apiResponse)

      self.printTestResult(
            apiCnx       = apiCnx
         ,  status_code  = status_code
         ,  test_status  = test_status
         ,  responseData = responseData
      )

