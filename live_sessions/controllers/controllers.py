from odoo import http
from odoo.http import request

class LiveSessionController(http.Controller):

    @http.route('/live_session/info/<int:session_id>', type='http', auth='public', website=True)
    def session_info(self, session_id, **kwargs):
        session = request.env['live.session.info'].sudo().browse(session_id)
        return request.render('live_sessions.live_session_info_template', {
            'session': session
        })
    @http.route('/live_session/register', type='http', auth='user', methods=['POST'], csrf=False)
    def register_session(self, session_id, frequency_id):
        user_id = request.env.user.id
        frequency = request.env['live.session.frequency'].sudo().browse(int(frequency_id))
        
        if user_id not in frequency.student_ids.ids:
            frequency.write({'student_ids': [(4, user_id)]})
        
        return request.redirect('/live_session/success')
    
    @http.route('/live_session/success', type='http', auth='public', website=True)
    def register_success(self):
        return request.render('live_sessions.registration_success_template')
        
    @http.route('/create/coach', type='http', auth='public', website=True,csrf=False)
    def create_coach(self, **kwargs):
        # Get the current user's partner record
        user = request.env.user
        partner = user.partner_id

        if not partner.exists():
            return request.make_response("Error: Partner record not found", status=404)

        # Prepare the data for update, excluding the resume field
        update_values = {
            'phone': kwargs.get('phone'),
            'qualification': kwargs.get('qualification'),
            'teaching_experience': kwargs.get('teaching_experience'),
            'specialization': kwargs.get('specialization'),
            'comments': kwargs.get('comments'),
            'status': 'submitted',  # Set status to "submitted"
        }

        # Update the partner record
        partner.sudo().write(update_values)
        return request.make_response("Record updated successfully")