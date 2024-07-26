from odoo import models, fields

class Live_Session_Coach(models.Model):
    _inherit = 'res.partner'

    qualification = fields.Char(string="Qualification")
    teaching_experience = fields.Char(string="Teaching Experience")
    resume = fields.Binary(string="Resume")
    specialization = fields.Char(string="Specialization")
    comments = fields.Text(string="Comments")
    status = fields.Char(string="Status")

    def action_accept_request(self):
        for record in self:
            # Add logic to handle acceptance
            record.status = 'accepted'
    
    def action_reject_request(self):
        for record in self:
            # Add logic to handle rejection
            record.status = 'rejected'