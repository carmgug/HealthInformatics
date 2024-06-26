'''
To run this code:
    1-Install dockerDesktop installable at the link:https://docs.docker.com/engine/install/
    2-Open Docker and execute in the cmd the command: docker run --rm -t -i -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password couchdb:3.3.3
    3-Execute the code
'''

import datetime
import random
import CouchDBClient
import random
from datetime import datetime, timedelta
import json

client = CouchDBClient.CouchDBClient()
client.reset()

#Different 3 database are created
client.createDatabase('patient')
client.createDatabase('operator')
client.createDatabase('exam')

print("Database List", client.listDatabases())

nomi_maschili = [
    "Luca", "Marco", "Andrea", "Giuseppe", "Mario", "Antonio", "Francesco", "Giovanni",
    "Roberto", "Stefano", "Alessandro", "Davide", "Simone", "Fabio", "Riccardo", "Paolo",
    "Michele", "Leonardo", "Gianluca", "Daniele", "Luigi", "Enrico", "Claudio", "Filippo",
    "Emanuele", "Salvatore", "Lorenzo", "Vincenzo", "Massimo", "Federico"
]

nomi_femminili = [
    "Maria", "Laura", "Giulia", "Anna", "Sara", "Alessia", "Martina", "Elena",
    "Francesca", "Roberta", "Valentina", "Jessica", "Elisa", "Silvia", "Chiara", "Daniela",
    "Cristina", "Serena", "Veronica", "Sabrina", "Simona", "Eleonora", "Michela", "Angela",
    "Monica", "Giorgia", "Patrizia", "Cinzia", "Lucia", "Federica"
]

cognomi_italiani = [
    "Rossi", "Bianchi", "Russo", "Ferrari", "Esposito", "Romano", "Ricci", "Marino",
    "Greco", "Bruno", "De Luca", "Moretti", "Conti", "Costa", "Giordano", "Mancini",
    "Lombardi", "Barone", "Pellegrini", "Vitale", "Marchetti", "Rinaldi", "Gentile",
    "Silvestri", "Palumbo", "Sanna", "Parisi", "Caruso", "De Santis", "Ferri"
]

nomi = {
    "M": nomi_maschili,
    "F": nomi_femminili
}

sesso = ["M", "F"]

citta_italiane = [
    "Roma", "Milano", "Napoli", "Torino", "Palermo", "Genova", "Bologna", "Firenze",
    "Bari", "Catania", "Venezia", "Verona", "Messina", "Padova", "Trieste"
]

citta_codici_provincia = {
    "Roma": "RM", "Milano": "MI", "Napoli": "NA", "Torino": "TO", "Palermo": "PA", "Genova": "GE", "Bologna": "BO",
    "Firenze": "FI", "Bari": "BA", "Catania": "CT", "Venezia": "VE", "Verona": "VR", "Messina": "ME", "Padova": "PD",
    "Trieste": "TS"}

citta_codici_postali = {
    "Roma": "00100", "Milano": "20100", "Napoli": "80100", "Torino": "10100", "Palermo": "90100", "Genova": "16100",
    "Bologna": "40100",
    "Firenze": "50100", "Bari": "70100", "Catania": "95100", "Venezia": "30100", "Verona": "37100", "Messina": "98100",
    "Padova": "35100", "Trieste": "34100"
}


def genera_numero_telefonico():
    prefissi = ["02", "06", "08", "09"]
    prefisso = random.choice(prefissi)
    resto_numero = ''.join(random.choices('0123456789', k=8))
    return f"{prefisso}{resto_numero}"


nomi_vie = [
    "Roma", "Trieste", "Firenze", "Milano", "Napoli", "Genova", "Bologna",
    "Torino", "Palermo", "Bari", "Venezia", "Verona", "Catania", "Padova",
    "Messina", "Brescia", "Taranto", "Parma", "Reggio", "Modena", "Prato",
    "Livorno", "Ravenna", "Cosenza", "Piacenza", "Lucca", "Como", "Udine",
    "Trento", "Varese"
]

