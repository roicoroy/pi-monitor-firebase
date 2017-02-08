import os
import json
import platform
import requests
import socket

from re import findall
from subprocess import check_output, CalledProcessError
from time import strftime

# ----------------- Stats Class
class Stats(object):
    def __init__(self):
        self.disk = "Unknown";
        self.ip = "Unknown";
        self.lastUpdateTime = strftime("%Y-%m-%d %H:%M:%S");
        self.networkName = "Unknown";
        self.os = "Unknown";
        self.temperature = 0;
        self.uptime = "Unknown";

    def setDisk(self, disk):
        self.disk = disk;

    def setIp(self, ip):
        self.ip = ip;

    def setNetworkName(self, networkName):
        self.networkName = networkName;

    def setOs(self, os):
        self.os = os;

    def setTemperature(self, temperature):
        self.temperature = temperature;

    def getTemperatureF(self):
        return (self.temperature * 9 / 5) + 32

    def setUptime(self, uptime):
        self.uptime = uptime;

    def toJson(self):
        jsonValues = {
            'disk': self.disk,
            'ip': self.ip,
            'lastUpdateTime': self.lastUpdateTime,
            'networkName': self.networkName,
            'os': self.os,
            'temperature': '{:.1f}'.format(self.temperature),
            'temperatureF': '{:.1f}'.format(self.getTemperatureF()),
            'uptime': self.uptime
        }
        return json.dumps(jsonValues, sort_keys=True);

# ----------------- Data Lookup Methods
def getDisk():
    bPerGB = 1000000000
    disk = {}
    st = os.statvfs('/')
    disk['free'] = '{:.1f}'.format(st.f_bavail * st.f_frsize / bPerGB)
    disk['total'] = '{:.1f}'.format(st.f_blocks * st.f_frsize / bPerGB)
    disk['used'] = '{:.1f}'.format((st.f_blocks - st.f_bfree) * st.f_frsize / bPerGB)
    return disk;

def getIp():
    # http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    ip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
    return ip;

def getNetworkName():
    return socket.getfqdn();

def getOs():
    platformData = {};
    platformData["platform"] = platform.platform();
    platformData["system"] = platform.system();
    platformData["release"] = platform.release();
    platformData["version"] = platform.version();
    return platformData;

def getTemperature():
    try:
        temp = check_output(["vcgencmd", "measure_temp"]).decode("UTF-8");
        temp = float(findall("\d+\.\d+",temp)[0]);
        return(temp);
    except OSError as e:
        return 0;

def getUptime():
    try:
        # See if -p (pretty) format works
        raw = check_output(["uptime", "-p"]);
        uptimeStart = raw.find('up') + 3;
        uptime = raw[uptimeStart:];
    except CalledProcessError as e:
        # Pretty didn't work
        raw = check_output(["uptime"]);
        uptimeStart = raw.find('up') + 3;
        firstComma = raw.find(',', uptimeStart);
        secondComma = raw.find(',', firstComma + 1);
        uptime = raw[uptimeStart:secondComma];

    return uptime;

# ----------------- Firebase

def firebasePut(path, data):
    requests.put(getFirebaseUrl(path), params=getFirebaseQueryParams(), data=data)

def getFirebaseQueryParams():
    return {'auth': config.get('auth')}

def getFirebaseUrl(path):
    return '{}/{}/{}'.format(config.get('base_url'), config.get('pi_name'), path)

# ----------------- Load Configuration

config = json.load(open("/home/pi/config-monitor.json"));
# config = json.load(open("config.json"));

# ----------------- Run
stats = Stats();
stats.setDisk(getDisk());
stats.setIp(getIp());
stats.setNetworkName(getNetworkName());
stats.setOs(getOs());
stats.setTemperature(getTemperature());
stats.setUptime(getUptime());

firebasePut('status.json', stats.toJson());
# print stats.toJson();
