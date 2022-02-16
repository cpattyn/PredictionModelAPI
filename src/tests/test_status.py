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


class StatusAPITest(APITest):

   def getAPIEndpoint(self, **kwargs):
      return '/status'


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

