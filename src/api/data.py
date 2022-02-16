#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Libraries
from datetime import datetime
import random

# 3-rd-part libraries
import numpy as np
import pandas as pd

# Custom librairies
import params
from scaler import loadScaler




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PRE_ENCODING_FEAT_LIST = [
      ('mintemp'           ,  np.float64)
   ,  ('maxtemp'           ,  np.float64)
   ,  ('rainfall'          ,  np.float64)
   ,  ('windgustspeed'     ,  np.float64)
   ,  ('windspeed9am'      ,  np.float64)
   ,  ('windspeed3pm'      ,  np.float64)
   ,  ('humidity9am'       ,  np.float64)
   ,  ('humidity3pm'       ,  np.float64)
   ,  ('pressure9am'       ,  np.float64)
   ,  ('pressure3pm'       ,  np.float64)
   ,  ('temp9am'           ,  np.float64)
   ,  ('temp3pm'           ,  np.float64)
   ,  ('year'              ,  np.uint16)
   ,  ('month'             ,  np.uint8)
   ,  ('day'               ,  np.uint8)
   ,  ('location'          ,  str)
   ,  ('windgustdir'       ,  str)
   ,  ('winddir9am'        ,  str)
   ,  ('winddir3pm'        ,  str)
   ,  ('raintoday'         ,  str)
]

COMPLETE_ORDERED_FEATS = [
      'mintemp'
   ,  'maxtemp'
   ,  'rainfall'
   ,  'windgustspeed'
   ,  'windspeed9am'
   ,  'windspeed3pm'
   ,  'humidity9am'
   ,  'humidity3pm'
   ,  'pressure9am'
   ,  'pressure3pm'
   ,  'temp9am'
   ,  'temp3pm'
   ,  'year'
   ,  'month'
   ,  'day'
   ,  'location_Brisbane'
   ,  'location_Canberra'
   ,  'location_Melbourne'
   ,  'location_Perth'
   ,  'location_Sydney'
   ,  'windgustdir_E'
   ,  'windgustdir_ENE'
   ,  'windgustdir_ESE'
   ,  'windgustdir_N'
   ,  'windgustdir_NE'
   ,  'windgustdir_NNE'
   ,  'windgustdir_NNW'
   ,  'windgustdir_NW'
   ,  'windgustdir_S'
   ,  'windgustdir_SE'
   ,  'windgustdir_SSE'
   ,  'windgustdir_SSW'
   ,  'windgustdir_SW'
   ,  'windgustdir_W'
   ,  'windgustdir_WNW'
   ,  'windgustdir_WSW'
   ,  'winddir9am_E'
   ,  'winddir9am_ENE'
   ,  'winddir9am_ESE'
   ,  'winddir9am_N'
   ,  'winddir9am_NE'
   ,  'winddir9am_NNE'
   ,  'winddir9am_NNW'
   ,  'winddir9am_NW'
   ,  'winddir9am_S'
   ,  'winddir9am_SE'
   ,  'winddir9am_SSE'
   ,  'winddir9am_SSW'
   ,  'winddir9am_SW'
   ,  'winddir9am_W'
   ,  'winddir9am_WNW'
   ,  'winddir9am_WSW'
   ,  'winddir3pm_E'
   ,  'winddir3pm_ENE'
   ,  'winddir3pm_ESE'
   ,  'winddir3pm_N'
   ,  'winddir3pm_NE'
   ,  'winddir3pm_NNE'
   ,  'winddir3pm_NNW'
   ,  'winddir3pm_NW'
   ,  'winddir3pm_S'
   ,  'winddir3pm_SE'
   ,  'winddir3pm_SSE'
   ,  'winddir3pm_SSW'
   ,  'winddir3pm_SW'
   ,  'winddir3pm_W'
   ,  'winddir3pm_WNW'
   ,  'winddir3pm_WSW'
   ,  'raintoday_No'
   ,  'raintoday_Yes'
]

FEAT_VALUES_CITIES    = ('Brisbane', 'Canberra', 'Melbourne', 'Perth', 'Sydney')
FEAT_VALUES_DIRECTION = ('E', 'ENE', 'ESE', 'N', 'NE', 'NNE', 'NNW', 'NW', 'S', 'SE', 'SSE', 'SSW', 'SW', 'W', 'WNW', 'WSW')
FEAT_VALUES_YES_NO    = ('yes', 'no')



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def printDF(df):
   with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
      print(df)



def loadDF(filepath):
   return pd.read_csv(
         filepath_or_buffer = filepath
      ,  sep       = ','
      ,  header    = 0
      ,  index_col = 0
   )



def featuresToDF(userFeatures):

   # Création du DataFrame a partir du nom des features (pre encodées)
   df = pd.DataFrame(columns = [ item[0] for item in PRE_ENCODING_FEAT_LIST ])
   # Assignation du type à chaque colonne du DataFrame
   df.astype(
         dtype = { item[0]: item[1] for item in PRE_ENCODING_FEAT_LIST }
      ,  copy = False
   )
   # On récupère les features saisies par l'utilisateur et on les insère dans le DataFrame
   for colName in userFeatures.keys():
      df.loc[0, colName] = userFeatures.get(colName)

   return df




