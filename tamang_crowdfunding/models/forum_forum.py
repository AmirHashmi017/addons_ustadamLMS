from odoo import api, fields, models


class Forum(models.Model):
    _inherit = 'forum.forum'

    # Field to categorize the forum
    forum_category = fields.Selection([
        ('elearning', 'eLearning'),
        ('personal', 'Personal'),
        ('crowdfunding', 'crowdfunding'),
    ], string='Forum Category', required=True, default='elearning')

    @api.model
    def create_crowdfunding_forum(self):
        """Create a forum specifically for crowdfunding if it doesn't exist."""
        existing_forum = self.search([('name', '=', 'Crowdfunding Forum')], limit=1)
        if not existing_forum:
            self.create({
                'name': 'Crowdfunding Forum',
                'description': 'A forum dedicated to crowdfunding projects and discussions.',
                'forum_category': 'crowdfunding',
                'privacy': 'public',  # This makes the forum accessible to all users
            })
