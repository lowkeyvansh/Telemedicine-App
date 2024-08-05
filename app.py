from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telemedicine.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    medical_history = db.Column(db.Text, nullable=True)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialty = db.Column(db.String(150), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    age = IntegerField('Age', validators=[DataRequired()])
    medical_history = TextAreaField('Medical History')
    submit = SubmitField('Add Patient')

class DoctorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    specialty = StringField('Specialty', validators=[DataRequired(), Length(min=2, max=150)])
    submit = SubmitField('Add Doctor')

class AppointmentForm(FlaskForm):
    patient_id = IntegerField('Patient ID', validators=[DataRequired()])
    doctor_id = IntegerField('Doctor ID', validators=[DataRequired()])
    appointment_date = DateTimeField('Appointment Date', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Book Appointment')

db.create_all()

@app.route('/')
def home():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    return render_template('index.html', patients=patients, doctors=doctors, appointments=appointments)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        new_patient = Patient(name=form.name.data, age=form.age.data, medical_history=form.medical_history.data)
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_patient.html', form=form)

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        new_doctor = Doctor(name=form.name.data, specialty=form.specialty.data)
        db.session.add(new_doctor)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_doctor.html', form=form)

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        new_appointment = Appointment(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            appointment_date=form.appointment_date.data,
            notes=form.notes.data
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('book_appointment.html', form=form)

@app.route('/view_patient/<int:id>')
def view_patient(id):
    patient = Patient.query.get_or_404(id)
    return render_template('view_patient.html', patient=patient)

@app.route('/view_doctor/<int:id>')
def view_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    return render_template('view_doctor.html', doctor=doctor)

@app.route('/view_appointment/<int:id>')
def view_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return render_template('view_appointment.html', appointment=appointment)

if __name__ == '__main__':
    app.run(debug=True)
