import requests
from requests.structures import CaseInsensitiveDict

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

def getCoordinates(zip_c):
    weather_url = 'https://api.weatherapi.com/v1/current.json'
    weather_query = {"q": zip_c}
    weather_headers = {
        'key': 'e7e5a0eed9044fbab81184925222907'
    }

    data = requests.get(weather_url, headers=weather_headers,
                                params=weather_query).json()
    coordinates = data['location']
    return [coordinates['lon'],coordinates['lat']]

def filter(sessionID):
    dictio = requests.get("https://api.endlessmedical.com/v1/dx/GetSuggestedSpecializations?SessionID="+\
                    sessionID+"&NumberOfResults=10").json()
    specializations = []
    for specialization in dictio['SuggestedSpecializations']:
        specializations.append(specialization[0])
    return specializations

def getCategories(specialization):
    categories = ""
    if "Cardiology" in specialization:
        categories += "healthcare.clinic_or_praxis.cardiology,"
    if "Pulmonology" in specialization:
        categories += "healthcare.clinic_or_praxis.pulmonology,"
    if "Radiology" in specialization:
        categories += "healthcare.clinic_or_praxis.radiology,"
    if "Allergology" in specialization:
        categories += "healthcare.clinic_or_praxis.allergology,"
    if 'Gastroenterology' in specialization:
        categories += "healthcare.clinic_or_praxis.gastroenterology,"
    if "General" in specialization:
        categories += "healthcare.clinic_or_praxis.general,"
    categories += "healthcare.hospital"

    return categories


    

def suggestHospital(coordinates,category):

    dist = 10*1609.344
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    main_url = "https://api.geoapify.com/v2/places?"
    category_url = "categories="+category
    coord_url = "&filter=circle:" + str(coordinates[0]) + \
                "," + str(coordinates[1]) + "," + str(dist)
    limit_url = "&limit="+str(5)
    api_key = "&apiKey=a81ef38a8fdb430c9ff29347d1ed7825"
    url = main_url+category_url+coord_url+limit_url+api_key
    resp = requests.get(url,headers)
    places = resp.json()["features"]
    hospitals = []

    for place in places:
        detail = place["properties"]
        try:
            name = detail["name"]
            address = detail["address_line1"] + " " + detail["address_line2"]
        except Exception:
            name = detail["street"]
            address = detail["address_line1"] + " " + detail["address_line2"]

        hospital = {'name': name, 'address': address}
        hospitals.append(hospital)
        
    return hospitals

if __name__ == "__main__":
    #print(suggestHospital(getCoordinates(65201),"healthcare"))
    sessionID = getSessionId()
    addSymptoms(sessionID,"Temp","90")
    addSymptoms(sessionID,"Fasting","0")
    addSymptoms(sessionID,"Constipation","0")
    #addSymptoms(sessionID,"Vomiting","0")
    #addSymptoms(sessionID,"HeartBurn","0")
    #addSymptoms(sessionID,"AbdCramps","0")
    #addSymptoms(sessionID,"Nausea","0")
    #print(getDiseases(Analyze(sessionID)))
    filter = filter(sessionID)
    categories = getCategories(filter)
    print(filter,'\n',suggestHospital(getCoordinates(65201),categories))