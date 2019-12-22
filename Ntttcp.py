from . import TrafficToolsLocator
import platform
import subprocess
from .cmd_executor_result import Cmd_executor_result


def ntttcpFlagsFactory():
    if "win" in platform.platform().lower():
        return NtttcpFlagsWindows()
    return NtttcpFlagsLinux()


class Ntttcp():

    def __init__(self, time, serverIP,sessions=4,processor="*", bufferLength=None,  numberOfBuffers=None, portBase=None,
                 coolDownSeconds=None, isIPV6=False):
        self.time = time
        self.bufferLength = bufferLength
        self.numberOfBuffers = numberOfBuffers
        self.sessions = sessions
        self.processor = processor
        self.portBase = portBase
        self.coolDownSeconds = coolDownSeconds

        self.isIPV6 = isIPV6
        self.result = None
        self.serverIP = serverIP
        self.ntttcpFlags = ntttcpFlagsFactory()
        self.ntttcpCMD = f"{TrafficToolsLocator.getLocator().getNtttcp()} -m {self.sessions},{self.processor},{self.serverIP} {self.ntttcpFlags.timeFlag} {self.time}" \
            f"{self.bufferLengthParams()}{self.numberOfBuffersParams()}{self.__ipv6Params()}"


    def getParameter(self, parameterFlag, parameterValue):
        if parameterValue is not None: return f" {parameterFlag} {parameterValue}"
        return""

    def bufferLengthParams(self):
        return self.getParameter(self.ntttcpFlags.bufferLength, self.bufferLength)

    def numberOfBuffersParams(self):
        return self.getParameter(self.ntttcpFlags.numberOfBuffers, self.numberOfBuffers)

    def __coolDownSecondsParams(self):
        return self.getParameter(self.ntttcpFlags.coolDownSeconds, self.coolDownSeconds)

    def __mappingParams(self):
        return self.getParameter(self.ntttcpFlags.mappingFlag, self.mapping)

    def __portBaseParams(self):
        return self.getParameter(self.ntttcpFlags.portBaseFlag, self.portBase)

    def __ipv6Params(self):
        if self.isIPV6: return f" {self.ntttcpFlags.ipv6Flag}"
        return ""

    def run(self):
        self.__runNtttcp()
    def isAlive(self):
        if self.process.poll() ==None:
            return True
        return False
    def getResult(self):
        if self.result is None:
            std_out, std_err = self.process.communicate()
            self.result = Cmd_executor_result(std_out, std_err, self.process.returncode, command=self.ntttcpCMD)
        return self.result


    def __runNtttcp(self):
        print("Running CMD: " + self.ntttcpCMD)

        p = subprocess.Popen(self.ntttcpCMD,  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True,
                             stdin=subprocess.PIPE)
        self.process = p

class NtttcpTCPClient(Ntttcp):
    def __init__(self, time, serverIP,
                 bufferLength=None, numberOfBuffers=None, portBase=None,
                 coolDownSeconds=None,sessions=4,processor="*" , isIPV6=False, clientBindedIp=None):
        Ntttcp.__init__(self,time, serverIP,sessions,processor ,bufferLength, numberOfBuffers, portBase, coolDownSeconds, isIPV6)
        self.clientBindedIp = clientBindedIp
        self.ntttcpCMD += f" {self.ntttcpFlags.clientFlag}{self.__clientBindedIpParams()}"

    def __clientBindedIpParams(self):

        return self.getParameter(self.ntttcpFlags.clientBindedIpFlag,
                                                                  self.clientBindedIp)


class NtttcpUDPClient(NtttcpTCPClient):
    def __init__(self, time, serverIP,sessions=4,processor="*", bufferLength=None, numberOfBuffers=None, portBase=None,
                 coolDownSeconds=None,  isIPV6=False, clientBindedIp=None):
        NtttcpTCPClient.__init__(self,time, serverIP,sessions,processor, bufferLength, numberOfBuffers, portBase, coolDownSeconds,
                                 isIPV6, clientBindedIp)
        self.ntttcpCMD += f" {self.ntttcpFlags.udpFlag}"


class NtttcpTCPServer(Ntttcp):
    def __init__(self, time, serverIP, bufferLength=None, numberOfBuffers=None, portBase=None,
                 coolDownSeconds=None,  isIPV6=False,sessions=4,processor="*",):
        Ntttcp.__init__(self,time, serverIP,sessions,processor, bufferLength, numberOfBuffers, portBase, coolDownSeconds, isIPV6)
        self.ntttcpCMD += f" {self.ntttcpFlags.serverFlag}"


class NtttcpUDPServer(NtttcpTCPServer):
    def __init__(self, time, serverIP, bufferLength=None, numberOfBuffers=None, portBase=None,
                 coolDownSeconds=None,  isIPV6=False,sessions=4,processor="*",):
        NtttcpTCPServer.__init__(self,time, serverIP,sessions,processor, bufferLength, numberOfBuffers, portBase, coolDownSeconds,
        isIPV6)
        self.ntttcpCMD += f" {self.ntttcpFlags.udpFlag}"


'This class is responsible for getting the flag of a  Ntttcp parametr by os'


class NtttcpFlags():
    def __init__(self):
        self.bufferLength = "-l"
        self.numberOfBuffers = "-n"
        self.coolDownSeconds = "-cd"
        self.clientFlag = "-s"
        self.udpFlag = "-u"
        self.serverFlag = "-r"
        self.timeFlag = "-t"
        self.mappingFlag = "-m"
        self.portBaseFlag = "-p"
        self.ipv6Flag = "-6"
        self.clientBindedIpFlag = "-nic"
        #TODO implement the other flags

# NTttcp: [-s|-r|-l|-n|-p|-sp|-a|-rb|-sb|-u|-w|-d|-t|-cd|-wu|-v|-6|-wa|-nic|-xml] -m <mapping> [mapping]
#
#         -s   work as a sender
#         -r   work as a receiver
#         -l   <Length of buffer>         [default TCP:  64K, UDP: 128]
#         -n   <Number of buffers>        [default:  20K]
#         -p   <port base>                [default: 5001]
#         -sp  synchronize data ports, if used -p should be same on every instance
#         -a   <outstanding I/O>          [default:    2]
#         -rb  <Receive buffer size>      [default:  64K]
#         -sb  <Send buffer size>         [default:   8K]
#                                    -a : [default:    0]
#                <Send buffer size> < 0 : system default
#         -u   UDP send/recv
#         -w   WSARecv/WSASend
#         -d   Verify Flag
#         -t   <Runtime> in seconds. When with -n mans max test time and disables
#              -wu and -cd flags.         [default (with -n): 3h]
#         -cd  <Cool-down> in seconds
#         -wu  <Warm-up> in seconds
#         -v   enable verbose mode
#         -6   enable IPv6 mode
#         -wa  Sets the WAIT_ALL flag when using recv or WSARecv functions
#         -nic <NIC IP>
#              Use NIC with <NIC IP> for sending data (sender only).
#         -xml [filename] save XML output to a file, by default saves to xml.txt
#         -m   <mapping> [mapping]
#              where a mapping is a session(s),processor,StartReceiver IP set
#              e.g. -m 4,0,1.2.3.4 sets up:
#              4 sessions on processor 0 to test a network on 1.2.3.4
# ERROR: main failed: error in parameters
class NtttcpFlagsWindows(NtttcpFlags):
    def __init__(self):
        NtttcpFlags.__init__(self)


class NtttcpFlagsLinux(NtttcpFlags):
    def __init__(self):
        NtttcpFlags.__init__(self)
