# -*- coding: utf-8 -*-
# from odoo import http


# class ./addonsProject/taskLyft(http.Controller):
#     @http.route('/./addons_project/task_lyft/./addons_project/task_lyft', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./addons_project/task_lyft/./addons_project/task_lyft/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./addons_project/task_lyft.listing', {
#             'root': '/./addons_project/task_lyft/./addons_project/task_lyft',
#             'objects': http.request.env['./addons_project/task_lyft../addons_project/task_lyft'].search([]),
#         })

#     @http.route('/./addons_project/task_lyft/./addons_project/task_lyft/objects/<model("./addons_project/task_lyft../addons_project/task_lyft"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./addons_project/task_lyft.object', {
#             'object': obj
#         })

