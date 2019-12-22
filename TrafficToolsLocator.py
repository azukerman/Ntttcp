from abc import  abstractmethod
import platform
def getLocator():
    if "win" in platform.platform().lower():
        return  TrafficToolsLocatorWindows()
    else: return  TrafficToolsLocatorLinux()
class TrafficToolsLocator:
    @abstractmethod
    def getNtttcp(self):pass

class TrafficToolsLocatorWindows(TrafficToolsLocator):
    def getNtttcp(self):
        return r"C:\exeOh\tools\NTttcp_x64.exe"


class TrafficToolsLocatorLinux(TrafficToolsLocator):
    def getNTttcp(self):
        return r"nttcp"