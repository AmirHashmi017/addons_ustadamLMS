# -*- coding: utf-8 -*-
# from odoo import http


# class AddonsUteach/liveSessions(http.Controller):
#     @http.route('/addons_uteach/live_sessions/addons_uteach/live_sessions', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/addons_uteach/live_sessions/addons_uteach/live_sessions/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('addons_uteach/live_sessions.listing', {
#             'root': '/addons_uteach/live_sessions/addons_uteach/live_sessions',
#             'objects': http.request.env['addons_uteach/live_sessions.addons_uteach/live_sessions'].search([]),
#         })

#     @http.route('/addons_uteach/live_sessions/addons_uteach/live_sessions/objects/<model("addons_uteach/live_sessions.addons_uteach/live_sessions"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('addons_uteach/live_sessions.object', {
#             'object': obj
#         })

