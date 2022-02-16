#!/bin/bash
########################################################################################################################
# DESCRIPTION
#     Ce script a pour but de préparer les images Docker qui seront utilisées pour héberger l'API et instancier les
#     containers clients (chargés de tester l'API).
#     AVANT d'exécutez ce script lisez l'AVERTISSEMENT ci-dessous.
#
# SYNTAXE
#     setup.sh [<repoName>]
#
#        - Si un nom de compte DockerHub (<repoName>) est fourni au script alors les images seront tagguées comme suit:
#              <repoName>/<imageName>:latest
#          Les images seront de plus poussées automatiquement sur ce compte DockerHub.
#
#        - Si aucun nom de compte DockerHub n'est précisé alors les images seront tagguées comme suit:
#              <imageName>:latest
#          Les images seront donc locales sur la machine où ce script aura été exécuté.
#          Attention donc dans ce cas à faire attention à rendre disponible ces images sur la machine où seront
#          instanciés les clients et l'API.
#
# AVERTISSEMENT
#     Si vous renseignez un nom de compte DockerHub assurez-vous, AVANT de lancer ce script, que vous parvenez à vous
#     y connecter avec la commande suivante (depuis la machine sur laquelle ce script sera exécuté):
#        docker login -u <repoName>
#     Un mot de passe vous sera demandé de façon interactive et en cas de connexion réussie docker conservera de quoi
#     se connecter à ce même compte sans demander de nouveau le mot de passe. Cette étape préliminaire est essentielle
#     pour ce script qui ne gère pas la demande de mot de passe de façon interactive.
########################################################################################################################

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

declare -r PROG=`basename $0`
declare -r PROG_NAME=`basename $0 .sh`
declare -r PROG_PATH=`eval realpath $(dirname $0)`

declare -r SUCCESS=0
declare -r ERROR=2


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Paths
declare -r LOG_PATH="${PROG_PATH}/log"
declare -r DOCKER_PATH="${PROG_PATH}/docker"
declare -r DOCKER_IMAGES_PATH="${PROG_PATH}/build/docker/images"

# Filenames
declare -r LOGFILE="${LOG_PATH}/${PROG_NAME}.log"


# Docker image tags
declare DOCKER_IMG_TAG_UBUNTU_PYTHON="project2-ubuntu-python"
declare DOCKER_IMG_TAG_API_SERVER="project2-api-server"
declare DOCKER_IMG_TAG_CLIENT_TESTER="project2-client-tester"
declare DOCKER_IMAGE_TAGS=("${DOCKER_IMG_TAG_UBUNTU_PYTHON}" "${DOCKER_IMG_TAG_API_SERVER}" "${DOCKER_IMG_TAG_CLIENT_TESTER}")


# Docker files
declare -r DOCKERFILE_UBUNTU_PYTHON="${DOCKER_PATH}/Dockerfile.client"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function errMsg()
{
   echo -e "${PROG}: ERROR: $*" >&2
}



function checkRC()
{
   declare rc="$1"

   if [[ -z "${rc}" ]]; then
      errMsg "return code undefined. Please contact the administrator."
      return ${ERROR}
   fi

   (( rc == SUCCESS )) && {
      echo "[rc=${rc}]: OK"
      return ${SUCCESS}
   }

   errMsg "at least one error occurred !"
   echo "[rc=${rc}]: FAILED"
   exit ${ERROR}
}



function initLogFile()
{
   echo -e "\nInitializing logfile..."

   # Creating an empty log file if not already exists
   if [[ ! -e "${LOGFILE}" ]]; then
      cat /dev/null > "${LOGFILE}" || {
         errMsg "Failed to create file: \"${LOGFILE}\""
         return ${ERROR}
      }
   else
      # The logfile already exists: just checking that we have write permission on it
      if [[ ! -w "${LOGFILE}" ]]; then
         errMsg "Missing \"write\" permission on file : \"${LOGFILE}\""
         return ${ERROR}
      fi
   fi

   return ${SUCCESS}
}



