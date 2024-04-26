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
    curr_time = datetime.now().strftime("%Y%m%d%H%M%S")
    # Create the MSH segment
    message_hl7 = f"MSH|^~\&|{SENDING_APPLICATION}|{SENDING_FACILITY}|{RECEIVING_APPLICATION}|{RECEIVING_FACILITY}|{curr_time}||{TRIGGER_EVENT}|{generate_message_id(curr_time)}|P|2.5|||{ACCEPT_ACK_TYPE}\r"
    # Create the EVN segment (The EVN segment is used to communicate necessary trigger event information to receiving
    # applications.)
    message_hl7 += f"EVN|A15|{curr_time}|||{jsonObject['operator']['id']}\r"
    # Create the PID segment (The PID segment contains patient identification information.) As identifier, we use the
    # fiscal code and so the identifier type is set to "MA" (Patient Medicaid number: CLASS INSURANCE)
    message_hl7 += generate_pid_row(jsonObject)
    # Create the PV1 segment (The PV1 segment contains information about the patient’s visit.)

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
    return pid_row


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
        }
    }
    # Translate the JSON object to an HL7 message
    message = translate_from_json_to_hl7(jsonObject)
    print(jsonObject)
    print(message[0])
    print(message[1])
    print(message[2])

__main__()
