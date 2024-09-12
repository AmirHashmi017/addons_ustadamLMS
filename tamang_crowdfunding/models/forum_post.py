from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class ForumPost(models.Model):
    _inherit = 'forum.post'

    @api.model
    def create(self, vals):
        forum = self.env['forum.forum'].browse(vals.get('forum_id'))
        if forum.forum_category == 'personal':
            if forum.create_uid != self.env.user:
                raise AccessError(_("You are not allowed to create posts in this forum."))

        posts = super(ForumPost, self).create(vals)

        for post in posts:
            if forum.forum_category != 'elearning':
                post.sudo().state = 'active'
                post.sudo().can_post = True
                post.sudo().can_answer = False
        return posts
