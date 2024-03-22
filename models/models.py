from odoo import models, fields, api


# The student model, which inherits the fields from res.partner
class Student(models.Model):
    _name = 'student'
    _description = 'Model to manage school students'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
        string='Related Partner', help='Partner-related data of the student')
    registration_ids = fields.One2many('registration', 'student_id', string='Inscripciones')

    # Student's ID and course ID
    student_DNI = fields.Integer(string='Cédula')
    course_id = fields.Many2one('course', string='Curso')

    # Additional fields specific to the student
    birth_date = fields.Date(string='Fecha de Nacimiento')
    age = fields.Integer(string='Edad', compute='_compute_age', store=True)

    @api.depends('birth_date')
    def _compute_age(self):
        for student in self:
            if student.birth_date:
                today = fields.Date.today()
                student.age = today.year - student.birth_date.year
            else:
                student.age = 0


# The teacher model, which inherits the fields from product.template
class Course(models.Model):
    _name = 'course'
    # _inherits = 'product.template'
    _description = 'Model to manage courses'

    product_id = fields.Many2one('product.template', string='Product', required=True, ondelete="cascade")
    course_name = fields.Char(string='Nombre del Curso')
    course_description = fields.Text(string='Descripción del Curso')
    subject_ids = fields.Many2many('subject', string='Materias')
    teacher_ids = fields.Many2many('teacher', string='Profesores')
    registration_ids = fields.One2many('registration', 'course_id', string='Inscripciones')


# The teacher model, which inherits the fields from res.partner
class Teacher(models.Model):
    _name = 'teacher'
    _description = 'Model to manage teachers'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
        string='Related Partner', help='Partner-related data of the teacher')
    
    teach_DNI = fields.Integer(string='Cédula')
    subject_ids = fields.One2many('subject', 'teacher_ids', string='Materias')


class Subject(models.Model):
    _name = 'subject'
    _description = 'Model to manage subjects'

    subject_name = fields.Char(string='Nombre de la Materia', required=True)
    course_id = fields.Many2one('course', string='Curso')
    teacher_ids = fields.Many2many('teacher', string='Profesores')


class Registration(models.Model):
    _name = 'registration'
    _description = 'Model to manage student registrations'

    registration_id = fields.Char(string='ID', required=True)
    student_id = fields.Many2one('student', string='Alumno')
    course_id = fields.Many2one('course', string='Curso')
    registration_date = fields.Date(string='Fecha de Inscripción', required=True)
