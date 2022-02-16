#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 3rd-party Libraries
from joblib import load

# Custom Librairies
import params


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def loadScaler():
   return load(params.SCALER_FILEPATH)


