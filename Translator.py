import hl7
from datetime import datetime

'''
Message structure:
{
    "patient":{
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
    }
    
    "operator":{
        "id": "123456"
        
    }
    
    "orders":[
        {
        "placerOrderNumber": "123456",
        "testName": "UREA AND ELECTROLYTES",
        "potassiumValue": "4.5",
        "potassiumUnit": "MMOLL",
        "potassiumReferenceRange": "3.5-5.3",   
        "sodiumValue": hl7_message[5][5],
        "sodiumUnit": hl7_message[5][6],
        "sodiumReferenceRange": hl7_message[5][7],
        "ureaValue": hl7_message[6][5],
        "ureaUnit": hl7_message[6][6],
        "ureaReferenceRange": hl7_message[6][7] 
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
'''

SENDING_APPLICATION = "EMERGENCY_ROOM_FORUM"
SENDING_FACILITY = "EMERGENCY_ROOM"
RECEIVING_APPLICATION = "CARDIOLOGY_DEPARTMENT_MANAGEMENT"
RECEIVING_FACILITY = "CARDIOLOGY_DEPARTMENT"
# An A15 event notifies other systems of a plan to transfer a patient to a new location when the patient has not yet
# left the old location. It is used when advanced notification of a transfer is required in order to prepare for the
# patient’s location change. For example, this transaction could be sent so that staff will be on hand to move the
# patient or so that dietary services can route the next meal to the new location.
TRIGGER_EVENT = "ADT^A15"
ACCEPT_ACK_TYPE = "AL"
IDENTIFIER_TYPE = "MA"


def generate_message_id(time):
    secret_code = "001"
    hashcode = (secret_code + time + RECEIVING_APPLICATION).__hash__()
    message_id = f"{SENDING_APPLICATION}_{hashcode}"
    return message_id


def translate_from_json_to_hl7(jsonObject):
    # Create a new HL7 message

    curr_time_tmp = datetime.now()
    curr_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
    # Create the MSH segment
    message_hl7 = f"MSH|^~\&|{SENDING_APPLICATION}|{SENDING_FACILITY}|{RECEIVING_APPLICATION}|{RECEIVING_FACILITY}|{curr_time_str}||{TRIGGER_EVENT}|{generate_message_id(curr_time_str)}|P|2.5|||{ACCEPT_ACK_TYPE}\r"
    # Create the EVN segment (The EVN segment is used to communicate necessary trigger event information to receiving
    # applications.)
    message_hl7 += f"EVN|A15|{curr_time_str}|||{jsonObject['operator']['id']}\r"
    # Create the PID segment (The PID segment contains patient identification information.) As identifier, we use the
    # fiscal code and so the identifier type is set to "MA" (Patient Medicaid number: CLASS INSURANCE)
    message_hl7 += generate_pid_row(jsonObject)
    # Adding the OBR and OBX segments for the urine test (results)
    message_hl7 += generate_obr_row_urine_test(jsonObject, curr_time_tmp)
    message_hl7 += generate_obx_row_urine_test(jsonObject, curr_time_tmp)
    # Adding the OBR and OBX segments for the blood test (results)
    message_hl7 += generate_obr_row_blood_test(jsonObject, curr_time_tmp)
    message_hl7 += generate_obx_row_blood_test(jsonObject, curr_time_tmp)
    # Adding the NTE segment (The NTE segment contains narrative text information)
    message_hl7 += "NTE|1||This is a test message for the Emergency Room Forum.\r"

    return hl7.parse(message_hl7)

    # Set the message type


