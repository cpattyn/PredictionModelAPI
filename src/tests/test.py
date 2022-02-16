#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from abc import ABC, abstractmethod
from pprint import pprint



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class APITest(ABC):

   def __init__(self
      ,  name = None
      ,  description = '<Missing Description>'
      ,  expected_code = 200
      ,  api_host = 'localhost'
      ,  api_port = 80
      ,  runParams = {}
      ,  **kwargs
   ):
      self.name          = str(name)
      self.description   = str(description)
      self.expected_code = expected_code
      self.api_host      = str(api_host)
      self.api_port      = int(api_port)
      self.runParams     = runParams


   def getName(self):
      return self.name


   def getDescription(self):
      return self.description



   def getExpectedCode(self):
      return self.expected_code


   def getRunParameters(self):
      return self.runParams



   @abstractmethod
   def getAPIEndpoint(self, **kwargs):
      raise NotImplementedError('ERROR: This is an abstract method that must be implemented in child class.')



   def getAPIEndpoint(self, **kwargs):
      return ''


   def getBaseAPICnx(self):
      return 'http://' + str(self.api_host) + ':' + str(self.api_port)


   def getAPICnx(self):
      return self.getBaseAPICnx() + self.getAPIEndpoint()



   @abstractmethod
   def run(self):
      raise NotImplementedError('ERROR: This is an abstract method that must be implemented in child class.')



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
         status_code = None
         test_status['status']     = 'FAILURE'
         test_status['err_reason'] = f'Failed to retrieved the status_code:\n{str(err)}'

      if status_code is not None:
         try:
            responseData = apiResponse.json()
         except Exception:
            responseData = None

         if (self.expected_code == status_code):
            test_status['status']     = 'SUCCESS'
            test_status['err_reason'] = None
         else:
            test_status['status']     = 'FAILURE'
            test_status['err_reason'] = 'The status_code returned by the API is not the one expected.'

      return (status_code, test_status, responseData)



   def printTestResult(self
      ,  apiCnx
      ,  status_code
      ,  test_status
      ,  responseData = None
   ):
      expected_code = self.getExpectedCode()

      print(f'''
============================
   Test: {self.getName().upper()}
============================

Description:
   {self.getDescription()}

Request done at: "{apiCnx}"

ResponseData:''')

      pprint(responseData)

      print(f'''

expected result = {expected_code}
actual restult  = {status_code}

==>  {test_status['status']}
''')
      if test_status['status'] != 'SUCCESS':
         print(f'\nreason: {test_status["err_reason"]}')