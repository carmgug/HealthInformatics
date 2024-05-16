import hl7
from datetime import datetime
import Translator_JSON_to_HL7

def translate_from_HL7_to_JSON(hl7_message):
    
    json_object = {}
    
    patientID = hl7_message[2][2][0][0]
    patientName = hl7_message[2][5][0][1]
    patientSurname = hl7_message[2][5][0][0]
    patientGender = hl7_message[2][8]
    patientBirthDate = hl7_message[2][7]
    patientAddress = hl7_message[2][11][0][0]
    patientCity = hl7_message[2][11][0][2]
    patientProvince = hl7_message[2][11][0][3]
    patientPostalCode = hl7_message[2][11][0][4]
    patientCountryCode = hl7_message[2][11][0][5]
    patientPhoneNumber = hl7_message[2][13]
    patientLanguage = hl7_message[2][15]
    
    patient = {
        "patientID": patientID[0],
        "patientName": patientName[0],
        "patientSurname": patientSurname[0],
        "patientGender": patientGender[0],
        "patientBirthDate": patientBirthDate[0],
        "patientAddress": patientAddress[0],
        "patientCity": patientCity[0],
        "patientProvince": patientProvince[0],
        "patientPostalCode": patientPostalCode[0],
        "patientCountryCode": patientCountryCode[0],
        "patientPhoneNumber": patientPhoneNumber[0],
        "patientLanguage": patientLanguage[0]
    }
    
    operatorID = hl7_message[1][5]
    #timestamp = datetime.strptime(str(hl7_message[1][2][0]), "%Y%m%d%H%M%S")
    operator = {
        "operatorID": operatorID[0],
        "timestamp": str(hl7_message[1][2][0])
    }
    
    orders = [
        {
            "placerOrderNumber": hl7_message[3][2][0],
            "fillerOrderNumber": hl7_message[3][3][0],
            "testName": hl7_message[3][4][0][1][0],
            "potassiumValue": hl7_message[4][5][0],
            "potassiumUnit": hl7_message[4][6][0],
            "potassiumReferenceRange": hl7_message[4][7][0],
            "sodiumValue": hl7_message[5][5][0],
            "sodiumUnit": hl7_message[5][6][0],
            "sodiumReferenceRange": hl7_message[5][7][0],
            "ureaValue": hl7_message[6][5][0],
            "ureaUnit": hl7_message[6][6][0],
            "ureaReferenceRange": hl7_message[6][7][0]
        },
        {
            "placerOrderNumber": hl7_message[7][2][0],
            "fillerOrderNumber": hl7_message[7][3][0],
            "testName": hl7_message[7][4][0][1][0],
            "systolicBloodPressureValue": hl7_message[8][5][0],
            "systolicBloodPressureUnit": hl7_message[8][6][0],
            "systolicBloodPressureReferenceRange": hl7_message[8][7][0],
            "diastolicBloodPressureValue": hl7_message[9][5][0],
            "diastolicBloodPressureUnit": hl7_message[9][6][0],
            "diastolicBloodPressureReferenceRange": hl7_message[9][7][0]
        }
    ]

    note = hl7_message[10][3]
    
    json_object['patient'] = patient
    json_object['operator'] = operator
    json_object['orders'] = orders
    json_object['note'] = note[0]
        
    return json_object

jsonObject = {
        "patient": {
            "fiscalCode": "GGLCML80A01H501S",
            "name": "John",
            "familyName": "Doe",
            "sex": "M",
            "birthDate": "19800101",
            "streetAddress": "Via Roma 1",
            "city": "Roma",
            "province": "RM",
            "postalCode": "00100",
            "country": "Italia",
            "countryCode": "ITA",
            "phone": "1234567890",
            "language": "Italian"
        },
        "operator": {
            "id": "123456"
        },
        "orders":[
            {
            "placerOrderNumber": "123456",
            "testName": "UREA AND ELECTROLYTES",
            "potassiumValue": "4.5",
            "potassiumUnit": "MMOLL",
            "potassiumReferenceRange": "3.5-5.3",
            "sodiumValue": "145.01",
            "sodiumUnit": "MMOLL",
            "sodiumReferenceRange": "133-146",
            "ureaValue": "5.45",
            "ureaUnit": "MMOLL",
            "ureaReferenceRange": "2.5-7.8",
            },
            {
            "placerOrderNumber": "123457",
            "testName": "BLOOD PRESSURE",
            "systolicBloodPressureValue": "120",
            "systolicBloodPressureUnit": "MMHG",
            "systolicBloodPressureReferenceRange": "90-120",
            "diastolicBloodPressureValue": "80",
            "diastolicBloodPressureUnit": "MMHG",
            "diastolicBloodPressureReferenceRange": "60-80",
            }
        ]
    
    }

def __main__():
    hl7_message = Translator_JSON_to_HL7.translate_from_json_to_hl7(jsonObject)
    json_object = translate_from_HL7_to_JSON(hl7_message)
    print(json_object)
