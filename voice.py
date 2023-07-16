import os

def noting(filename,content):
    filename += ".txt"
    filepath = "voice_notes/"+filename
    try:
        with open(filepath, "w") as file:
            file.write(content)
            return 1
    except FileNotFoundError:
        return 2
    except IOError:
        return 0

def delete(filename):
    filename += ".txt"
    filepath = "voice_notes/"+filename
    try:
        os.remove(filepath)
        return 1
    except OSError:
        return 0

def recite(filename):
    filename += ".txt"
    filepath = "voice_notes/"+filename
    try:
        with open(filepath, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return 2
    except IOError:
        return 0


