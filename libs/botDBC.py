from libs.botClasses import *
from botConfig import botConfig as bc
import inspect
import os
import requests
from libs.botLogger import botLogger

# Why is that black van out there?
log = botLogger("waddlebot-dbc")
log.fileLogger("waddlebot-dbc.log")

#const
DEFAULT_CFG_FILENAME="config.yml"

#gitr done function classes

class botDb:
    def __init__(self, config: dict = None, dbc: dbinfo = None ):
        # our input
        self.dbc = dbc
        # These must initialize in order to be useful
        self.config = self.__importDBC()
        self.columns = self.__importColumns()
        # if you dont give me the goods, ill try to find them myself
        if self.dbc == None:
            log.debug("No dbinfo object given, trying to find config file based on default")
            call_abspath = os.path.abspath((inspect.stack()[0])[1])
            path = os.path.dirname(call_abspath) + DEFAULT_CFG_FILENAME
            self.dbc = bc(configPath=path).config["database"]
        # set the below to whatever request auth method you want before calling dbConnect functions
        self.auth = None

    def __importColumns(self):
        columns = self.config["columns"]
        columns.update(self.config["foreignKeys"])
        return columns

    def webdbRead(self, query: dbquery):
        requrl = "https://"+self.db.webhost+":"+self.db.webport+"/"+self.db.database+"/"+self.db.table+"/read"
        reqquery = {'columns': ','.join(query.columns), 'queryColumn': query.queryColumn, 'queryValue': query.queryValue}
try:
    response = requests.get(requrl, data=reqquery, auth=self.auth)
    response.raise_for_status()
    return response.json()
except requests.RequestException as err:
    log.error(f"Request failed: {err}")
    raise
except ValueError as err:
    log.error(f"JSON decoding failed: {err}")
    raise
        return None
    
    def webdbUpdate(self, query: dbquery):
        requrl = "https://"+self.db.webhost+":"+self.db.webport+"/"+self.db.database+"/"+self.db.table+"/update"
        reqquery = {'columns': ','.join(query.columns), 'queryColumn': query.queryColumn, 'queryValue': query.queryValue}
        try:
            response = requests.get(requrl, data=reqquery)
            responseJSON = response.json
            log.debug(responseJSON)
            return responseJSON['response']
        except Exception as err:
            log.error(err)
        return None