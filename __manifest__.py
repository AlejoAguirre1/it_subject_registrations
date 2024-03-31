# -*- coding: utf-8 -*-
{
    'name': "IT Subject Registrations",

    'summary': """
        A module designed to manage the enrolment of new students 
        in an educational system.""",

    'description': """
        This module allows registering students and teachers, as
        well as modifying the subjects they study/teach and the courses
        they are in.
    """,

    'author': "Alejandro Aguirre",
    'website': "https://github.com/AlejoAguirre1/it_subject_registrations/tree/master",

    # Categories can be used to filter modules in modules listing
    'category': 'Human Resources',
    'version': '0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/registration_view.xml',
        'views/course_view.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/subject_view.xml',
        'views/res_partner_views.xml',
        'views/record_menu.xml'
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
