from odoo import models, fields

class Live_Session_Teacher(models.Model):
    _inherit="res.users"
    UID=fields.One2many('live.session.info','teacher_id',string="UID")

class Live_Session_Info(models.Model):
    _name = 'live.session.info'
    _description = 'Live Sessions Information'

    meeting_type = fields.Selection([('Online', 'Online'), ('In-Person', 'In-Person')], string='Meeting Type')
    meet_url = fields.Char(string='Meet URL')
    img = fields.Image(string='Image')
    lesson_name = fields.Char(string='Lesson Name')
    lesson_description = fields.Text(string='Lesson Description')
    learning_objectives = fields.Text(string='Learning Objectives')
    
    isFree = fields.Boolean(string='Is Free')
    price = fields.Float(string='Price')
    old_price = fields.Float(string='Old Price')
    number_of_participants = fields.Integer(string='Number of Participants')
    knowledge_level = fields.Selection([('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], string='Knowledge Level')
    hide_dates = fields.Boolean(string='Hide Dates')
    
    visibility = fields.Selection([('public', 'public'), ('private', 'private')], string='Visibility')

    frequency_ids = fields.One2many('live.session.frequency', 'session_id', string='FrequencyIds')
    teacher_id=fields.Many2one('res.users',string='Teacher ID')
