#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Libraries
import os

# 3rd-party Libraries
from joblib import load

# Custom libraries
import params


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def loadModel(filename):
   filepath = os.path.join(params.MODEL_PATH, filename)
   return load(filepath)


