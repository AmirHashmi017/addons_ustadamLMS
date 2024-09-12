from odoo import fields, models, api
from odoo.http import request


class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users', 'website.seo.metadata',
                'website.searchable.mixin', ]

    influencer_forum_id = fields.Many2one('forum.forum', string='Influencer Forum', compute='_compute_influencer_forum',
                                          store=True)

    def _compute_influencer_forum(self):
        for user in self:
            forum = self.env['forum.forum'].search([('create_uid', '=', user.id)], limit=1)
            user.influencer_forum_id = forum

    def action_become_influencer(self):
        for user in self:
            if not user.influencer_forum_id:
                forum = self.env['forum.forum'].create({
                    'name': f"{user.name}'s Timeline",
                    'forum_category': 'personal',
                })
                user.influencer_forum_id = forum
        return True

    @api.model
    def _search_get_detail(self, website, order, options):
        search_fields = ['name']
        fetch_fields = ['id', 'name', 'website_url']
        mapping = {
            'name': {'name': 'name', 'type': 'text', 'match': True},
            'website_url': {'name': 'website_url', 'type': 'text', 'truncate': False},
        }

        domain = website.website_domain()

        return {
            'model': 'res.users',
            'base_domain': [domain],
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'fa-user',
            'order': order,
        }

    @api.model
    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        results_data = super()._search_render_results(fetch_fields, mapping, icon, limit)
        for user, user_data in zip(self, results_data):
            user_data['website_url'] = '/profile/user/' + str(user.id)
        return results_data

    def _search_fetch(self, search_detail, search, limit, order):
        domain = [('influencer_forum_id', '!=', False), ('name', 'ilike', search)]
        users = self.sudo().search(domain, limit=limit, order=order)
        return users, len(users)
