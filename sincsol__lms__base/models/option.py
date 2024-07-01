from odoo import models, fields

class Option(models.Model):
    _name = "ustadam.option"
    _description = "will hold option info"

    name = fields.Char(string='Name', required=True)
    is_correct = fields.Boolean(string='IsCorrect', required=True)

    option_id = fields.Many2one('ustadam.question', string='OptionID')
    # question_id = fields.Many2one('ustadam.question', string='Question')