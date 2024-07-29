from odoo import models, fields
from odoo.exceptions import AccessError


class Live_Session_Coach(models.Model):
    _inherit = 'res.partner'

    qualification = fields.Char(string="Qualification")
    teaching_experience = fields.Char(string="Teaching Experience")
    resume = fields.Binary(string="Resume")
    specialization = fields.Char(string="Specialization")
    comments = fields.Text(string="Comments")
    status = fields.Char(string="Status")

    def action_accept_request(self):
        internal_user_group = self.env.ref('base.group_user')
        teacher_group = self.env.ref('live_sessions.group_teacher')
        portal_group = self.env.ref('base.group_portal')

        for partner in self:
             user = partner.user_ids and partner.user_ids[0]  # Get the linked user
             if user:
                 try:
                     user.sudo().write({'groups_id': [(3, portal_group.id), (4, internal_user_group.id), (4, teacher_group.id)]})
                 except AccessError:
                     raise AccessError(_("You are not allowed to modify user groups. Contact your administrator."))
             partner.status = 'accepted'
        
        # redirect('../')



    
    def action_reject_request(self):
        for record in self:
            # Add logic to handle rejection
            record.status = 'rejected'