# -*- coding: utf-8 -*-
# from odoo import http


# class ./addonsUstadam/sincsolLmsQuiz(http.Controller):
#     @http.route('/./addons_ustadam/sincsol__lms_quiz/./addons_ustadam/sincsol__lms_quiz', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./addons_ustadam/sincsol__lms_quiz/./addons_ustadam/sincsol__lms_quiz/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./addons_ustadam/sincsol__lms_quiz.listing', {
#             'root': '/./addons_ustadam/sincsol__lms_quiz/./addons_ustadam/sincsol__lms_quiz',
#             'objects': http.request.env['./addons_ustadam/sincsol__lms_quiz../addons_ustadam/sincsol__lms_quiz'].search([]),
#         })

#     @http.route('/./addons_ustadam/sincsol__lms_quiz/./addons_ustadam/sincsol__lms_quiz/objects/<model("./addons_ustadam/sincsol__lms_quiz../addons_ustadam/sincsol__lms_quiz"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./addons_ustadam/sincsol__lms_quiz.object', {
#             'object': obj
#         })

