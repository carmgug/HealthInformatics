from flask import Flask, render_template, request, jsonify
import requests

import Translator_HL7_to_JSON
#import databaseImplementation
import Translator_JSON_to_HL7

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/form_emergency_room')
def emergency_room():
    return render_template('FormPatient.html')


@app.route('/cardiology_home')
def cardiology_home():
    return render_template('TemplateProva.html')


# Create a get request for the form, that have as input a string
# and a list of strings.


data = []
patient = []


@app.route('/getExamByFiscalCode', methods=['GET'])
def getExamByFiscalCode():
    #take the fiscal code from the input
    fiscalCode = request.args.get('fiscalCode')
    #take the list of exams from the input
    exams, patientInfo = databaseImplementation.getExamByFiscalCode(fiscalCode)
    #return the list of exams

    data = exams
    patient = patientInfo
    return render_template('TemplateProva.html', data=data, patient=patient)


@app.route('/getExamByFiscalCodeAndTestName', methods=['GET'])
def getExamByFiscalCodeAndTestName():
    fiscalCode = request.args.get('fiscalCode')
    examsType = request.args.get('examsType')
    if (examsType == "ALL"):
        exams, patientInfo = databaseImplementation.getExamByFiscalCode(fiscalCode)
        data = exams
        patient = patientInfo
        return render_template('TemplateProva.html', data=data, patient=patient)
    #take the list of exams from the input
    exams, patientInfo = databaseImplementation.getExamByFiscalCodeAndTestName(fiscalCode, examsType)
    #return the list of exams
    data = exams
    patient = patientInfo
    return render_template('TemplateProva.html', data=data, patient=patient)


@app.route('/send_to_cardiology', methods=['POST'])
def sendToCardiology():
    #take the json from the input
    json = request.get_json()
    #translate the json into a hl7 message
    hl7 = Translator_JSON_to_HL7.translate_from_json_to_hl7(json)
    #send the hl7 message to the cardiology department
    #Simulate the sending of the message
    # Create a json object with hl7 inside and then call post function
    # on the server
    jsonObject = {'hl7': hl7}
    response = requests.post('http://localhost:5000/send_hl7_message', json=jsonObject)
    return jsonify({'status': 'OK'}), 200



@app.route('/send_hl7_message', methods=['POST'])
def reciveFromEmergencyRoom():
    #receive the hl7 message from the emergency room
    #take the hl7 message from the input
    hl7 = request.get_json()
    hl7 = hl7['hl7']
    #translate the hl7 message into a json
    json = Translator_HL7_to_JSON.translate_from_HL7_to_JSON(hl7)
    #store the json in the database
    #databaseImplementation.addNewExam(json)
    print(json)
    print("SALVATO")
    # return ok response
    # Return an "OK" status
    return jsonify({'status': 'OK'}), 200


if __name__ == '__main__':
    app.run(debug=True)
