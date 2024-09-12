from odoo.addons.website_forum.controllers.website_forum import WebsiteForum
from odoo import http
from odoo.http import request


class CustomCrowdfundingForum(WebsiteForum):

    @http.route([
        '/forum/<model("forum.forum"):forum>/<string:view>',
        '/forum/<model("forum.forum"):forum>/<string:view>/page/<int:page>',
        '/forum/all',
        '/forum/all/page/<int:page>',
        '/forum/<model("forum.forum"):forum>',
        '/forum/<model("forum.forum"):forum>/page/<int:page>',
        '/forum/<model("forum.forum"):forum>/tag/<model("forum.tag"):tag>/questions',
        '/forum/<model("forum.forum"):forum>/tag/<model("forum.tag"):tag>/questions/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=WebsiteForum.sitemap_forum)
    def questions(self, forum=None, tag=None, page=1, filters='all', my=None, sorting=None, search='',
                  create_uid=False, include_answers=False, view=None, **post):
        # Handle the crowdfunding view
        if view == 'crowdfunding':
            # Fetch crowdfunding-specific data
            crowdfunding_forums = request.env['forum.forum'].sudo().search([
                ('forum_category', '=', 'crowdfunding')
            ])

            # Get posts for the crowdfunding forums
            crowdfunding_posts = request.env['forum.post'].sudo().search([
                ('forum_id', 'in', crowdfunding_forums.ids)
            ])

            # Prepare the response and call the super method
            response = super(CustomCrowdfundingForum, self).questions(
                forum, tag, page, filters, my, sorting, search, create_uid, include_answers, view, **post
            )

            # Update context with crowdfunding-related data
            response.qcontext.update({
                'view': view,
                'posts': crowdfunding_posts,
            })
            return response

        # Handle other views by calling the parent method
        return super(CustomCrowdfundingForum, self).questions(
            forum, tag, page, filters, my, sorting, search, create_uid, include_answers, view, **post
        )
