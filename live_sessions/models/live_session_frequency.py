from odoo import models, fields

class Live_Session_Frequency(models.Model):
    _name = 'live.session.frequency'
    _description = 'Live Sessions Frequency'

    day = fields.Date(string='Day')
    
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    
    frequency_type = fields.Selection([('One Day', 'Day'), ('daily', 'Daily'), ('weekly', 'Weekly')], string='Frequency Type')

    session_id = fields.Many2one('live.session.info', string='Session Id')
    curriculum_id = fields.One2many('live.session.curriculum', 'frequency_id', string='Material Id')