note = [
    "Patient's urea levels are within normal range, indicating proper kidney function.",
    "Electrolyte levels are balanced, suggesting no underlying metabolic abnormalities.",
    "Urea levels slightly elevated, may indicate dehydration. Advised increased fluid intake.",
    "Potassium levels are low, suggesting possible renal issues. Recommend further investigation.",
    "Calcium levels are within normal limits, indicating proper bone and nerve function.",
    "Patient's blood pressure is elevated, indicating hypertension. Advised lifestyle modifications.",
    "Blood pressure readings are consistently high. Medication adjustment may be necessary.",
    "Systolic pressure is within normal range, but diastolic pressure is elevated. Monitor closely.",
    "Blood pressure readings fluctuate, recommend daily monitoring to identify patterns.",
    "Orthostatic hypotension observed, advise caution when changing positions to prevent falls.",
]



operators = [{'idOperator': 1, 'name': 'John', 'surname': 'Doe'},
             {'idOperator': 2, 'name': 'Jane', 'surname': 'Doe'},
             {'idOperator': 3, 'name': 'Alice', 'surname': 'Smith'},
             {'idOperator': 4, 'name': 'Bob', 'surname': 'Smith'},
             {'idOperator': 5, 'name': 'Charlie', 'surname': 'Brown'},
             {'idOperator': 6, 'name': 'Lucy', 'surname': 'Brown'}]


def calcola_codice_fiscale(nome, cognome, data_nascita, luogo_nascita, sesso):
    nome = nome.upper().replace(" ", "")
    cognome = cognome.upper().replace(" ", "")

    giorno, mese, anno = data_nascita.split("-")

    codice_comune = luogo_nascita[:4].upper()

    consonanti_cognome = "".join(filter(lambda x: x not in 'AEIOU', cognome))

    consonanti_nome = "".join(filter(lambda x: x not in 'AEIOU', nome))

    anno_di_nascita = anno[2:]

    mesi = 'ABCDEHLMPRST'
    mese_char = mesi[int(mese) - 1]

    giorno = int(giorno)
    if sesso == 'F':
        giorno += 40
    giorno_char = str(giorno)

    codice_fiscale = consonanti_cognome[:3] + consonanti_nome[
                                              :3] + anno_di_nascita + mese_char + giorno_char + codice_comune + sesso

    return codice_fiscale


formato_personalizzato_data = "%Y%m%d%H%M%S"


def genera_data_di_nascita_e_eta():
    anno_corrente = datetime.now().year
    anno_minimo = anno_corrente - 85
    anno_massimo = anno_corrente - 20

    anno_nascita = random.randint(anno_minimo, anno_massimo)
    mese_nascita = random.randint(1, 12)
    giorno_nascita = random.randint(1, 28)

    data_di_nascita = datetime(anno_nascita, mese_nascita, giorno_nascita)
    eta = anno_corrente - anno_nascita - ((datetime.now().month, datetime.now().day) < (mese_nascita, giorno_nascita))

    return data_di_nascita.strftime("%Y-%m-%d"), eta


def generaData(numPerson):
    ret = []
    numOrder = 0
    for i in range(numPerson):
        sessoRnd = random.choice(sesso)
        name = random.choice(nomi[sessoRnd])
        familyName = random.choice(cognomi_italiani)
        date, age = genera_data_di_nascita_e_eta()
        city = random.choice(citta_italiane)
        phone = genera_numero_telefonico()
        cf = calcola_codice_fiscale(name, familyName, date, city, sessoRnd)
        yersterdayDate = datetime.now() - timedelta(days=1)
        data = {
            "patient": {
                "fiscalCode": cf,
                "name": name,
                "familyName": familyName,
                "sex": sessoRnd,
                "birthDate": date,
                "streetAddress": "Via" + random.choice(nomi_vie),
                "city": city,
                "province": citta_codici_provincia[city],
                "postalCode": citta_codici_postali[city],
                "country": "Italia",
                "countryCode": "ITA",
                "phone": phone,
                "language": "Italian"
            },
            "note": note[random.randint(0, len(note) - 1)],

            "operator": {
                "idOperator": random.choice(range(1, len(operators) + 1)),
                "timestamp": yersterdayDate.strftime(formato_personalizzato_data)
            },
            "orders": [
                {
                    "fillerOrderNumber": numOrder,
                    "testName": "UREA AND ELECTROLYTES",
                    "potassiumValue": random.randint(35, 53) / 10,
                    "potassiumUnit": "MMOLL",
                    "potassiumReferenceRange": "3.5-5.3",
                    "sodiumValue": random.randint(133, 146),
                    "sodiumUnit": "MMOLL",
                    "sodiumReferenceRange": "133-146",
                    "ureaValue": round(random.uniform(2.5, 7.8),1),
                    "ureaUnit": "MMOLL",
                    "ureaReferenceRange": "2.5-7.8",
                },
                {
                    "fillerOrderNumber": numOrder + 1,
                    "testName": "BLOOD PRESSURE",
                    "systolicBloodPressureValue": random.randint(90, 120),
                    "systolicBloodPressureUnit": "MMHG",
                    "systolicBloodPressureReferenceRange": "90-120",
                    "diastolicBloodPressureValue": random.randint(60, 80),
                    "diastolicBloodPressureUnit": "MMHG",
                    "diastolicBloodPressureReferenceRange": "60-80",
                }
            ]
        }
        ret.append(data)
        numOrder += 2

    return ret


