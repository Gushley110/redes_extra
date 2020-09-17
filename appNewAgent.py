from appConstants import SNMP_V1, SNMP_V2C
from snmpAgentInfo import SnmpAgentInfo

import snmpQuery
import re

def getAgentSysName(agentInfo):
    try:
        SYSTEM_NAME = '1.3.6.1.2.1.1.5.0'
        responseValues = snmpQuery.snmpGet(
                agentInfo.snmpVersion,
                agentInfo.community,
                agentInfo.address,
                agentInfo.port,
                [SYSTEM_NAME]
            )
        return responseValues[SYSTEM_NAME]
    except:
        print('Error al intentar conectar con el agente.')
    return None

def getAddress():
    while True:
        address = input('Ingrese la direccion del agente: ')
        address = address.strip()
        if not address:
            print('Por favor ingresa una direccion.')
            continue
        return address

def getPort():
    pattern = re.compile('^\d+$')
    while True:
        port = input('Ingrese el puerto: ').strip()
        if not port:
            print('Por favor ingresa un puerto.')
            continue
        if not pattern.match(port):
            print('Ingresa un puerto valido.')
            continue
        return int(port)

def getCommunity():
    pattern = re.compile('^\w+$', re.ASCII)
    while True:
        community = input('Ingrese la comunidad: ').strip()
        if not community:
            print('Por favor ingresa la comunidad.')
            continue
        if not pattern.match(community):
            print('Ingresa una comunidad valida.')
            continue
        return community

def getVersion():
    pattern = re.compile('^\d$')
    while True:
        version = input('Ingrese la version SNMP (v1 = 1, v2c = 2): ')
        version = version.strip()
        if not version:
            print('Por favor selecciona una opcion.')
            continue
        if not pattern.match(version):
            print('Ingresa solo un digito para la opcion.')
            continue
        version = int(version) - 1
        if version < SNMP_V1 or SNMP_V2C < version:
            print('Ingresa una opción valida.')
            continue
        return version

def newAgent():
    address = getAddress()
    port = getPort()
    community = getCommunity()
    version = getVersion()

    agentInfo = SnmpAgentInfo(address, port, community, version)
    agentName = getAgentSysName(agentInfo)

    if agentName == None:
        print('Fallo al conectar con el agente, revisa la informacion: ', agentInfo) 
    else:
        print('El nombre del agente es ', agentName) 

    return agentInfo

