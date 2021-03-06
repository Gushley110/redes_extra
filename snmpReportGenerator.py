from appConstants import DB_FILENAME, TEMPLATE_FILE

import snmpQuery
import rrdtool
import pdfkit
import jinja2
import os

class SnmpReportGenerator:

    def __init__(self, agentInfo):
        self.resourceFolder = agentInfo.getIdentifier()
        self.agentInfo = agentInfo
        self.loadTemplate()

    def loadTemplate(self):
        templateLoader = jinja2.FileSystemLoader(searchpath = './')
        templateEnv = jinja2.Environment(loader = templateLoader)
        self.template = templateEnv.get_template(TEMPLATE_FILE)
    
    # This has to be cleaner.
    def renderGraphs(self, startTime, endTime):
        rrdtool.graph(self.resourceFolder + '/ifInUcastPkts.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=Packets/s',
                'DEF:{0}={1}:{2}:{3}'.format('inucast',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'ifInUcastPkts',
                        'AVERAGE'
                    ),
                'AREA:inucast#0000FF:Paquetes Multicast Recibidos'
            )
        rrdtool.graph(self.resourceFolder + '/ipInReceives.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=Packets/s',
                'DEF:{0}={1}:{2}:{3}'.format('ipin',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'ipInReceives',
                        'AVERAGE'
                    ),
                'AREA:ipin#00FF00:IP Recibidos'
            )
        rrdtool.graph(self.resourceFolder + '/icmpOutEchos.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=ICMP Msgs/s',
                'DEF:{0}={1}:{2}:{3}'.format('icmpout',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'icmpOutEchos',
                        'AVERAGE'
                    ),
                'AREA:icmpout#FF0000:Mensajes ICMP echo salientes'
            )
        rrdtool.graph(self.resourceFolder + '/tcpInSegs.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=TCP Segments',
                'DEF:{0}={1}:{2}:{3}'.format('tcpin',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'tcpInSegs',
                        'AVERAGE'
                    ),
                'AREA:tcpin#000000:Segmentos TCP Recibidos'
            )
        rrdtool.graph(self.resourceFolder + '/udpOutDatagrams.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=UDP Datagrams/s',
                'DEF:{0}={1}:{2}:{3}'.format('udpout',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'udpOutDatagrams',
                        'AVERAGE'
                    ),
                'AREA:udpout#777777:Datagramas enviados.'
            )

    def getAgentSysInfo(self):
        return snmpQuery.snmpWalk(
                self.agentInfo.snmpVersion,
                self.agentInfo.community,
                self.agentInfo.address,
                self.agentInfo.port,
                '1.3.6.1.2.1.1',
            )

    def getInterfaceInfo(self):
        return snmpQuery.snmpWalk(
                self.agentInfo.snmpVersion,
                self.agentInfo.community,
                self.agentInfo.address,
                self.agentInfo.port,
                '1.3.6.1.2.1.2',
            )

    def getCpuInfo(self):
        return snmpQuery.snmpWalk(
                self.agentInfo.snmpVersion,
                self.agentInfo.community,
                self.agentInfo.address,
                self.agentInfo.port,
                '1.3.6.1.2.1.25.3.3.1.2',
            )

    def getRAMInfo(self):
        return snmpQuery.snmpWalk(
                self.agentInfo.snmpVersion,
                self.agentInfo.community,
                self.agentInfo.address,
                self.agentInfo.port,
                '1.3.6.1.4.1.2021.4',
            )

    def getDiskInfo(self):
        return snmpQuery.snmpWalk(
                self.agentInfo.snmpVersion,
                self.agentInfo.community,
                self.agentInfo.address,
                self.agentInfo.port,
                '1.3.6.1.2.1.25.3.6.1',
            )

    def getDiskCapacities(self):
        return snmpQuery.snmpWalk(
                self.agentInfo.snmpVersion,
                self.agentInfo.community,
                self.agentInfo.address,
                self.agentInfo.port,
                '1.3.6.1.2.1.25.3.6.1.4',
            )
    
    def renderHTML(self):
        sysInfo = self.getAgentSysInfo()
        ifInfo = self.getInterfaceInfo()
        raminfo = self.getRAMInfo()
        cpuInfo = self.getCpuInfo()
        diskInfo = self.getDiskInfo()
        diskCapacities = self.getDiskCapacities()

        # This is just because I'm rushing
        sysDescr = sysInfo['1.3.6.1.2.1.1.1.0'].lower()
        numberInterfaces = ifInfo['1.3.6.1.2.1.2.1.0'].lower()
        numberCpu = len(cpuInfo)
        numberDisk = len(diskInfo) // 4

        interfaceIn = []
        interfaceOut = []
        cpuLoads = []
        capacities = []

        for i in range(1, int(numberInterfaces) + 1):
            interfaceIn.append(ifInfo['1.3.6.1.2.1.2.2.1.10.' + str(i)])
            interfaceOut.append(ifInfo['1.3.6.1.2.1.2.2.1.16.' + str(i)])

        for load in cpuInfo.values():
            cpuLoads.append(load)

        for capacity in diskCapacities.values():
            capacities.append(capacity)

        logo = 'mine.png' # Minecraft logo fallback for the memes.
        if 'windows' in sysDescr:
            logo = 'windows.png'
        elif 'linux' in sysDescr:
            logo = 'linux.png'

        self.renderedHTML = self.template.render(
                agentOSLogo = os.path.abspath(logo),
                agentSysName = sysInfo['1.3.6.1.2.1.1.5.0'],
                agentSysDescr = sysInfo['1.3.6.1.2.1.1.1.0'],
                agentSysUpTime = sysInfo['1.3.6.1.2.1.1.3.0'],
                agentSysContact = sysInfo['1.3.6.1.2.1.1.4.0'],
                agentSysLocation = sysInfo['1.3.6.1.2.1.1.6.0'],
                agentInterfaces = ifInfo['1.3.6.1.2.1.2.1.0'],
                agentTraficIn = interfaceIn,
                agentTraficOut = interfaceOut,
                agentDisks = numberDisk,
                agentDiskCapacity = capacities,
                agentCpuCores = numberCpu,
                agentCpuLoads = cpuLoads,
                agentRAM = raminfo['1.3.6.1.4.1.2021.4.5.0']
            )

    

    def makeReport(self, fileName, startTime, endTime):
        options = {
            "enable-local-file-access": None
        }
        self.renderGraphs(startTime, endTime)
        self.renderHTML()
        pdfkit.from_string(self.renderedHTML, fileName + '.pdf',options=options)