def genNumFeatures(df_userFeatures):

   # Chargement du dataframe contenant les valeurs min et max des features numériques
   numFeatures_min_max = loadDF(params.NUM_FEATURES_MIN_MAX_FILEPATH)

   # Génération des features numériques (de façon aléatoire)
   randValues = numFeatures_min_max.apply(lambda x: round(random.uniform(x['min'], x['max']), 6), axis=1)

   # Identification des colonnes numériques
   numCols = randValues.index.tolist()

   # Remplacement des valeurs nulles par les valeurs générées aléatoirement
   data = df_userFeatures[numCols].copy()
   for col in randValues.index.tolist():
      data[col].fillna(value = randValues[col], inplace = True)

   return data




def genCatFeatures(df_userFeatures):

   dirCols        = ('windgustdir', 'winddir9am', 'winddir3pm')
   catCols        = ['location'] + list(dirCols)
   catEncodedCols = []

   # column: location
   for city in FEAT_VALUES_CITIES:
      catEncodedCols.append('location' + '_' + city)
   # columns: windgustdir | winddir9am | winddir3pm
   for col in dirCols:
      for direction in FEAT_VALUES_DIRECTION:
         catEncodedCols.append(col + '_' + direction)

   data = df_userFeatures[catCols].copy()
   data.fillna(
         value = {
               'location'   : FEAT_VALUES_CITIES[random.randint(0,len(FEAT_VALUES_CITIES) - 1)]
            ,  'windgustdir': FEAT_VALUES_DIRECTION[random.randint(0, len(FEAT_VALUES_DIRECTION) - 1)]
            ,  'winddir9am' : FEAT_VALUES_DIRECTION[random.randint(0, len(FEAT_VALUES_DIRECTION) - 1)]
            ,  'winddir3pm' : FEAT_VALUES_DIRECTION[random.randint(0, len(FEAT_VALUES_DIRECTION) - 1)]
         }
      ,  inplace = True
   )

   # Construction du DataFrame avec les colonnes encodées
   encodedData = pd.DataFrame(
         data = np.zeros((1, len(catEncodedCols)), dtype = np.int8)
      ,  columns = catEncodedCols
   )

   # On positionne à 1 la valeur encodée telle que choisi dans data
   for colName in catCols:
      value = data.loc[0, colName]
      encodedData.loc[0, colName + '_' + value] = 1

   return encodedData





def prepareFeatures(userFeatures):

   # Transformation des features (dictionary -> Dataframe)
   df_userFeatures = featuresToDF(userFeatures)

   if params.DEBUG:
      print('\nFeatures are now stored into a DataFrame:')
      print('   shape[features]: ', df_userFeatures.shape)
      printDF(df_userFeatures)

   # Récupération des valeurs numériques
   numFeatures = genNumFeatures(df_userFeatures)

   # Génération des valeurs non numériques
   catFeatures = genCatFeatures(df_userFeatures)

   # DataFrame contenant la date courante (décomposée)
   todayDate   = datetime.today()
   yearVal, monthVal, dayVal =                     \
      userFeatures.get('year'  , todayDate.year),   \
      userFeatures.get('month' , todayDate.month),  \
      userFeatures.get('day'   , todayDate.day)
   dateFeature = pd.DataFrame(
      data = {
               'year'   : [yearVal]
            ,  'month'  : [monthVal]
            ,  'day'    : [dayVal]
         }
   )

   # On impose la valeur de raintoday en fonction de la variable "rainfall"
   # Si "rainfall" > 0 alors raintoday vaudra: 'yes'
   # Si "rainfall" == 0 alors raintoday vaudra: 'no
   if df_userFeatures.loc[0, 'rainfall'] > 0:
      raintodayFeature = pd.DataFrame(
         data = {
               'raintoday_No' : [0]
            ,  'raintoday_Yes': [1]
         }
      )
   else:
      raintodayFeature = pd.DataFrame(
         data = {
               'raintoday_No' : [1]
            ,  'raintoday_Yes': [0]
         }
      )

   # Concaténation
   features = pd.concat([numFeatures, catFeatures, dateFeature, raintodayFeature], axis = 1)

   if params.DEBUG:
      print('\nFeatures:')
      printDF(features)
      print('\nControle des NaNs:')
      print('   nbNulls: ', features.isnull().sum().sum())

   # On replace les colonnes du DataFrame dans le bon ordre
   features = features[ COMPLETE_ORDERED_FEATS ]

   if params.DEBUG:
      print('\nOrdered Features:')
      features.info()

   # Chargement du scaler
   scaler = loadScaler()

   # Transformation du jeu de données par le scaler
   features = pd.DataFrame(
         data    = scaler.transform(features)
      ,  columns = features.columns
   )

   return features

