from odoo import models, fields
from odoo.exceptions import UserError


class Option(models.Model):
    _name = "ustadam.option"
    _description = "will hold option info"

    name = fields.Char(string='Name', required=True)
    is_correct = fields.Boolean(string='IsCorrect', required=True)

    option_id = fields.Many2one('ustadam.question', string='OptionID')
    # question_id = fields.Many2one('ustadam.question', string='Question')
    
    
    def attempt_option(self):
        # Get the current user
        user_id = self.env.uid
        
        # Get the quiz context (assuming this method is called from a quiz context)
        quiz_id = self._context.get('quiz_id')

        # Hardcoded student_id as 1 (you might need to change this logic as per your requirements)
        student_id = 1

        # Find or create the student result for the current user and quiz
        student_result = self.env['ustadam.student_result'].search([
            ('student_id', '=', student_id),
            ('quiz_id', '=', quiz_id)
        ], limit=1)

        if not student_result:
            student_result = self.env['ustadam.student_result'].create({
                'student_id': student_id,
                'quiz_id': quiz_id,
                'marks': 0,
            })

        # Update the student result if the option is correct
        if self.is_correct:
            student_result.marks += 1

        # Open the student result form view
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ustadam.student_result',
            'view_mode': 'form',
            'res_id': student_result.id,
            'target': 'new',
        }