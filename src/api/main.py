#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Librairies
import os
import sys

# 3rd-party Librairies
import getopt

# Custom Libraries
import params
from api import api



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


RECOGNIZED_APP_OPTS = {
      'host'         :  ('API_HOST', str,    '0.0.0.0')
   ,  'port'         :  ('API_PORT', int,    5000)
   ,  'debug'        :  ('DEBUG'   , None,   False)
   ,  'use_reloader' :  (None      , None,   False)
}
# The key correspond to the name of this option for the command line.
# The value correspond to a tuple of length 2 with the following entries:
#     1: the environment variable name that correspond to the option identified by the key
#     2: the type of the option expected argument
#     3: the default value (the value to be used if the option is not set at the command neither as an environment variable)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Exceptions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UnknownOptionError(Exception):
   pass

class UnsetOptionError(Exception):
   pass



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def eprint(*args, **kwargs):
   print(*args, file = sys.stderr, **kwargs)


def app():
   return api



def getAPIOpts(
      envVars     = {}
   ,  cmdLineArgs = {}
):

   def getOptValue(optName):
      if optName not in RECOGNIZED_APP_OPTS:
         raise UnknownOptionError(f'Unknown option: {optName}')

      recognizedOptType = RECOGNIZED_APP_OPTS[optName][1]

      if optName in cmdLineArgs.keys():
         if recognizedOptType is None:
            value = True
         else:
            value = cmdLineArgs.get(optName)
         return value

      try:
         envVarName = RECOGNIZED_APP_OPTS[optName][0]
         return envVars[envVarName]
      except UnknownOptionError as err:
         raise err
      except Exception:
         raise UnsetOptionError(f'Option not set: {optName}')


   opts = dict()

   # Adding options in "opts" per order or priority
   for optName in RECOGNIZED_APP_OPTS.keys():
      try:
         value = getOptValue(optName)
         if value is not None:
            opts[optName] = value

      except UnsetOptionError:
         optType      = RECOGNIZED_APP_OPTS[optName][1]
         optDfltValue = RECOGNIZED_APP_OPTS[optName][2]
         if optType is None:
            if optDfltValue:
               opts[optName] = True
         else:
            opts[optName] = optDfltValue

   return opts



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main Function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main(argv):

   # Parsing the command line
   longopts = [ optName + '=' if item[1] is not None else optName
                  for optName, item in RECOGNIZED_APP_OPTS.items()
              ]

   options, remainder = getopt.getopt(
         args      = sys.argv[1:]
      ,  shortopts = ''
      ,  longopts  = longopts
   )

   # Preparing parameters
   cmdLineArgs = { key[2:]: value for key, value in options }
   apiOpts = getAPIOpts(
         envVars     = os.environ
      ,  cmdLineArgs = cmdLineArgs
   )

   app().run(**apiOpts)



########################################################################################################################
#
# MAIN PROGRAM starts here...
#
########################################################################################################################

if __name__ == '__main__':
   main(sys.argv)
