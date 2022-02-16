#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Librairies
import os
import sys

# Custom Librairies
import params
from test_status import StatusAPITest
from test_models import ModelsAPITest
from test_perf_models import PerfModelsAPITest
from test_perf_model import PerfModelAPITest
from test_authent import AuthentAPITest
from test_prediction import PredictionAPITest


# Return Codes
SUCCESS = 0
ERROR   = 2



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def eprint(*args, **kwargs):
   print(*args, file = sys.stderr, **kwargs)


def buildTester(
      role
   ,  api_host
   ,  api_port
):
   if not isinstance(role, str):
      raise TypeError(f'ERROR: Invalid type for variable: <ROLE> : a type <string> is expected.')
   role = role.lower()
   if (role == 'status'):
      return StatusAPITest(
            name = 'STATUS'
         ,  description = 'Checks the availability of the API'
         ,  expected_code = 200
         ,  api_host = api_host
         ,  api_port = api_port
      )
   elif (role == 'models_list'):
      return ModelsAPITest(
            name = 'MODEL LIST'
         ,  description = 'Retrieve the list of models which are avaialble from the API'
         ,  expected_code = 200
         ,  api_host = api_host
         ,  api_port = api_port
      )
   elif (role == 'performance_all_models'):
      return PerfModelsAPITest(
            name = 'PERFORMANCE MODELS'
         ,  description = 'Retrieve the score of each model available from the API'
         ,  expected_code = 200
         ,  api_host = api_host
         ,  api_port = api_port
      )
   elif (role == 'performance_one_model'):
      return PerfModelAPITest(
            name = 'PERFORMANCE MODEL'
         ,  description = 'Retrieve the score of the selected model'
         ,  expected_code = 200
         ,  api_host = api_host
         ,  api_port = api_port
         ,  model_id = os.environ.get('MODEL_ID')
      )
   elif (role == 'authentication'):
      return [
         AuthentAPITest(
               name = 'AUTHENTICATION'
            ,  description = 'Check a successful authentication to the API'
            ,  expected_code = 200
            ,  api_host = api_host
            ,  api_port = api_port
            ,  runParams = {
                     'username': 'Mara'
                  ,  'password': 9820
               }
         )
         ,  AuthentAPITest(
                  name = 'AUTHENTICATION'
               ,  description = 'Check a fail authentication to the API'
               ,  expected_code = 401
               ,  api_host = api_host
               ,  api_port = api_port
               ,  runParams = {
                        'username': 'InvalidUser'
                     ,  'password': 1234
                  }
            )
      ]
   elif (role == 'prediction'):
      return [
         PredictionAPITest(
               name = 'PREDICTION (full observation)'
            ,  description = 'Check a prediction with a full observation'
            ,  expected_code = 200
            ,  api_host = api_host
            ,  api_port = api_port
            ,  runParams = {
                     'model_id': 'db5f7fb6-8ddf-420c-a485-4517c3200a64'
                  ,  'features': {
                           'mintemp'      : 10
                        ,  'maxtemp'      : 20
                        ,  'rainfall'     : 0.4
                        ,  'windgustspeed': 37.0
                        ,  'windspeed9am' : 17.0
                        ,  'windspeed3pm' : 11.0
                        ,  'humidity9am'  : 62.0
                        ,  'humidity3pm'  : 65.0
                        ,  'pressure9am'  : 1019.2
                        ,  'pressure3pm'  : 1011.4
                        ,  'temp9am'      : 15.1
                        ,  'temp3pm'      : 17.6
                        ,  'year'         : 2022
                        ,  'month'        : 2
                        ,  'day'          : 8
                        ,  'location'     : 'Sydney'
                        ,  'windgustdir'  : 'NNW'
                        ,  'winddir9am'   : 'ESE'
                        ,  'winddir3pm'   : 'ENE'
                        ,  'raintoday'    : 'yes'
                     }
                  ,  'Authentication': 'UmhpYW5ub246MzU0NQ=='
               }
         ),
         PredictionAPITest(
               name = 'PREDICTION (partial observation)'
            ,  description = 'Check a prediction with a partial observation'
            ,  expected_code = 200
            ,  api_host = api_host
            ,  api_port = api_port
            ,  runParams = {
                     'model_id': '59fa8691-f141-4cd9-8c50-4dc7138950d5'
                  ,  'features': {
                           'mintemp'      : 10
                        ,  'maxtemp'      : 20
                        ,  'rainfall'     : 0.4
                        ,  'temp3pm'      : 17.6
                        ,  'year'         : 2022
                        ,  'month'        : 2
                        ,  'day'          : 8
                        ,  'location'     : 'Sydney'
                        ,  'winddir3pm'   : 'ENE'
                        ,  'raintoday'    : 'yes'
                     }
                  ,  'Authentication': 'UmhpYW5ub246MzU0NQ=='
               }
         )
      ]
   else:
      raise Exception(f'This role is not supported for an API Tester: {role}')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main Function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(argv):

   def runTest(test):
      try:
         test.run()
      except Exception as err:
         print('The following exception occurred during the execution of this test:\n', str(err))


   try:

      progName = argv[0]
      progArgs = argv[1:]

      # Retrieving environment variables
      API_HOST = os.environ.get('API_HOST', params.DFLT_API_HOST)
      API_PORT = os.environ.get('API_PORT', params.DFLT_API_PORT)
      ROLE     = os.environ.get('ROLE')

      # ROLE is a mandatory environment variable
      if ROLE is None:
         eprint(f'{progName}: ERROR: <ROLE> is a mandatory environment variable for this script: please set this value to a non-Null value and try again.')
         return ERROR

      # Instanciating the API tester
      tester = buildTester(
            role = ROLE
         ,  api_host = API_HOST
         ,  api_port = API_PORT
      )

      # Run the test scenario
      if isinstance(tester, list):
         for testScenario in tester:
            testScenario.run()
      else:
         tester.run()

      return SUCCESS

   except Exception as e:
      print(str(e))
      return ERROR



########################################################################################################################
#
# MAIN PROGRAM starts here...
#
########################################################################################################################

if __name__ == '__main__':
   main(sys.argv)
