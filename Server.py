from flask import Flask, render_template, request, jsonify
import requests

import Translator_HL7_to_JSON
#import databaseImplementation
import Translator_JSON_to_HL7
import databaseImplementation

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



data = []
patient = []


@app.route('/getExamByFiscalCode', methods=['GET'])
def getExamByFiscalCode():
    fiscalCode = request.args.get('fiscalCode')
    exams, patientInfo = databaseImplementation.getExamByFiscalCode(fiscalCode)
    data = exams
    patient = patientInfo
    return render_template('TemplateProva.html', data=data, patient=patient)


@app.route('/getExamByFiscalCodeAndTestName', methods=['GET'])
def getExamByFiscalCodeAndTestName():
    fiscalCode = request.args.get('fiscalCode')
    examsType = request.args.get('examsType')
    exams, patientInfo = databaseImplementation.getExamByFiscalCodeAndTestName(fiscalCode, examsType)
    data = exams
    patient = patientInfo
    return render_template('TemplateProva.html', data=data, patient=patient)


@app.route('/getExamByFiscalCodeAndDate', methods=['GET'])
def getExamByFiscalCodeAndDate():
    fiscalCode = request.args.get('fiscalCode')
    date = request.args.get('date')
    exams, patientInfo = databaseImplementation.getExamByFiscalCodeAndDate(fiscalCode, date)
    data = exams
    patient = patientInfo
    return render_template('TemplateProva.html', data=data, patient=patient)


@app.route('/getExamByFiscalCodeAndDateAndTestName', methods=['GET'])
def getExamByFiscalCodeAndDateAndTestName():
    fiscalCode = request.args.get('fiscalCode')
    examsType = request.args.get('examsType')
    date = request.args.get('examDate')
    if(date!=""):
        date = date.replace("-", "")


    if(examsType == "ALL" and date == ""):
        exams, patientInfo = databaseImplementation.getExamByFiscalCode(fiscalCode)
        data = exams
        patient = patientInfo
        return render_template('TemplateProva.html', data=data, patient=patient)
    elif(examsType == "ALL" and date!=""):
        exams, patientInfo = databaseImplementation.getExamByFiscalCodeAndDate(fiscalCode, date)
        data = exams
        patient = patientInfo
        return render_template('TemplateProva.html', data=data, patient=patient)
    elif(examsType != "ALL" and date==""):
        exams, patientInfo = databaseImplementation.getExamByFiscalCodeAndTestName(fiscalCode, examsType)
        data = exams
        patient = patientInfo
        return render_template('TemplateProva.html', data=data, patient=patient)

    exams, patientInfo = databaseImplementation.getExamByFiscalCodeAndDateAndTestName(fiscalCode, date,examsType)
    data = exams
    patient = patientInfo
    return render_template('TemplateProva.html', data=data, patient=patient)


@app.route('/send_to_cardiology', methods=['POST'])
def sendToCardiology():
    json = request.get_json()
    hl7 = Translator_JSON_to_HL7.translate_from_json_to_hl7(json)
    # Create a json object with hl7 inside and then call post function
    # on the server
    jsonObject = {'hl7': hl7}
    response = requests.post('http://localhost:5000/send_hl7_message', json=jsonObject)
    return jsonify({'status': 'OK'}), 200



@app.route('/send_hl7_message', methods=['POST'])
def reciveFromEmergencyRoom():
    # the hl7 message from the emergency room
    hl7 = request.get_json()
    hl7 = hl7['hl7']
    #translate the hl7 message into a json
    json = Translator_HL7_to_JSON.translate_from_HL7_to_JSON(hl7)
    print(json)
    databaseImplementation.addNewExam(json)
    print("SALVATO")
    # return ok response
    # Return an "OK" status
    return jsonify({'status': 'OK'}), 200


if __name__ == '__main__':
    app.run(debug=True)