function setDockerImageTags()
{
   if [[ -n "${DOCKERHUB_REPO}" ]]; then
      echo -e "\nA Docker Hub account has been specified: \"${DOCKERHUB_REPO}\""
      # Adjusting image tag names
      DOCKER_IMG_TAG_UBUNTU_PYTHON="${DOCKERHUB_REPO}/${DOCKER_IMG_TAG_UBUNTU_PYTHON}"
      DOCKER_IMG_TAG_API_SERVER="${DOCKERHUB_REPO}/${DOCKER_IMG_TAG_API_SERVER}"
      DOCKER_IMG_TAG_CLIENT_TESTER="${DOCKERHUB_REPO}/${DOCKER_IMG_TAG_CLIENT_TESTER}"
      DOCKER_IMAGE_TAGS=("${DOCKER_IMG_TAG_UBUNTU_PYTHON}" "${DOCKER_IMG_TAG_API_SERVER}" "${DOCKER_IMG_TAG_CLIENT_TESTER}")
   else
      echo -e "\nNo Docker Hub account has been specified: all docker images will be generated in this local machine only."
   fi

   return ${SUCCESS}
}



function buildDockerImage()
{
   echo -e "\nBuilding Docker image: "

   eval docker image build $@
   declare rc=$?

   return ${rc}
}



function buildDockerImages()
{
   declare -i rc=0

   for imgName in ${DOCKER_IMAGE_TAGS[@]}
   do
      echo -e "\nBuilding Docker image: \"${imgName}\"..."
      case "${imgName}" in
         "${DOCKER_IMG_TAG_UBUNTU_PYTHON}")
               opts="--file \"${DOCKER_IMAGES_PATH}/ubuntu-python/Dockerfile__ubuntu-python\""
               opts="${opts} --tag \"${imgName}:latest\""
               opts="${opts} --pull \"${PROG_PATH}\""
               ;;
         "${DOCKER_IMG_TAG_API_SERVER}")
               opts="--file \"${DOCKER_IMAGES_PATH}/api-server/Dockerfile__api-server\""
               opts="${opts} --tag \"${imgName}:latest\""
               opts="${opts} \"${PROG_PATH}\""
               ;;
         "${DOCKER_IMG_TAG_CLIENT_TESTER}")
               opts="--file \"${DOCKER_IMAGES_PATH}/client-tester/Dockerfile__client-tester\""
               opts="${opts} --tag \"${imgName}:latest\""
               opts="${opts} \"${PROG_PATH}\""
               ;;
      esac
      cmd="docker image build ${opts}"
      eval ${cmd}
      rc=$?
      (( rc != 0 )) && break
   done

   return ${rc}
}



function pushDockerImages()
{
   declare -i rc=0

   for imgName in ${DOCKER_IMAGE_TAGS[@]}
   do
      echo -e "\nPushing Docker image: \"${imgName}\"..."
      cmd="docker image push ${imgName}"
      eval ${cmd}
      rc=$?
      (( rc != 0 )) && break
   done

   return ${rc}
}


function init()
{
   setDockerImageTags || return ${ERROR}

   initLogFile || return ${ERROR}

   # Entering the current date in the log file
   echo -e "\nSTART: [${PROG}]: $(date +'%Y-%m-%d %H:%M:%S (UTC%:z)')" >> "${LOGFILE}"

   return ${SUCCESS}
}



function main()
{
   # Build Docker images
   buildDockerImages ; checkRC $?

   # Push Docker images to Docker Hub
   if [[ -n "${DOCKERHUB_REPO}" ]]; then
      pushDockerImages ; checkRC $?
   fi

   return ${SUCCESS}
}



########################################################################################################################
#
# MAIN PROGRAM starts here...
#
########################################################################################################################

# On récupère le nom du repo DockerHub (si spécifié)
DOCKERHUB_REPO="$1"

echo -e "\nRunning ${PROG} for project 2: API Deployment..."

init ; checkRC $?
main | tee -a "${LOGFILE}"

echo -e "\nAll Docker images are now ready !"
echo "You can now start the API server and run client containers..."

