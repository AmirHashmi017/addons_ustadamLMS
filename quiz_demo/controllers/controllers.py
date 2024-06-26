# -*- coding: utf-8 -*-
# from odoo import http


# class ./addonsSincsol/quizzesDemo(http.Controller):
#     @http.route('/./addons_sincsol/quizzes_demo/./addons_sincsol/quizzes_demo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./addons_sincsol/quizzes_demo/./addons_sincsol/quizzes_demo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./addons_sincsol/quizzes_demo.listing', {
#             'root': '/./addons_sincsol/quizzes_demo/./addons_sincsol/quizzes_demo',
#             'objects': http.request.env['./addons_sincsol/quizzes_demo../addons_sincsol/quizzes_demo'].search([]),
#         })

#     @http.route('/./addons_sincsol/quizzes_demo/./addons_sincsol/quizzes_demo/objects/<model("./addons_sincsol/quizzes_demo../addons_sincsol/quizzes_demo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./addons_sincsol/quizzes_demo.object', {
#             'object': obj
#         })

