# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import csv
import os
from abc import abstractmethod


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DFLT_CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), '..', '..', 'db', 'credentials.csv')



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Credentials:

   def __init__(self
      ,  csvFilepath = DFLT_CREDENTIALS_FILEPATH
      ,  delimiter   = ','
   ):
      self.csvFilepath = csvFilepath
      self.delimiter   = delimiter
      self.data        = {}
      self._load()


   def _load(self):
      self.data = {}
      with open(self.csvFilepath) as csvFile:
         reader = csv.DictReader(csvFile, delimiter = self.delimiter)
         for row in reader:
            try:
               username = row['username']
               password = row['password']
               if username:
                  username = Credentials.getNormalizedUsername(username)
               if password is None:
                  print(f'WARNING: No password defined for user: {username} : this user has been skipped !')
                  continue
               self.data[username] = password
            except Exception as err:
               print('WARNING: the following exception occurred:')
               print(str(err))
               print('WARNING: the corresponding entry in credential file has been skipped !')
               continue



   @abstractmethod
   def getNormalizedUsername(username):
      if not isinstance(username, str):
         raise TypeError('Invalid type for argument <username>: a type <string> is expected')
      return username.lower()



   def isUserExist(self, username):
      username = Credentials.getNormalizedUsername(username)
      return username in self.data.keys()



   def getPassword(self, username):
      username = Credentials.getNormalizedUsername(username)
      return self.data.get(username)

