from odoo import models, fields

class Live_Session_Curriculum(models.Model):
    _name = 'live.session.curriculum'
    _description = 'Live Sessions Curriculum'

    text = fields.Text(string='Text')
    video_url = fields.Char(string='Video URL')
    attachments = fields.Binary(string='Attachments')

    # quiz_ids = fields.One2many('uteach.quiz', 'curriculum_id', string='Quiz Ids')
    frequency_id = fields.Many2one('live.session.frequency', string='Frequency Id')