data = generaData(20)


#ADD DATA TO DATABASE

def addOperators(operators):
    for operator in operators:
        client.addDocument('operator', {
            'idOperator': operator['idOperator'],
            'name': operator['name'],
            'familyName': operator['surname'],
        })


def hasOperator(operatorId):
    for operator in client.listDocuments('operator'):
        doc = client.getDocument('operator', operator)
        if (doc['idOperator'] == operatorId):
            print(operator)
            return True
    return False


def hasPatient(patientId):
    for patient in client.listDocuments('patient'):
        doc = client.getDocument('patient', patient)
        if (doc['fiscalCode'] == patientId):
            print(patient)
            return True
    return False


def addPatient(dbClient, patientJsonInfo):
    dbClient.addDocument('patient', {
        '_id': dbClient._generateUuid(),
        'fiscalCode': patientJsonInfo['fiscalCode'],
        'name': patientJsonInfo['name'],
        'familyName': patientJsonInfo['familyName'],
        'sex': patientJsonInfo['sex'],
        'birthDate': patientJsonInfo['birthDate'],
        'streetAddress': patientJsonInfo['streetAddress'],
        'city': patientJsonInfo['city'],
        'province': patientJsonInfo['province'],
        'postalCode': patientJsonInfo['postalCode'],
        'country': patientJsonInfo['country'],
        'countryCode': patientJsonInfo['countryCode'],
        'language': patientJsonInfo['language']
    }
                         )

def addExam(dbClient, fiscalCode, operatorId, examInfo, time, note):
    if (examInfo['testName'] == "UREA AND ELECTROLYTES"):
        dbClient.addDocument('exam', {
            '_id': dbClient._generateUuid(),  # Usa un UUID per l'identificatore dell'esame
            'patientId': fiscalCode,  # Aggiungi l'identificatore fiscale del paziente
            'idOperator': int(operatorId),  # Aggiungi l'identificatore dell'operatore che ha effettuato l'ordine
            'fillerOrderNumber': examInfo['fillerOrderNumber'],
            'testName': examInfo['testName'],
            'potassiumValue': examInfo['potassiumValue'],
            'potassiumUnit': "MMOLL",
            "potassiumReferenceRange": "3.5-5.3",
            "sodiumValue" : examInfo['sodiumValue'],
            "sodiumUnit": "MMOLL",
            "sodiumReferenceRange":"133-146",
            "ureaValue":examInfo['ureaValue'] ,
            "ureaUnit": "MMOLL",
            "ureaReferenceRange": "2.5-7.8" ,
            'date': time[:8],  # Ottieni i primi 8 caratteri per la data
            'time': time[8:],  # Ottieni i caratteri dopo i primi 8 per l'ora
            'note': note
        })


    elif (examInfo['testName'] == "BLOOD PRESSURE"):
        dbClient.addDocument('exam', {
            'id': dbClient._generateUuid(),  # Usa un UUID per l'identificatore dell'esame
            'patientId': fiscalCode,  # Aggiungi l'identificatore fiscale del paziente
            'idOperator': int(operatorId),  # Aggiungi l'identificatore dell'operatore che ha effettuato l'ordine
            'testName': examInfo['testName'],
            'systolicBloodPressureValue': examInfo['systolicBloodPressureValue'],
            'systolicBloodPressureUnit': "MMHG",
            "systolicBloodPressureReferenceRange": "90-120",
            'diastolicBloodPressureValue': examInfo['diastolicBloodPressureValue'],
            'diastolicBloodPressureUnit': "MMHG",
            "diastolicBloodPressureReferenceRange": "60-80",
            'date': time[:8],  # Ottieni i primi 8 caratteri per la data
            'time': time[8:],  # Ottieni i caratteri dopo i primi 8 per l'ora
            'note': note
        })


