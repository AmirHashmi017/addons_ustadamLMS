import base64
import random
import uuid

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_forum.controllers.website_forum import WebsiteForum

from odoo import http, tools, _
from odoo.exceptions import UserError
from odoo.http import request


class CustomWebsiteForum(WebsiteForum):

    @http.route([
        '/forum/<model("forum.forum"):forum>/<string:view>',  # Specific route with view parameter
        '/forum/<model("forum.forum"):forum>/<string:view>/page/<int:page>',  # Specific route with view and page
        '/forum/<model("forum.forum"):forum>/<string:view>',  # Specific route for feed
        '/forum/all',
        '/forum/all/page/<int:page>',
        '/forum/<model("forum.forum"):forum>',
        '/forum/<model("forum.forum"):forum>/page/<int:page>',
        '/forum/<model("forum.forum"):forum>/tag/<model("forum.tag"):tag>/questions',
        '/forum/<model("forum.forum"):forum>/tag/<model("forum.tag"):tag>/questions/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=WebsiteForum.sitemap_forum)
    def questions(self, forum=None, tag=None, page=1, filters='all', my=None, sorting=None, search='',
                  create_uid=False, include_answers=False, view=None, **post):
        def get_partner_info(partners):
            output = []
            for partner in partners:
                _, partner_followers_count = request.env['forum.partner.helper'].get_partners_by_type(partner,
                                                                                                      'follower')
                _, partner_following_count = request.env['forum.partner.helper'].get_partners_by_type(partner,
                                                                                                      'following')
                output.append({
                    'partner': partner,
                    'followers_count': partner_followers_count,
                    'following_count': partner_following_count,
                })
            return output

        followers = following = notification = []
        notification_count = 0

        if view == 'feed':
            following, _ = request.env['forum.partner.helper'].get_partners_by_type(request.env.user.partner_id,
                                                                                    'following')
            following_ids = []
            for partner in following:
                user = request.env['res.users'].sudo().search([('partner_id', '=', partner.id)])
                following_ids.append(user.id)

            followed_forums = request.env['forum.forum'].search([('create_uid', 'in', following_ids)])

            posts = request.env['forum.post'].search([
                ('forum_id', 'in', followed_forums.ids)
            ])

            posts = posts.sorted(key=lambda p: p.create_date, reverse=True)

            latest_posts_by_forum = {}
            for p in posts:
                if p.forum_id.id not in latest_posts_by_forum:
                    latest_posts_by_forum[p.forum_id.id] = p

            latest_posts = list(latest_posts_by_forum.values())

            combined_posts = []

            # If the user has viewed the latest posts, add some random posts
            if latest_posts:
                # Fetch random posts excluding the already fetched latest posts
                random_posts = request.env['forum.post'].search([
                    ('id', 'not in', [p.id for p in latest_posts]),
                    ('forum_id.forum_category', '=', 'personal')
                ])

                # Determine how many posts are needed to reach a minimum of 10
                num_latest_posts = len(latest_posts)
                num_needed_posts = max(10 - num_latest_posts, 0)

                # Limit the random sample size to ensure total posts are between 10 and 15
                random_sample_size = min(num_needed_posts, len(random_posts))
                random_sample = random.sample(random_posts, random_sample_size)

                # Combine the latest posts with the random posts if needed
                combined_posts = latest_posts + random_sample if num_latest_posts < 10 else latest_posts

                # Sort the combined list by creation date
                combined_posts = sorted(combined_posts, key=lambda p: p.create_date, reverse=True)

                # If the total combined posts exceed 15, truncate to the first 15
                combined_posts = combined_posts[:15]
            else:
                all_posts = request.env['forum.post'].search([
                    ('forum_id.forum_category', '=', 'personal')
                ])
                combined_posts = random.sample(all_posts, min(10, len(all_posts)))  # Limit to 10 random posts

                combined_posts = sorted(combined_posts, key=lambda p: p.create_date, reverse=True)

            combined_posts = request.env['forum.post'].sudo().browse([p.id for p in combined_posts])

            response = super(CustomWebsiteForum, self).questions(forum, tag, page, filters, my, sorting, search,
                                                                 create_uid, include_answers, **post)

            response.qcontext.update({
                'posts': combined_posts,
                'view': view,
            })
            return response

        elif my == 'favourites':
            favourite_posts = request.env['forum.post'].search([
                ('favourite_ids', 'in', request.env.user.id)
            ])

            response = super(CustomWebsiteForum, self).questions(forum, tag, page, filters, my, sorting, search,
                                                                 create_uid, include_answers, **post)

            response.qcontext.update({
                'question_ids': favourite_posts,
                'question_count': len(favourite_posts),
                'view': view,
            })
            return response

        elif view in ['followers', 'following', 'notification']:
            if view == 'followers':
                followers, _ = request.env['forum.partner.helper'].get_partners_by_type(request.env.user.partner_id,
                                                                                        'follower')
                followers = get_partner_info(followers)
            elif view == 'following':
                following, _ = request.env['forum.partner.helper'].get_partners_by_type(request.env.user.partner_id,
                                                                                        'following')
                following = get_partner_info(following)
            elif view == 'notification':
                notification = request.env['forum.notification'].sudo().get_user_notifications()
                notification_count = request.env['forum.notification'].get_notification_count()

            response = super(CustomWebsiteForum, self).questions(forum, tag, page, filters, my, sorting, search,
                                                                 create_uid, include_answers, **post)

            response.qcontext.update({
                'followers': followers,
                'following': following,
                'notification': notification,
                'notification_count': notification_count,
                'view': view,
            })
            return response

        else:
            return super(CustomWebsiteForum, self).questions(forum, tag, page, filters, my, sorting, search, create_uid,
                                                             include_answers, **post)

    @http.route('/forum/<model("forum.forum"):forum>/post/<model("forum.post"):post>/comment', type='http', auth="user",
                methods=['POST'], website=True)
    def post_comment(self, forum, post, **kwargs):
        question = post.parent_id or post

        if kwargs.get('comment'):
            if post.forum_id.forum_category == 'personal':
                # Allow comment without any restrictions
                body = tools.mail.plaintext2html(kwargs['comment'])
                post.with_context(mail_create_nosubscribe=True).message_post(
                    body=body,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment'
                )
                question._update_last_activity()

                # notification
                post_author = post.create_uid
                if post_author and post_author != request.env.user:
                    request.env['forum.notification'].sudo().create({
                        'user_id': post_author.id,
                        'post_id': post.id,
                        'message': f"{request.env.user.name} commented on your post: {kwargs['comment']}",
                    })

            else:
                if post.forum_id.id == forum.id:
                    # Existing logic for non-personal categories
                    body = tools.mail.plaintext2html(kwargs['comment'])
                    post.with_context(mail_create_nosubscribe=True).message_post(
                        body=body,
                        message_type='comment',
                        subtype_xmlid='mail.mt_comment'
                    )
                    question._update_last_activity()
        return request.redirect(f'/forum/{slug(forum)}/{slug(question)}')

    @http.route('/forum/<model("forum.forum"):forum>/post/<model("forum.post"):post>/downvote', type='json',
                auth="public", website=True)
    def post_downvote(self, forum, post, **kwargs):
        if not request.session.uid:
            return {'error': 'anonymous_user'}
        if request.uid == post.create_uid.id:
            return {'error': 'own_post'}

        user_vote = post.user_vote
        if user_vote > 0:
            return post.vote(upvote=False)
        else:
            return {'error': 'Cannot downvote unless upvoted'}

    @http.route(['/forum/<model("forum.forum"):forum>/new',
                 '/forum/<model("forum.forum"):forum>/<model("forum.post"):post_parent>/reply'],
                type='http', auth="user", methods=['POST'], website=True)
    def post_create(self, forum, post_parent=None, **post):
        # Check if content is empty
        if post.get('content', '') == '<p><br></p>':
            return request.render('http_routing.http_error', {
                'status_code': _('Bad Request'),
                'status_message': post_parent and _('Reply should not be empty.') or _('Question should not be empty.')
            })

        # Process media files if any
        media_files = request.httprequest.files.getlist('media_upload')
        media_html = ''
        if media_files:
            for media_file in media_files:
                media_html += self._process_media_file(media_file)

        # Update content with embedded media
        # content = post.get('content', '') + media_html

        post_tag_ids = forum._tag_to_write_vals(post.get('post_tags', ''))
        if forum.has_pending_post:
            return request.redirect("/forum/%s/ask" % slug(forum))

        new_question = request.env['forum.post'].create({
            'forum_id': forum.id,
            'name': post.get('post_name') or (post_parent and 'Re: %s' % (post_parent.name or '')) or '',
            'content': post.get('content', False) + media_html,
            'parent_id': post_parent and post_parent.id or False,
            'tag_ids': post_tag_ids
        })
        if post_parent:
            post_parent._update_last_activity()
        return request.redirect(f'/forum/{slug(forum)}/{slug(post_parent) if post_parent else new_question.id}')

    @http.route('/forum/<model("forum.forum"):forum>/post/<model("forum.post"):post>/save', type='http', auth="user",
                methods=['POST'], website=True)
    def post_save(self, forum, post, **kwargs):
        # Collect values from the form
        vals = {
            'content': kwargs.get('content'),
        }

        # Validate and set the post name
        if 'post_name' in kwargs:
            if not kwargs.get('post_name').strip():
                return request.render('http_routing.http_error', {
                    'status_code': _('Bad Request'),
                    'status_message': _('Title should not be empty.')
                })

            vals['name'] = kwargs.get('post_name')

        # Set tags
        vals['tag_ids'] = forum._tag_to_write_vals(kwargs.get('post_tags', ''))

        # Handle media uploads
        media_files = request.httprequest.files.getlist('media_upload')
        if media_files:
            media_content = ""
            for media_file in media_files:
                if media_file and media_file.filename:
                    media_content += self._process_media_file(media_file)

            # Append media content to the existing post content
            if 'content' in vals:
                vals['content'] += media_content
            else:
                vals['content'] = media_content

        # Update the post
        post.write(vals)

        # Redirect to the appropriate page
        question = post.parent_id if post.parent_id else post
        return request.redirect("/forum/%s/%s" % (slug(forum), slug(question)))

    def _process_media_file(self, file):
        # Check file size
        if file and file.content_length > 10 * 1024 * 1024:  # 10MB limit
            raise UserError(_('File %s exceeds the maximum allowed size of 10MB.' % file.filename))

        # Generate a unique filename and save the file
        file_name = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1]
        file_data = base64.b64encode(file.read()).decode('utf-8')

        # Save the file as an attachment and make it public
        attachment = request.env['ir.attachment'].sudo().create({
            'name': file_name,
            'datas': file_data,
            'mimetype': file.content_type,
            'res_model': 'forum.post',  # Model name
            'res_id': 0,  # To be updated later
            'public': True,  # Set the attachment to be public
        })

        # Generate HTML based on file type
        if file.content_type.startswith('image/'):
            return '<img src="/web/content/%d/%s" alt="%s"/>' % (attachment.id, file_name, file_name)
        elif file.content_type.startswith('video/'):
            return '<video controls><source src="/web/content/%d/%s" type="%s"/>Your browser does not support the video tag.</video>' % (
                attachment.id, file_name, file.content_type)
        return ''
