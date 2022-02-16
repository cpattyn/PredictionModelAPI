# Ce fichier contient tous les paramètres utiles à l'API

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Import
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os

__CUR_PATH = os.path.abspath(os.path.dirname(__file__))

# DEBUG
DEBUG = True if os.environ.get('DEBUG') is not None else False


# PATHS
#
DATA_PATH   = os.path.join( __CUR_PATH, '..', '..', 'data' )
DB_PATH     = os.path.join( __CUR_PATH, '..', '..', 'db' )
SCALER_PATH = os.path.join( __CUR_PATH, '..', '..', 'db', 'scaler' )
MODEL_PATH  = os.path.join( __CUR_PATH, '..', '..', 'db', 'models' )

# FILEPATHS
#
API_MODEL_LIST_FILEPATH       = os.path.join( DB_PATH, 'api_models.json' )
NUM_FEATURES_MIN_MAX_FILEPATH = os.path.join( DATA_PATH, 'numFeatures_min_max.csv' )
SCALER_FILEPATH               = os.path.join( SCALER_PATH,  'scaler.joblib')


del __CUR_PATH