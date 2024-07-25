from odoo import fields,models
class live_session_requests(models.Model):
    _name="live.session.requests"
    _description="To store Requests"
  
    name=fields.Char(string="name", required=True)
    email=fields.Char(string="Email", required=True)
    Phone=fields.Char(string="Phone" ,required=True)
    qualification=fields.Char(string="Qualification", required=True)
    teaching_experience=fields.Char(string="Teaching Experience", required=True)
    resume=fields.Binary(string="Resume" ,required=True)
    specialization=fields.Char("Specialization", required=True)
    reason=fields.Binary("Reason to Join", required=True)
    