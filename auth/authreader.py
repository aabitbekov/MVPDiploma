

def getUsername():
    with open('auth/auth.txt') as f:
        lines = str(f.read())
        lines = lines.split(',')
    return  lines

def getPass():
    with open('auth/pass.txt') as f:
        lines = str(f.read())
        lines = lines.split(',')
    return  lines

def getNames():
    with open('auth/names.txt') as f:
        lines = str(f.read())
        lines = lines.split(',')
    return  lines