def generate_pid_row(jsonObject):
    # Create the PID segment (The PID segment contains patient identification information.) As identifier, we use the
    # fiscal code and so the identifier type is set to "MA" (Patient Medicaid number: CLASS INSURANCE)
    pid_row = "PID|1|"
    # 1. Column 2: Patient ID (Internal Identifier)
    pid_row += f"{jsonObject['patient']['fiscalCode']}^^^^{IDENTIFIER_TYPE}|"
    # 2. Column 3: Patient Identifier List (empty)
    pid_row += "|"
    # 2. Column 4: Alternate Patient ID (External Identifier) (empty)
    pid_row += "|"
    # 3. Column 5: Patient Name
    pid_row += f"{jsonObject['patient']['familyName']}^{jsonObject['patient']['name']}|"
    # 4. Column 6: Mother's Maiden Name (empty)
    pid_row += "|"
    # 5. Column 7: Date/Time of Birth
    pid_row += f"{jsonObject['patient']['birthDate']}|"
    # 6. Column 8: Administrative sex
    pid_row += f"{jsonObject['patient']['sex']}|"
    # 7. Column 9: Patient Alias (empty)
    pid_row += "|"
    # 8. Column 10: Race (empty)
    pid_row += "|"
    # 9. Column 11: Patient Address
    type_of_address = "L"  # L = Legal Address
    pid_row += (f"{jsonObject['patient']['streetAddress']}^^{jsonObject['patient']['city']}^"
                f"{jsonObject['patient']['province']}^{jsonObject['patient']['postalCode']}^"
                f"{jsonObject['patient']['countryCode']}^{type_of_address}|")
    # 10. Column 12: County Code (empty) #ALREADY INCLUDED IN THE ADDRESS
    pid_row += "|"
    # 11. Column 13: Phone Number
    pid_row += f"{jsonObject['patient']['phone']}|"
    # 12. Column 14: Business Phone Number (empty)
    pid_row += "|"
    # 13. Column 15: Primary Language
    pid_row += f"{jsonObject['patient']['language']}|"
    # 14. Column 16: Marital Status (empty)
    pid_row += "|"
    # 15. Column 17: Religion (empty)
    pid_row += "|"
    # 16. Column 18: Patient Account Number (empty)
    pid_row += "|"
    pid_row += "\r"
    return pid_row


def generate_obr_row_urine_test(jsonObject, curr_time):
    # Create the OBR segment (The OBR segment contains the details of the order placed by the requesting system.)
    obr_row = "OBR|1|"
    # 1. Column 2: Placer Order Number (it receives its value from the JSON object)
    obr_row += f"{jsonObject['orders'][0]['placerOrderNumber']}|"
    # 2. Column 3: Filler Order Number made by (Fiscal ID of the patient + name of the test + timestamp) hashed
    #curr_time = datetime.now()
    fiscal_code = jsonObject['patient']['fiscalCode']
    test_name = jsonObject['orders'][0]['testName']
    filler_order_number = f"{fiscal_code}_{test_name}_{curr_time}".__hash__()
    obr_row += f"{filler_order_number}|"
    # 3. Column 4: Service Identifier
    service_identifier = "25167001"  # SNOMED universal Service Identifier for the urea and electrolytes test
    # The Service Identifier could be a local identifier but we chose to use the universal SNOMED ID
    obr_row += f"{service_identifier}^{jsonObject['orders'][0]['testName']}^^^|"
    # 4. Column 5: Priority (empty)
    obr_row += "|"
    # 5. Column 6: Requested Date/Time
    obr_row += f"{curr_time}|"
    # 6. Column 7: Observation Date/Time
    obr_row += f"{curr_time}|"
    obr_row += "\r"

    return obr_row


