from odoo import http
from odoo.http import request
import base64
class TasklyftController(http.Controller):

    @http.route('/create_gig', type='http', auth='user', website=True, csrf=True)
    def create_gig(self, **kwargs):
        if request.httprequest.method == 'POST':
            title = kwargs.get('title')
            category = kwargs.get('category')
            experience_level = kwargs.get('experience_level')
            price_per_hour = kwargs.get('price_per_hour')
            
            picture_file = kwargs.get('picture')
            
            
            picture = base64.b64encode(picture_file.read()) if picture_file else None

            
            request.env['tasklyft.service'].sudo().create({
                'title': title,
                'category': category,
                'experience_level': experience_level,
                'price_per_hour': price_per_hour,
                'picture': picture,
                'user_id': request.env.user.partner_id.id,
            })
            

        return request.render('task_lyft.services_page')

class TaskLyft(http.Controller):

    @http.route(['/services'], type='http', auth='public', website=True)
    def services_page(self, **kwargs):
        domain = []

        # Get filter parameters
        category = kwargs.get('category')
        title = kwargs.get('title')
        experience_level = kwargs.get('experience_level')
        price_range = kwargs.get('price_range')

        # Apply category filter
        if category:
            domain.append(('category', '=', category))

        # Apply title filter
        if title:
            domain.append(('title', 'ilike', title))

        # Apply experience level filter
        if experience_level:
            domain.append(('experience_level', '=', experience_level))

        # Apply price range filter
        if price_range:
            price_min, price_max = price_range.split('-')
            if price_min:
                domain.append(('price_per_hour', '>=', float(price_min)))
            if price_max:
                domain.append(('price_per_hour', '<=', float(price_max)))

        # Fetch filtered services
        services = request.env['tasklyft.service'].sudo().search(domain)

        return request.render('task_lyft.services_page', {
            'services': services
        })
