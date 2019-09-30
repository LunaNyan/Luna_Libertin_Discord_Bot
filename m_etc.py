import psutil, base64

def base64e(s):
    e = base64.b64encode(s.encode('utf-8'))
    e = str(e).replace("b'", "")
    e = e.replace("'", "")
    return e

def base64d(b):
    return str(base64.b64decode(b).decode('utf-8'))

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def checkTrait(text):
    c = text[-1:]
    if int((ord(c) - 0xAC00) % 28) != 0:
        return "을"
    else:
        return "를"
