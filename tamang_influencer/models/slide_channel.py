from odoo import api, fields, models


class Channel(models.Model):
    _inherit = 'slide.channel'

    @api.model_create_multi
    def create(self, vals_list):
        # Filter forums to ensure only eLearning forums are used for eLearning channels
        for vals in vals_list:
            if 'forum_id' in vals:
                forum = self.env['forum.forum'].browse(vals['forum_id'])
                if forum and forum.forum_category != 'elearning':
                    raise ValueError("The selected forum is not valid for eLearning courses.")

        channels = super(Channel, self.with_context(mail_create_nosubscribe=True)).create(vals_list)
        channels.forum_id.privacy = False
        return channels

    def write(self, vals):
        if 'forum_id' in vals:
            forum = self.env['forum.forum'].browse(vals['forum_id'])
            if forum.forum_category != 'elearning':
                raise ValueError("The selected forum is not valid for eLearning courses.")

        old_forum = self.forum_id

        res = super(Channel, self).write(vals)
        if 'forum_id' in vals:
            self.forum_id.privacy = False
            if old_forum != self.forum_id:
                old_forum.write({
                    'privacy': 'private',
                    'authorized_group_id': self.env.ref('website_slides.group_website_slides_officer').id,
                })
        return res
