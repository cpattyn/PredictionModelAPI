#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 3rd-party Libraries
import requests

# Custom Libraries
from test import APITest


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ModelsAPITest(APITest):

   def getAPIEndpoint(self, **kwargs):
      return '/models'



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
            # Retrieving the model list
            try:
               modelList = apiResponse.json()['models']
            except Exception:
               modelList = None
               test_status['status']     = 'FAILURE'
               test_status['err_reason'] = 'Failed to retrieve the model list from the API.'

            if modelList is not None:
               responseData = modelList
               # The API should have at least one available model
               if len(modelList) < 1:
                  test_status['status']     = 'FAILURE'
                  test_status['err_reason'] = 'No model available from the API: there should be at least one.'
               else:
                  availCnt = 0
                  for model in modelList:
                     if model.get('available') == True:
                        availCnt += 1
                        break

                  if availCnt >= 1:
                     test_status['status']     = 'SUCCESS'
                     test_status['err_reason'] = None
                  else:
                     test_status['status']     = 'FAILURE'
                     test_status['err_reason'] = 'No model available from the API: there should be at least one.'

      return status_code, test_status, responseData




   def run(self, **kwargs):
      apiCnx = self.getAPICnx(**kwargs)

      # requête
      apiResponse = requests.get(url = apiCnx)

      status_code, test_status, responseData = self.getTestStatus(apiResponse = apiResponse)

      self.printTestResult(
            apiCnx       = apiCnx
         ,  status_code  = status_code
         ,  test_status  = test_status
         ,  responseData = responseData
      )

