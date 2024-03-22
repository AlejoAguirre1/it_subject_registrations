# -*- coding: utf-8 -*-
# from odoo import http


# class ItSubjectRegistrations(http.Controller):
#     @http.route('/it_subject_registrations/it_subject_registrations', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/it_subject_registrations/it_subject_registrations/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('it_subject_registrations.listing', {
#             'root': '/it_subject_registrations/it_subject_registrations',
#             'objects': http.request.env['it_subject_registrations.it_subject_registrations'].search([]),
#         })

#     @http.route('/it_subject_registrations/it_subject_registrations/objects/<model("it_subject_registrations.it_subject_registrations"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('it_subject_registrations.object', {
#             'object': obj
#         })
