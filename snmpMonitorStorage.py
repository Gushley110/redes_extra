from utilityFunctions import BuildDataSourceString

import appConstants
import rrdtool
import shutil
import os

class SnmpMonitorStorage:

    def __init__(self, snmpAgentInfo):
        self.makeStorageFile(snmpAgentInfo)
        self.createDatabase()

    def makeStorageFile(self, snmpAgentInfo):
        self.path = snmpAgentInfo.getIdentifier() 

        #if os.path.exists(self.path):
        #    shutil.rmtree(self.path)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.fileName = '/' + appConstants.DB_FILENAME
        self.fileName = self.path + self.fileName

    def createDatabase(self):
        if os.path.isfile(self.fileName):
            return

        dataSources = []
        for name in appConstants.SIMPLE_NODES:
            dataSources.append(
                    BuildDataSourceString(name, 
                        appConstants.NAME_TO_RRDTYPE[name])
                )
        for name in appConstants.COMPLEX_NODES:
            dataSources.append(
                    BuildDataSourceString(name,
                        appConstants.NAME_TO_RRDTYPE[name])
                )
        errorCode = rrdtool.create(self.fileName,
                '--start', appConstants.RRD_NOW,
                '--step', appConstants.RRD_STEP,
                *dataSources,
                'RRA:AVERAGE:0.5:1:270',
            )

        if errorCode:
            logging.error('Error creating RRDTool file : %s',
                rrdtool.error())
            raise
    
    def updateDatabase(self, updateValues):
        updateString = appConstants.RRD_NOW 
        for name in appConstants.SIMPLE_NODES:
            updateString += ':'
            if name in updateValues:
                updateString += str(updateValues[name])
            else:
                updateString += appConstants.RRD_UNKNOWN
        for name in appConstants.COMPLEX_NODES:
            updateString += ':'
            if name in updateValues:
                updateString += str(updateValues[name])
            else:
                updateString += appConstants.RRD_UNKNOWN
        rrdtool.update(self.fileName, updateString)

