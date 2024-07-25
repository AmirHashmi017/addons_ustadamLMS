from odoo import http
from odoo.http import request

class LiveSessionController(http.Controller):

    @http.route('/live_session/info/<int:session_id>', type='http', auth='public', website=True)
    def session_info(self, session_id, **kwargs):
        session = request.env['live.session.info'].sudo().browse(session_id)
        return request.render('live_sessions.live_session_info_template', {
            'session': session
        })
