from snmpMonitorStorage import SnmpMonitorStorage
from threading import Thread

import appConstants
import snmpQuery
import logging
import time
import sys

class SnmpAgentMonitor(Thread):

    def __init__(self, snmpAgentInfo):
        Thread.__init__(self)
        self.storage = SnmpMonitorStorage(snmpAgentInfo)
        self.snmpAgentInfo = snmpAgentInfo
        self.running = True
        self.start()

    def stop(self):
        self.running = False

    def __del__(self):
        self.stop()

    def run(self):
        while self.running:
            try:
                updateValues = dict()

                responses = snmpQuery.snmpGet(
                        self.snmpAgentInfo.snmpVersion,
                        self.snmpAgentInfo.community,
                        self.snmpAgentInfo.address,
                        self.snmpAgentInfo.port,
                        appConstants.SIMPLE_OIDS
                    )
                if responses:
                    for oid in responses:
                        name = appConstants.OID_TO_NAME[oid]
                        updateValues[name] = responses[oid]
            
                for oid in appConstants.COMPLEX_OIDS:
                    responses = snmpQuery.snmpWalk(
                            self.snmpAgentInfo.snmpVersion,
                            self.snmpAgentInfo.community,
                            self.snmpAgentInfo.address,
                            self.snmpAgentInfo.port,
                            oid
                        )

                    if responses:
                        total = 0
                        for key in responses:
                            total += int(responses[key])
                        name = appConstants.OID_TO_NAME[oid]
                        updateValues[name] = str(total)

                self.storage.updateDatabase(updateValues)
                
                time.sleep(appConstants.MONITOR_FREQ)                

            except:
                logging.error('Exception while monitoring %s : %s',
                    self.snmpAgentInfo, sys.exc_info())
                self.stop()

