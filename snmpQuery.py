import pysnmp.hlapi as snmp

import logging

# community : The comunnity name.
# host : The agent address/ hostname.
# oids : A list of  Object Identifiers to query.
# port : The port where SNMP is running on the agent.

def snmpGet(snmpVersion, community, host, port, oids):

    logging.info('New Get Query [v:%d, %s, %s, %d, %s]', 
        snmpVersion, community, host, port, oids)

    objectTypes = [snmp.ObjectType(snmp.ObjectIdentity(oid)) for oid in oids]

    errorIndication, errorStatus, errorIndex, varBinds = next(
            snmp.getCmd(snmp.SnmpEngine(),
                snmp.CommunityData(community, mpModel = snmpVersion),
                snmp.UdpTransportTarget((host, port)),
                snmp.ContextData(),
                *objectTypes
            )
        )

    if errorIndication: 
        logging.error(errorIndication)
        return None

    if errorStatus:
        logging.error('%s at %s', errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
        return None

    results = [(str(name), str(value)) for name, value in varBinds]

    return dict(results)

def snmpWalk(snmpVersion, community, host, port, oid):

    logging.info('New Walk Query [v:%d, %s, %s, %d, %s]', 
        snmpVersion, community, host, port, oid)

    generator = snmp.nextCmd(snmp.SnmpEngine(),
            snmp.CommunityData(community, mpModel = snmpVersion),
            snmp.UdpTransportTarget((host, port)),
            snmp.ContextData(),
            snmp.ObjectType(snmp.ObjectIdentity(oid)),
            lexicographicMode = False
        )
    
    results = dict()

    for errorIndication, errorStatus, errorIndex, varBinds in generator: 
        if errorIndication: 
            logging.error(errorIndication)
            continue

        if errorStatus:
            logging.error('%s at %s', errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
            continue

        for name, value in varBinds:
            results[str(name)] = str(value)

    return results

