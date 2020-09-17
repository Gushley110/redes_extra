import appConstants
import logging

class SnmpAgentInfo:

    def __init__(self, address, port, community, snmpVersion = appConstants.SNMP_V2C):
        self.snmpVersion = snmpVersion
        self.community = community
        self.identifier = None
        self.address = address
        self.port = port

    def getIdentifier(self):
        if self.identifier:
            return self.identifier

        identifier = '-'.join(self.address.split('.'))
        identifier += ('-' + str(self.port) + '-')
        identifier += self.community
        self.identifier = identifier

        return identifier

    def __str__(self):
        return '[SNMPv{0}, {1}, {2}, {3}]'.format(
            self.snmpVersion + 1,
            self.community,
            self.address,
            self.port,
        )

