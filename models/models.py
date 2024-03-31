from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import re

# The student model, which inherits the fields from res.partner
class Student(models.Model):
    _name = 'student'
    _description = 'student_model'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, 
                                 index=True, string='Related Partner', help='Partner-related data of the student')
    
    # Relation to the registration table
    registration_ids = fields.One2many('registration', 'student_id', string='Inscripciones')

    # Student's ID and course ID
    student_DNI = fields.Integer(string='Cédula')
    course_id = fields.Many2one('course', string='Curso')

    # Additional fields specific to the student
    birth_date = fields.Date(string='Fecha de Nacimiento')
    age = fields.Integer(string='Edad', compute='_compute_age', store=True)

    # Computes the student's age based on the current's date, and his birth date
    # The for loop here is used in case reloading several student's age is necessary
    @api.depends('birth_date')
    def _compute_age(self):
        for student in self:
            if student.birth_date:
                today = fields.Date.today()
                student.age = today.year - student.birth_date.year
            else:
                student.age = 0

    @api.onchange('student_DNI')
    def on_change_student_dni(self):
        existing_student = self.env['student'].search([('student_DNI', '=', self.student_DNI)])
        if existing_student:
            # Display a warning message indicating that the student is already registered
            warning_message = {
                'title': '¡Advertencia!',
                'message': 'La cédula ingresada pertenece a un estudiante ya registrado.',
            }
            return {'warning': warning_message}

    @api.constrains('student_DNI')
    def _check_student_dni(self):
        for record in self:
            if record.student_DNI <= 0:
                raise ValidationError('La cédula debe ser un número positivo.')
            if not re.match(r'^[0-9]+$', str(record.student_DNI)):
                raise ValidationError('Cédula Inválida. Debe contener números solamente.')

# The teacher model, which inherits the fields from product.template
class Course(models.Model):
    _name = 'course'
    _description = 'course_model'
    _inherits = {'product.template': 'product_id'}

    product_id = fields.Many2one('product.template', required=True, ondelete="cascade", auto_join=True, index=True,
                                 string='Product', help='Product-related data of the course')

    course_name = fields.Char(string='Nombre del Curso')
    course_description = fields.Text(string='Descripción del Curso')
    subject_ids = fields.Many2many('subject', string='Materias')
    teacher_ids = fields.Many2many('teacher', string='Profesores')
    registration_ids = fields.One2many('registration', 'course_id', string='Inscripciones')


# The teacher model, which inherits the fields from res.partner
class Teacher(models.Model):
    _name = 'teacher'
    _description = 'teacher_model'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
        string='Related Partner', help='Partner-related data of the teacher')
    
    teach_DNI = fields.Integer(string='Cédula')
    subject_ids = fields.One2many('subject', 'teacher_ids', string='Materias')


# The subject model, it provides fiels for the name of the subject, course_id, and teachers
class Subject(models.Model):
    _name = 'subject'
    _description = 'subject_model'

    subject_name = fields.Char(string='Nombre de la Materia', required=True)
    course_id = fields.Many2one('course', string='Curso')
    teacher_ids = fields.Many2many('teacher', string='Profesores')

    @api.constrains('subject_name')
    def create(self, values):
        if 'subject_name' in values:
            existing_subject = self.env['subject'].search([('subject_name', '=', values['subject_name'])], limit=1)
            if existing_subject:
                raise UserError("El nombre de la materia ya existe. Por favor, ingrese un nombre diferente.")
        return super(Subject, self).create(values)


# The registration model, it provides fiels for the registration ID, student, course, and registration date
class Registration(models.Model):
    _name = 'registration'
    _description = 'registration_model'

    registration_id = fields.Char(string='ID', required=True)
    student_id = fields.Many2one('student', string='Alumno')
    course_id = fields.Many2one('course', string='Curso')
    registration_date = fields.Date(string='Fecha de Inscripción', required=True)
