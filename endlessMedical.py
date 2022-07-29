import requests

def getSessionId():
    """Get the session and confirmation to use the EndlessMedical API"""
    url = "https://api.endlessmedical.com/v1/dx/InitSession"
    sessionID = requests.get(url).json()['SessionID']
    confirm =  "I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and Endless Medical services. The Terms of Use are available on endlessmedical.com"
    requests.post("https://api.endlessmedical.com/v1/dx/AcceptTermsOfUse?SessionID="+sessionID+"&passphrase="+confirm)
    return sessionID

def addSymptoms(sessionID,name,value):
    """Create the symptoms string"""
    requests.post("https://api.endlessmedical.com/v1/dx/UpdateFeature?SessionID="+sessionID+"&name="+name+"&value="+value)
    


def Analyze(sessionID):
    """Analyze and return the possible disease"""
    return requests.get("https://api.endlessmedical.com/v1/dx/Analyze?SessionID="+sessionID+"&NumberOfResults=5").json()

if __name__ == "__main__":
    sessionID = getSessionId()
    addSymptoms(sessionID,"Temp","90")
    addSymptoms(sessionID,"Fasting","0")
    addSymptoms(sessionID,"Constipation","0")
    addSymptoms(sessionID,"Vomiting","0")
    addSymptoms(sessionID,"HeartBurn","0")
    addSymptoms(sessionID,"AbdCramps","0")
    addSymptoms(sessionID,"Nausea","0")
    print(Analyze(sessionID))