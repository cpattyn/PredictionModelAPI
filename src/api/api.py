#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Standard Libraries
import base64
import json

# 3rd-party Librairies
from flask import Flask, request, make_response
from pydantic import BaseModel
from flask_pydantic import validate
from werkzeug.exceptions import InternalServerError, Unauthorized

# Custom Libraries
import params
from data import prepareFeatures
from model import loadModel
from authent import Authent
from credential import Credentials



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getAPIModels():
   '''
   DESCRIPTION
      Cette fonction renvoie la liste des modèles disponibles pour l'API sous forme d'un dictionnaire.
      Les clés du dictionnaire correspondront à l'ID des modèles.
   RETOUR
      dict
   '''
   with open(params.API_MODEL_LIST_FILEPATH, 'r') as jsonFile:
      models = json.load(jsonFile)
   models = models.get('api_models')
   if models is None:
      models = {}
   return models



def getAPIModel(modelId):
   '''
   DESCRIPTION
      Cette fonction retourne un dictionnaire correspondant au modèle dont l'id est <modelId>
   RETURN
      dict
   '''
   # Retrieving list of all models
   models = getAPIModels()
   if models is None:
      return None
   return models.get(modelId)



def getModelInstance(modelId):
   '''
   DESCRIPTION
      Cette fonction retourne une instance de modèle scikit learn correspondant à l'id donné: <modelId>
   RETURN
      scikit learn model instance
   '''
   # Retrieving list of all models
   models = getAPIModels()
   if models is None:
      return None
   model = models.get(modelId)
   if model is None:
      return None
   filename = model.get('filename')
   if filename is None:
      return None
   # Envoie de l'instance du modèle
   return loadModel(filename)




def extractCredentials(authentKey):
   '''
   DESCRIPTION
      Cette fonction requiert le couple (login / password) fourni par l'utilisateur pour s'authentifier.
      A noter que la fonction s'attend à ce que l'argument <authentKey> soit encodé de la façon suivante:
         base64('<login>:<password>')
      où
         <login>   : correspond au username
         <password>: le password correspondant au username
   RETURN
      La fonction retournera le tuple suivant:
      (username, password)
   '''
   decodedCred = base64.b64decode(authentKey).decode(encoding='utf-8')
   fields = decodedCred.split(":")
   if len(fields) != 2:
      raise Exception('ERROR: invalid format for credentials. Expected format is:\nbase64("<login>:<password>")')
   return ( fields[0], fields[1] )



def authenticate(username, password):
   return apiAuthent.authenticate(username, password)








#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# API
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

api        = Flask('project-2')
apiAuthent = Authent(Credentials())


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# API parameters
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ModelPredictionParams(BaseModel):
   model_id: str
   features: dict



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# API routes
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@api.route('/status')
def get_status():
   return {
         'context': 'formation Data Engineer'
      ,  'api'    : 'project #2 - déploiement'
      ,  'authors': ['Christelle PATTYN', 'David CHARLES-ELIE-NELSON']
      ,  'status' : 'ok'
   }



@api.route('/models')
def get_models():
   try:
      # Retrieving list of all models
      models = getAPIModels()

      modelList = []
      for id, item in models.items():
         model = {
               'id'       : id
            ,  'type'     : item.get('type')
            ,  'available': False
         }

         try:
            modelInstance = loadModel(item.get('filename'))
         except Exception as err:
            print('Warning: Exception raised wile loading model: ', str(err))
            modelInstance = None

         if modelInstance is not None:
            model['available'] = True

         modelList.append(model)

      return { 'models': modelList }

   # Converting all errors in InternalServerError
   except Exception as err:
      raise InternalServerError(
         description = 'Internal Server Error' if not params.DEBUG else str(err)
      )



@api.route('/performance/models')
def get_performance_models():
   try:
      # Retrieving a list of all models
      models = getAPIModels()

      result = []
      for id, item in models.items():
         model = {
               'model_id'     : id
            ,  'model_type'   : item.get('type')
            ,  'model_score'  : None
         }

         try:
            modelInstance = loadModel(item.get('filename'))
         except Exception as err:
            print('Warning: Exception raised wile loading model: ', str(err))
            modelInstance = None

         if modelInstance is not None:
            model['model_score'] = modelInstance.best_score_
            model['metric_name'] = modelInstance.get_params().get('scoring')

         result.append(model)

      return { 'performances': result }

   # Converting all errors in InternalServerError
   except Exception as err:
      raise InternalServerError(
         description = 'Internal Server Error' if not params.DEBUG else str(err)
      )



