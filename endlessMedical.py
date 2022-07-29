import requests

yn_questions = {"AbdCramps":"Abdominal cramps","Chills": "Chills","ChestPainAnginaYesNo":"Chest Pain", "Conjunctivas":"Conjunctivas",\
                "DecreasedMood":"Decreased Mood",\
                "Constipation":"Constipation","EatingPain":"Eating Pain","GeneralizedFatigue":"Fatigue",\
                "HeadacheFrontal":"Headahce","ResistantHypertension":"Hypertension","HypoTension":"HypoTension",\
                "EyesItchy":"Itching eyes","Nocturia":"Nocturia","Nausea":"Nausea", "NoseCongestion": "Nose congestion",\
                "LossOfSmell":"Loss of smell","LossOfTaste":"Loss of taste","LossOfConsciousness":"Loss of consciousness",\
                 "LowbackPain":"Low back pain","Seizure":"Seizure","Snoring":"Snoring","Sneezing":"Sneezing",\
                "SwallowPain":"Pain when swallowing","Vomiting":"Vomiting","WeightLoss":"Weight loss","Weight gain":"Weight gain"}

num_questions = {"Temp":"Temperature"}

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

def getDiseases(data):
    """Extract all diseases of the analyze and store them in an array"""
    dictio = data["Diseases"]
    diseases = []
    for disease in dictio:
        diseases.append(*disease)
    return diseases

if __name__ == "__main__":
    sessionID = getSessionId()
    addSymptoms(sessionID,"Temp","90")
    addSymptoms(sessionID,"Fasting","0")
    addSymptoms(sessionID,"Constipation","0")
    addSymptoms(sessionID,"Vomiting","0")
    addSymptoms(sessionID,"HeartBurn","0")
    addSymptoms(sessionID,"AbdCramps","0")
    addSymptoms(sessionID,"Nausea","0")
    print(getDiseases(Analyze(sessionID)))