def generate_obx_row_urine_test(jsonObject, current_time):
    # Create the OBX segment (The OBX segment contains the observation details.)
    # Three rows are needed for the urine test
    # First row: Potassium
    obx_row = "OBX|"
    # 1. Column 1: Sequence Number
    obx_row += "1|"
    # 2. Column 2: type of observation
    obx_row += "NM|"
    # 3. Column 3: Potassium Observation Identifier
    obx_row += "88480006^Potassium^^^|"  # SNOMED universal code for Potassium
    # 4. Column 4: Potassium Observation SubID (empty)
    obx_row += "|"
    # 5. Column 5: Potassium Observation Value (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['potassiumValue']}|"
    # 6. Column 6: Potassium Observation Unit (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['potassiumUnit']}|"
    # 7. Column 7: Reference Range (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['potassiumReferenceRange']}|"
    # 8. Column 8: Abnormal Flags (empty)
    obx_row += "|"  #TO-DO: Add the abnormal flags
    # 9. Column 9: Probability (empty)
    obx_row += "|"
    # 10. Column 10: Nature of Abnormal Test (empty)
    obx_row += "|"
    # 11. Column 11: Observation Result Status
    obx_row += "F|"  # F = Final results
    # 12. Column 12: Effective Date of Reference Range (empty)
    obx_row += "|"
    # 13. Column 13: User Defined Access Checks (empty)
    obx_row += "|"
    # 14. Column 14: Date/Time of the Observation
    obx_row += f"{current_time}|"
    # 15. Column 15: Producer's ID (empty)
    obx_row += "|"
    obx_row += "\r"

    # Second row: Sodium  
    obx_row += "OBX|"
    # 1. Column 1: Sequence Number
    obx_row += "2|"
    # 2. Column 2: type of observation
    obx_row += "NM|"
    # 3. Column 3: Sodium Observation Identifier
    obx_row += "39972003^Sodium^^^|"  # SNOMED universal code for Sodium
    # 4. Column 4: Sodium Observation SubID (empty)
    obx_row += "|"
    # 5. Column 5: Sodium Observation Value (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['sodiumValue']}|"
    # 6. Column 6: Sodium Observation Unit (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['sodiumUnit']}|"
    # 7. Column 7: Reference Range (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['sodiumReferenceRange']}|"
    # 8. Column 8: Abnormal Flags (empty)
    obx_row += "|"  #TO-DO: Add the abnormal flags
    # 9. Column 9: Probability (empty)
    obx_row += "|"
    # 10. Column 10: Nature of Abnormal Test (empty)
    obx_row += "|"
    # 11. Column 11: Observation Result Status
    obx_row += "F|"  # F = Final results
    # 12. Column 12: Effective Date of Reference Range (empty)
    obx_row += "|"
    # 13. Column 13: User Defined Access Checks (empty)
    obx_row += "|"
    # 14. Column 14: Date/Time of the Observation
    obx_row += f"{current_time}|"
    # 15. Column 15: Producer's ID (empty)
    obx_row += "|"
    obx_row += "\r"

    # Third row: Urea
    obx_row += "OBX|"
    # 1. Column 1: Sequence Number
    obx_row += "3|"
    # 2. Column 2: type of observation
    obx_row += "NM|"
    # 3. Column 3: Urea Observation Identifier
    obx_row += "387092000^Urea^^^|"  # SNOMED universal code for Urea
    # 4. Column 4: Urea Observation SubID (empty)
    obx_row += "|"
    # 5. Column 5: Urea Observation Value (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['ureaValue']}|"
    # 6. Column 6: Urea Observation Unit (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['ureaUnit']}|"
    # 7. Column 7: Reference Range (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][0]['ureaReferenceRange']}|"
    # 8. Column 8: Abnormal Flags (empty)
    obx_row += "|"  #TO-DO: Add the abnormal flags
    # 9. Column 9: Probability (empty)
    obx_row += "|"
    # 10. Column 10: Nature of Abnormal Test (empty)
    obx_row += "|"  #TO-DO: Add the abnormal flags
    # 11. Column 11: Observation Result Status
    obx_row += "F|"  # F = Final results
    # 12. Column 12: Effective Date of Reference Range (empty)
    obx_row += "|"
    # 13. Column 13: User Defined Access Checks (empty)
    obx_row += "|"
    # 14. Column 14: Date/Time of the Observation
    obx_row += f"{current_time}|"
    # 15. Column 15: Producer's ID (empty)
    obx_row += "|"
    obx_row += "\r"

    return obx_row


def generate_obr_row_blood_test(jsonObject, curr_time):
    # Create the OBR segment (The OBR segment contains the details of the order placed by the requesting system.)
    obr_row = "OBR|1|"
    # 1. Column 2: Placer Order Number (it receives its value from the JSON object)
    obr_row += f"{jsonObject['orders'][1]['placerOrderNumber']}|"
    # 2. Column 3: Filler Order Number made by (Fiscal ID of the patient + name of the test + timestamp) hashed
    #curr_time = datetime.now()
    fiscal_code = jsonObject['patient']['fiscalCode']
    test_name = jsonObject['orders'][1]['testName']
    filler_order_number = f"{fiscal_code}_{test_name}_{curr_time}".__hash__()
    obr_row += f"{filler_order_number}|"
    # 3. Column 4: Service Identifier
    service_identifier = "75367002"  # SNOMED universal Service Identifier for the blood test
    # https://www.findacode.com/snomed/75367002--blood-pressure.html
    # The Service Identifier could be a local identifier but we chose to use the universal SNOMED ID
    obr_row += f"{service_identifier}^{jsonObject['orders'][1]['testName']}^^^|"
    # 4. Column 5: Priority (empty)
    obr_row += "|"
    # 5. Column 6: Requested Date/Time
    obr_row += f"{curr_time}|"
    # 6. Column 7: Observation Date/Time
    obr_row += f"{curr_time}|"
    obr_row += "\r"

    return obr_row


