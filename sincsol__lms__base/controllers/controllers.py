# -*- coding: utf-8 -*-
# from odoo import http


# class ./addonsSincsol/sincsolLmsBase(http.Controller):
#     @http.route('/./addons_sincsol/sincsol__lms__base/./addons_sincsol/sincsol__lms__base', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./addons_sincsol/sincsol__lms__base/./addons_sincsol/sincsol__lms__base/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./addons_sincsol/sincsol__lms__base.listing', {
#             'root': '/./addons_sincsol/sincsol__lms__base/./addons_sincsol/sincsol__lms__base',
#             'objects': http.request.env['./addons_sincsol/sincsol__lms__base../addons_sincsol/sincsol__lms__base'].search([]),
#         })

#     @http.route('/./addons_sincsol/sincsol__lms__base/./addons_sincsol/sincsol__lms__base/objects/<model("./addons_sincsol/sincsol__lms__base../addons_sincsol/sincsol__lms__base"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./addons_sincsol/sincsol__lms__base.object', {
#             'object': obj
#         })

