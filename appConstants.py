#SNMP Version Constants according to the API.

SNMP_V2C = 1
SNMP_V1 = 0

#Monitor Constants.

MONITOR_FREQ = 10

#Nodes to be monitored.

SIMPLE_NODES = sorted(
        [
            'ipInReceives',
            'icmpOutEchos',
            'tcpInSegs',
            'udpOutDatagrams'
        ]
    )

COMPLEX_NODES = sorted(
        [
            'ifInUcastPkts'
        ]
    )

'''NAME_TO_OID = {
        'ifOutNUcastPkts'   : '1.3.6.1.2.1.2.2.1.18',
        'tcpRetransSegs'    : '1.3.6.1.2.1.6.12.0',
        'ipOutRequests'     : '1.3.6.1.2.1.4.10.0',
        'udpOutDatagrams'   : '1.3.6.1.2.1.7.4.0', 
        'icmpInMsgs'        : '1.3.6.1.2.1.5.1.0'
    }'''

NAME_TO_OID = {
    'ifInUcastPkts'     :   '1.3.6.1.2.1.2.2.1.11',
    'ipInReceives'      :   '1.3.6.1.2.1.4.3.0',
    'icmpOutEchos'      :   '1.3.6.1.2.1.5.21.0',
    'tcpInSegs'         :   '1.3.6.1.2.1.6.10.0',
    'udpOutDatagrams'   :   '1.3.6.1.2.1.7.4.0'
}

COMPLEX_OIDS = [NAME_TO_OID[name] for name in COMPLEX_NODES]
SIMPLE_OIDS = [NAME_TO_OID[name] for name in SIMPLE_NODES]

OID_TO_NAME = dict()
for x in range(0, len(COMPLEX_OIDS)):
    OID_TO_NAME[COMPLEX_OIDS[x]] = COMPLEX_NODES[x]
for x in range(0, len(SIMPLE_OIDS)):
    OID_TO_NAME[SIMPLE_OIDS[x]] = SIMPLE_NODES[x]

#RRDTool Constants

DB_FILENAME = 'snmp.rrd'
RRD_COUNTER = 'COUNTER'
RRD_THRESHOLD = '60'
RRD_UNKNOWN = 'U'
RRD_STEP = '20'
RRD_NOW = 'N'

NAME_TO_RRDTYPE = {
        'ifInUcastPkts'   : RRD_COUNTER,
        'ipInReceives'   : RRD_COUNTER,
        'icmpOutEchos'    : RRD_COUNTER, 
        'tcpInSegs'     : RRD_COUNTER,
        'udpOutDatagrams'        : RRD_COUNTER
    }

#Report Generator Constants.

TEMPLATE_FILE = 'reportTemplate.html'

