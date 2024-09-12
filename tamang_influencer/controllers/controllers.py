from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
# from odoo.addons.website_forum.controllers.main import WebsiteForum
from odoo.addons.website_mail.controllers.main import WebsiteMail
from odoo.addons.website_forum.controllers.website_forum import WebsiteProfile

class InfluencerController(http.Controller):
    @http.route('/my/become_influencer', type='http', auth='user', website=True)
    def become_influencer(self, **kw):
        user = request.env.user
        if not user.influencer_forum_id:
            user.action_become_influencer()
        if not user.website_published:
            user.write({'website_published': True})
        return request.redirect('/my/my_forum')

    @http.route('/my/my_forum', type='http', auth='user', website=True)
    def my_forum(self, **kw):
        user = request.env.user
        forum = user.influencer_forum_id
        if not forum:
            return request.render('website.page_not_found')
        return request.redirect('/forum/%s?view=feed' % slug(forum), code=302)


class ForumNotificationController(http.Controller):

    @http.route('/forum/mark_notification_read/<int:notification_id>', type='http', auth="user", website=True)
    def mark_notification_read(self, notification_id, redirect_url=None, **kwargs):
        """Marks the notification as read."""
        notification = request.env['forum.notification'].browse(notification_id)
        if notification.exists() and notification.user_id.id == request.env.user.id:
            notification.is_read = True

        return request.redirect(redirect_url or '/forum')

    @http.route('/forum/delete_notification/<int:notification_id>', type='http', auth="user", website=True)
    def delete_notification(self, notification_id, redirect_url=None, **kwargs):
        """Deletes the notification."""
        notification = request.env['forum.notification'].browse(notification_id)
        if notification.exists() and notification.user_id.id == request.env.user.id:
            notification.unlink()  # Deletes the notification

        return request.redirect(redirect_url or '/forum')


class CustomWebsiteMail(WebsiteMail):

    @http.route(['/website_mail/follow'], type='json', auth="public", website=True)
    def website_message_subscribe(self, id=0, object=None, message_is_follower="on", email=False, **post):
        # og call
        res = super(CustomWebsiteMail, self).website_message_subscribe(id, object, message_is_follower, email, **post)

        if res:  # followed
            followed_record = request.env[object].browse(int(id))

            if followed_record.exists():
                post_author = followed_record.creator_id

                if post_author and post_author.id != request.env.user.id:
                    if object == 'forum.post':
                        request.env['forum.notification'].sudo().create({
                            'user_id': post_author.id,
                            'post_id': followed_record.id,
                            'message': f"{request.env.user.name} has started following you.",
                            'is_read': False,
                        })
                    else:
                        request.env['forum.notification'].sudo().create({
                            'user_id': post_author.id,
                            'message': f"{request.env.user.name} has started following you.",
                            'is_read': False,
                        })

        return res


class CustomWebsiteForum(WebsiteProfile):
    @http.route('/forum/<model("forum.forum"):forum>/post/<model("forum.post"):post>/upvote', type='json',
                auth="public", website=True)
    def post_upvote(self, forum, post, **kwargs):
        res = super(CustomWebsiteForum, self).post_upvote(forum, post, **kwargs)

        # gen notif for user
        post_author = post.create_uid
        if post_author and post_author.id != request.uid:
            request.env['forum.notification'].sudo().create({
                'user_id': post_author.id,
                'post_id': post.id,
                'message': f"{request.env.user.name} liked your post.",
                'is_read': False,
            })

        return res