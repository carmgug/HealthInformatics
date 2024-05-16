from flask import Flask, render_template, request

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

# Create a get request for the form, that have as input a string
# and a list of strings.



data = []
patient=[]
@app.route('/getExamByFiscalCode', methods=['GET'])
def getExamByFiscalCode():
    #take the fiscal code from the input
    fiscalCode = request.args.get('fiscalCode')
    #take the list of exams from the input
    exams, patientInfo = databaseImplementation.getExamByFiscalCode(fiscalCode)
    #return the list of exams

    data=exams
    patient=patientInfo
    return render_template('TemplateProva.html', data=data,patient=patient)


@app.route('/getExamByFiscalCodeAndTestName', methods=['GET'])
def getExamByFiscalCodeAndTestName():
    fiscalCode = request.args.get('fiscalCode')
    examsType = request.args.get('examsType')
    if(examsType=="ALL"):
        exams, patientInfo = databaseImplementation.getExamByFiscalCode(fiscalCode)
        data=exams
        patient=patientInfo
        return render_template('TemplateProva.html', data=data,patient=patient)
    #take the list of exams from the input
    exams, patientInfo = databaseImplementation.getExamByFiscalCodeAndTestName(fiscalCode,examsType)
    #return the list of exams
    data=exams
    patient=patientInfo
    return render_template('TemplateProva.html', data=data,patient=patient)






if __name__ == '__main__':
    app.run(debug=True)