import requests

def getSessionId():
    url = "https://api.endlessmedical.com/v1/dx/InitSession"
    sessionID = requests.get(url).json()['SessionID']
    confirm =  "I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and Endless Medical services. The Terms of Use are available on endlessmedical.com"
    requests.post("https://api.endlessmedical.com/v1/dx/AcceptTermsOfUse?SessionID="+sessionID+"&passphrase="+confirm)
    return sessionID

def Analyze():
    sessionID = getSessionId()
    requests.post("https://api.endlessmedical.com/v1/dx/UpdateFeature?SessionID="+sessionID+"&name=Temp&value=80")
    return requests.get("https://api.endlessmedical.com/v1/dx/Analyze?SessionID="+sessionID+"&NumberOfResults=5").json()
