from odoo import api, fields, models


class Forum(models.Model):
    _inherit = 'forum.forum'

    # Field to store the creator of the forum
    creator_id = fields.Many2one(
        'res.users',
        string='Creator',
        index=True,
        ondelete='cascade'
    )

    # Field to categorize the forum
    forum_category = fields.Selection([
        ('elearning', 'eLearning'),
        ('personal', 'Personal')
    ], string='Forum Category', required=True, default='elearning')

    # karma_gen_question_new = fields.Integer(string='Asking a question', default=2)
    # karma_gen_answer_accept = fields.Integer(string='Accepting an answer', default=2)
    # karma_gen_answer_accepted = fields.Integer(string='Answer accepted', default=15)
    # karma_gen_answer_flagged = fields.Integer(string='Answer flagged', default=-100)
    # karma_answer = fields.Integer(string='Answer questions', default=3)
    # karma_edit_all = fields.Integer(string='Edit all posts', default=300)
    # karma_close_own = fields.Integer(string='Close own posts', default=100)
    # karma_close_all = fields.Integer(string='Close all posts', default=500)
    # karma_unlink_all = fields.Integer(string='Delete all posts', default=1000)
    # karma_upvote = fields.Integer(string='Upvote', default=5)
    # karma_answer_accept_own = fields.Integer(string='Accept an answer on own questions', default=20)
    # karma_answer_accept_all = fields.Integer(string='Accept an answer to all questions', default=500)
    # karma_comment_convert_own = fields.Integer(string='Convert own answers to comments and vice versa', default=50)
    # karma_comment_convert_all = fields.Integer(string='Convert all answers to comments and vice versa', default=500)
    # karma_comment_unlink_all = fields.Integer(string='Unlink all comments', default=500)
    # karma_flag = fields.Integer(string='Flag a post as offensive', default=500)
    # karma_post = fields.Integer(string='Ask questions without validation', default=100)
    # karma_moderate = fields.Integer(string='Moderate posts', default=1000)

    @api.depends_context('uid')
    def _compute_following_ids(self):
        """Compute the forums that the current user is following."""
        for forum in self:
            forum.following_ids = self.env['forum.forum'].search([
                ('followers_ids', 'in', self.env.user.id)
            ])

    @api.model
    def create(self, vals):
        """Override the create method to automatically set the forum category based on the creator."""
        if vals.get('creator_id') and not vals.get('forum_category'):
            vals['forum_category'] = 'personal'

        # Over-riding some default values for personal forums
        vals['privacy'] = 'connected'
        vals['karma_gen_question_upvote'] = 0
        vals['karma_gen_question_downvote'] = 0
        vals['karma_unlink_own'] = 0
        vals['karma_tag_create'] = 0
        vals['karma_edit_retag'] = 0
        vals['karma_edit_own'] = 0
        vals['karma_comment_own'] = 0
        vals['karma_comment_all'] = 0
        vals['karma_editor'] = 0
        vals['karma_user_bio'] = 0
        vals['karma_dofollow'] = 30
        vals['karma_comment_unlink_own'] = 0
        vals['karma_downvote'] = 100000
        vals['karma_ask'] = 0

        return super(Forum, self).create(vals)
