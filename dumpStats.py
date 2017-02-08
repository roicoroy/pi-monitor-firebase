import json
import requests

# ----------------- Firebase

def firebaseGet(path):
    return requests.get(getFirebaseUrl(path), params=getFirebaseQueryParams())

def getFirebaseQueryParams():
    return {'auth': config.get('auth')}

def getFirebaseUrl(path):
    return '{}/{}/{}'.format(config.get('base_url'), config.get('pi_name'), path)

# ----------------- Load Configuration

# config = json.load(open("/home/pi/config-monitor.json"));
config = json.load(open("config.json"));

# ----------------- Run
jsonUgly = firebaseGet('status.json').json();
print json.dumps(jsonUgly, sort_keys=True, indent=4, separators=(',', ': '))