@api.route('/performance/model/<string:modelId>')
def get_performance_model(modelId):
   try:
      # Retrieving a list of all models
      model = getAPIModel(modelId)

      result = {
            'model_id'     : modelId
         ,  'model_type'   : model.get('type')
         ,  'model_score'  : None
      }

      try:
         modelInstance = loadModel(model.get('filename'))
      except Exception as err:
         print('Warning: Exception raised wile loading model: ', str(err))
         modelInstance = None

      if modelInstance is not None:
         result['model_score'] = modelInstance.best_score_
         result['metric_name'] = modelInstance.get_params().get('scoring')
      else:
         Exception('Failed to load the model')

      return { 'performance': result }

   # Converting all errors in InternalServerError
   except Exception as err:
      raise InternalServerError(
         description = 'Internal Server Error' if not params.DEBUG else str(err)
      )



@api.route('/authent')
def authent():
   userLogin, userPassword = extractCredentials(request.headers.get('Authentication'))
   if apiAuthent.authenticate(userLogin, userPassword):
      return {
            'service': 'authentication'
         ,  'username': userLogin
         ,  'status': 'SUCCESS'
      }
   return make_response(
         {
               'service': 'authentication'
            ,  'username': userLogin
            ,  'status': 'FAILURE'
         }
      ,  401
   )



@api.route('/prediction', methods=['POST'])
@validate()
def post_predict_model(body:ModelPredictionParams):
   # Cette route nécessite une authentification
   try:

      try:
         # Récupération des crédentials fournis par l'utilisateur pour s'authentifier
         userLogin, userPassword = extractCredentials(request.headers.get('Authentication'))

         # Authentification
         if not apiAuthent.authenticate(userLogin, userPassword):
            raise Exception('Authentication failed !')
      except:
         raise Unauthorized


      # Récupération de l'identfiant du modèle ainsi que des features depuis le corps de la requête
      modelId      = body.model_id
      userFeatures = body.features

      # Préparation des features pour le modèle
      features = prepareFeatures(userFeatures)

      if params.DEBUG:
         print('\nFeatures are now prepared for the model:')
         print('   shape[features]: ', features.shape)
         print('   info: ')
         features.info()
         nbNulls = features.isnull().sum().sum()
         print('Features with null value: ')
         print('   count: ', nbNulls)
         if nbNulls > 0:
            print('   list:')
            print(features.columns[features.isnull().any()])

      # Chargement du modèle
      model = getModelInstance(modelId)
      if params.DEBUG:
         print('\nInstance model loaded:')
         print(model)

      # On effectue la prédiction par le modèle
      pred = model.predict_proba(features)
      if params.DEBUG:
         print('\nPrediction returned by the model:')
         print('   prediction: ', pred)

      probaNoRainTomorrow = pred[0,0]
      probaRainTomorrow   = pred[0,1]

      result = {
            'classesProba': [ probaNoRainTomorrow, probaRainTomorrow]
         ,  'classes'     : ['no_rain', 'rain']
      }

      if probaNoRainTomorrow == probaRainTomorrow:
         result['msg'] = f'Le modèle prédit qu\'il y aura autant de chance qu\'il pleuve demain qu\'il ne pleuve pas: débrouillez-vous !!! :)'
      elif probaNoRainTomorrow > probaRainTomorrow:
         result['msg'] = f'Le modèle prédit qu\'il n\'y aura pas de pluie demain avec une certitude de: {round(probaNoRainTomorrow * 100, 2)} %'
      elif probaNoRainTomorrow < probaRainTomorrow:
         result['msg'] = f'Le modèle prédit de la pluie pour demain avec une certitude de: {round(probaRainTomorrow * 100, 2)} %'

      return result


   # Converting all errors in InternalServerError
   except Unauthorized:
      raise

   except Exception as err:
      raise InternalServerError(
         description = 'Internal Server Error' if not params.DEBUG else str(err)
      )