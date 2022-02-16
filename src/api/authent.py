# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Authent:

   def __init__(self, credentials):
      self.credentials = credentials


   def authenticate(self, username, password):
      if not self.credentials.isUserExist(username):
         return False
      return password == self.credentials.getPassword(username)