def generate_obx_row_blood_test(jsonObject, current_time):
    # Create the OBX segment (The OBX segment contains the observation details.)
    # Three rows are needed for the blood test
    # First row: Systolic Blood Pressure
    obx_row = "OBX|"
    # 1. Column 1: Sequence Number
    obx_row += "1|"
    # 2. Column 2: type of observation
    obx_row += "NM|"
    # 3. Column 3: Systolic Blood Pressure Observation Identifier
    obx_row += "271649006^Systolic Blood Pressure^^^|"  # SNOMED universal code for Systolic Blood Pressure
    #https://www.findacode.com/snomed/271649006--systolic-blood-pressure.html
    # 4. Column 4: Systolic Blood Pressure Observation SubID (empty)
    obx_row += "|"
    # 5. Column 5: Systolic Blood Pressure Observation Value (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][1]['systolicBloodPressureValue']}|"
    # 6. Column 6: Systolic Blood Pressure Observation Unit (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][1]['systolicBloodPressureUnit']}|"
    # 7. Column 7: Reference Range (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][1]['systolicBloodPressureReferenceRange']}|"
    # 8. Column 8: Abnormal Flags (empty)
    obx_row += "|"  #TO-DO: Add the abnormal flags
    # 9. Column 9: Probability (empty)
    obx_row += "|"
    # 10. Column 10: Nature of Abnormal Test (empty)
    obx_row += "|"
    # 11. Column 11: Observation Result Status
    obx_row += "F|"  # F = Final results
    # 12. Column 12: Effective Date of Reference Range (empty)
    obx_row += "|"
    # 13. Column 13: User Defined Access Checks (empty)
    obx_row += "|"
    # 14. Column 14: Date/Time of the Observation
    obx_row += f"{current_time}|"
    # 15. Column 15: Producer's ID (empty)
    obx_row += "|"
    obx_row += "\r"

    # Second row: Diastolic Blood Pressure
    obx_row += "OBX|"
    # 1. Column 1: Sequence Number
    obx_row += "2|"
    # 2. Column 2: type of observation
    obx_row += "NM|"
    # 3. Column 3: Diastolic Blood Pressure Observation Identifier
    obx_row += "271650006^Diastolic Blood Pressure^^^|"  # SNOMED universal code for Diastolic Blood Pressure
    #https://www.findacode.com/snomed/271650006--diastolic-blood-pressure.html
    # 4. Column 4: Diastolic Blood Pressure Observation SubID (empty)
    obx_row += "|"
    # 5. Column 5: Diastolic Blood Pressure Observation Value (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][1]['diastolicBloodPressureValue']}|"
    # 6. Column 6: Diastolic Blood Pressure Observation Unit (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][1]['diastolicBloodPressureUnit']}|"
    # 7. Column 7: Reference Range (it receives its value from the JSON object)
    obx_row += f"{jsonObject['orders'][1]['diastolicBloodPressureReferenceRange']}|"
    # 8. Column 8: Abnormal Flags (empty)
    obx_row += "|"  #TO-DO: Add the abnormal flags
    # 9. Column 9: Probability (empty)
    obx_row += "|"
    # 10. Column 10: Nature of Abnormal Test (empty)
    obx_row += "|"
    # 11. Column 11: Observation Result Status
    obx_row += "F|"  # F = Final results
    # 12. Column 12: Effective Date of Reference Range (empty)
    obx_row += "|"
    # 13. Column 13: User Defined Access Checks (empty)
    obx_row += "|"
    # 14. Column 14: Date/Time of the Observation
    obx_row += f"{current_time}|"
    # 15. Column 15: Producer's ID (empty)
    obx_row += "|"
    obx_row += "\r"

    return obx_row


def __main__():
    # Example of a JSON object
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
        "note": "NOTE PAZIENTE",
        "orders": [
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
    # Translate the JSON object to an HL7 message
    message = translate_from_json_to_hl7(jsonObject)
    print(jsonObject)
    print(message[0])
    print(message[1])
    print(message[2])
    print(message[3])
    print(message[4])
    print(message[5])
    print(message[6])
    print(message[7])
    print(message[8])
    print(message[9])
    print(message[10])


__main__()
