#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 3rd-party Libraries
import random
import requests

# Custom Libraries
from test import APITest
from test_models import ModelsAPITest

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PerfModelAPITest(APITest):

   def __init__(self
      ,  **kwargs
   ):
      self.model_id = kwargs.pop('model_id')
      super().__init__(**kwargs)



   def getAPIEndpoint(self, **kwargs):
      return '/performance/model'



   def getTestStatus(self
      ,  apiResponse
   ):
      test_status = {
            'status'    : 'UNKNOWN'
         ,  'err_reason': 'Unknown'
      }

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
            # Retrieving the model performance
            try:
               model_perf = apiResponse.json()['performance']
            except Exception:
               model_perf = None
               test_status['status']     = 'FAILURE'
               test_status['err_reason'] = 'Failed to retrieve the performance for the selected model.'

            if model_perf is not None:
               if model_perf.get('model_score') is None:
                  test_status['status']     = 'FAILURE'
                  test_status['err_reason'] = 'Field "model_score" is missing from the API response.'
               else:
                  test_status['status']     = 'SUCCESS'
                  test_status['err_reason'] = None

      return status_code, test_status, model_perf




   def run(self, **kwargs):

      test_status = {
            'status'    : 'UNKNOWN'
         ,  'err_reason': 'Unknown'
      }
      model_id = kwargs.get('MODEL_ID')

      responseData = None

      # Retrieving the list of all models
      url = self.getBaseAPICnx() + ModelsAPITest().getAPIEndpoint()
      apiResponse = requests.get(url = url)

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
            if model_id is None:
               # Retrieving the model list
               try:
                  modelList = apiResponse.json()['models']
               except Exception:
                  modelList = None
                  test_status['status']     = 'FAILURE'
                  test_status['err_reason'] = 'Failed to retrieve the model list from the API.'

               if modelList is not None:

                  modelIds = []
                  for model in modelList:
                     if model.get('available'):
                        id = model.get('id')
                        if id is not None:
                           modelIds.append(id)

                  if len(modelIds) < 1:
                     test_status['status']     = 'FAILURE'
                     test_status['err_reason'] = 'No model available from the API: there should be at least one.'
                  else:
                     idx = random.randint(0, len(modelIds) - 1)
                     model_id = modelIds[idx]

            apiCnx = self.getAPICnx() + f'/{str(model_id)}'

            # requête
            apiResponse = requests.get(url = apiCnx)
            status_code, test_status, responseData = self.getTestStatus(apiResponse = apiResponse)
            self.printTestResult(
                  apiCnx       = apiCnx
               ,  status_code  = status_code
               ,  test_status  = test_status
               ,  responseData = responseData
            )


