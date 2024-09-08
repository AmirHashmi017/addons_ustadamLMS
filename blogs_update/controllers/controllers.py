# -*- coding: utf-8 -*-
# from odoo import http


# class ./addonsTesting/blogsUpdate(http.Controller):
#     @http.route('/./addons_testing/blogs_update/./addons_testing/blogs_update', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./addons_testing/blogs_update/./addons_testing/blogs_update/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./addons_testing/blogs_update.listing', {
#             'root': '/./addons_testing/blogs_update/./addons_testing/blogs_update',
#             'objects': http.request.env['./addons_testing/blogs_update../addons_testing/blogs_update'].search([]),
#         })

#     @http.route('/./addons_testing/blogs_update/./addons_testing/blogs_update/objects/<model("./addons_testing/blogs_update../addons_testing/blogs_update"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./addons_testing/blogs_update.object', {
#             'object': obj
#         })

