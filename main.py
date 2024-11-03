#############################################
#############################################
##
##  Import modules
##
#############################################
#############################################

from dotenv import load_dotenv
import logger_app
import os

#############################################
#############################################
##
##  Prepare logging
##
#############################################
#############################################

logger = logger_app.prepareLogger(__name__)
logger.debug("Logger is active now!")

#############################################
#############################################
##
##  Load .env config and check items
##
#############################################
#############################################

if load_dotenv(".env"):
    required_items = {"discord-bot-token", "vk-api-token"}
    optimal_items = {}
    
    not_found = set()
    for item in required_items:
        if item not in os.environ.keys():
            logger.warning("Not found required item <{item}> in .env file!")
            not_found.add(item)
    
    if len(not_found) != 0:
        logger.critical("Add missed required items!")
        exit(1)
    
    for item in optimal_items:
        if item not in os.environ.keys() and os.environ.get("print-missed-items", True):
            logger.warning("Not found optimal item <{item}> in .env file!")
    
    logger.info(".env config loaded!")
else:
    logger.critical("Not found .env file with config!")
    exit(1)

#############################################
#############################################
##
##  Import modules
##
#############################################
#############################################