def addNewExam(visit):
    # se l'operatore non esiste non esiste l'esame
    if (not hasOperator(int(visit['operator']['idOperator']))):
        print('Operator not found')
        return
    # se il paziente non esiste lo devo aggiungere 
    if (not hasPatient(visit['patient']['fiscalCode'])):
        addPatient(client, visit['patient'])
    # aggiungo l'esame
    for order in visit['orders']:
        addExam(client, visit['patient']['fiscalCode'], visit['operator']['idOperator'], order,
                visit['operator']['timestamp'], visit['note'])

    print("New exam added: ",visit)


def getExam():
    ret = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        ret.append(doc)

    return ret


def getAllFiscalCode():
    ret = []
    for cf in client.listDocuments('patient'):
        doc = client.getDocument('patient', cf)
        ret.append(doc['fiscalCode'])

    return ret


def getExamByFiscalCode(fiscalCode):
    ret = []
    patientData = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        if (doc['patientId'] == fiscalCode):
            ret.append(doc)

    for el in ret:
        for person in client.listDocuments('patient'):
            doc = client.getDocument('patient', person)
            if (el['patientId'] == doc['fiscalCode'] and not (doc in patientData)):
                patientData.append(doc)

    return ret, patientData


def getExamByFiscalCodeAndDate(fiscalCode, date):
    ret = []
    patientData = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        if (doc['patientId'] == fiscalCode and doc['date'] == date):
            ret.append(doc)

    for el in ret:
        for person in client.listDocuments('patient'):
            doc = client.getDocument('patient', person)
            if (el['patientId'] == doc['fiscalCode'] and not (doc in patientData)):
                patientData.append(doc)

    return ret, patientData


def getExamByTestName(testName):
    ret = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        if (doc['testName'] == testName):
            ret.append(doc)

    return ret


def getExamByFiscalCodeAndDateAndTestName(fiscalCode, date, testName):
    ret = []
    patientData = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        if (doc['patientId'] == fiscalCode and doc['date'] == date and doc['testName'] == testName):
            ret.append(doc)

    print(len(ret))

    for el in ret:
        for person in client.listDocuments('patient'):
            doc = client.getDocument('patient', person)
            if (el['patientId'] == doc['fiscalCode'] and not (doc in patientData)):
                patientData.append(doc)

    print(len(ret))

    return ret, patientData


# ritorna tutti gli esami di un operatore
def getExamByOperatorId(operatorId):
    ret = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        if (doc['idOperator'] == operatorId):
            ret.append(doc)

    return ret

'''
# ritorna tutti gli esami di un paziente
def getExamByFiscalCode(fiscalCode):
    ret = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        if (doc['patientId'] == fiscalCode):
            ret.append(doc)
    return ret
'''

# ritorna gli esami per data di esecuzione
def getExamByDate(date):
    ret = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        if (doc['date'] == date):
            ret.append(doc)

    return ret


def getExamByFiscalCodeAndTestName(fiscalCode, testName):
    ret = []
    patientData = []
    for exam in client.listDocuments('exam'):
        doc = client.getDocument('exam', exam)
        if (doc['patientId'] == fiscalCode and doc['testName'] == testName):
            ret.append(doc)

    for el in ret:
        for person in client.listDocuments('patient'):
            doc = client.getDocument('patient', person)
            if (el['patientId'] == doc['fiscalCode'] and not (doc in patientData)):
                patientData.append(doc)

    return ret, patientData


addOperators(operators)

for el in data:
    addNewExam(el)

print("---------GET ALL FISCAL CODE---------")

print(getAllFiscalCode())
