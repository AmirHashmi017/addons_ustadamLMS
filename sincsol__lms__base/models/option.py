from odoo import models, fields

class Option(models.Model):
    _name = "ustadam.option"
    _description = "will hold option info"

    content = fields.Char(string='Text', required=True)
    is_correct = fields.Boolean(string='IsCorrect', required=True)

    question_id = fields.Many2one('ustadam.question', string='Question')
    option_id = fields.Many2one('ustadam.question', string='OptionID')