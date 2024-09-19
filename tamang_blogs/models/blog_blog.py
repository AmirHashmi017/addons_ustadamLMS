from odoo import models, api, fields

class BlogInherit(models.Model):
    _inherit = 'blog.blog'

    @api.model
    def create_crowdfunding_blog(self):
        existing_investment_blog = self.env['blog.blog'].search([('name', '=', 'Investment Funding')], limit=1)
        if not existing_investment_blog:
            # Create a new blog with the name 'Investment Funding'
            investment_blog = self.create({
                'name': 'Investment Funding',
                'subtitle': 'Posts related to investment funding',
            })
    
        # Check if the 'Donations Funding' blog exists
        existing_donations_blog = self.env['blog.blog'].search([('name', '=', 'Donations Funding')], limit=1)
        if not existing_donations_blog:
            # Create a new blog with the name 'Donations Funding'
            donations_blog = self.create({
                'name': 'Donations Funding',
                'subtitle': 'Posts related to donations funding',
            })
        
        # Return the IDs of the created or existing blogs
        return {
            'investment_blog_id': existing_investment_blog.id if existing_investment_blog else investment_blog.id,
            'donations_blog_id': existing_donations_blog.id if existing_donations_blog else donations_blog.id
        }

class BlogPostInherit(models.Model):
    _inherit = 'blog.post'

    @api.model
    def create(self, vals):
        # Get the 'Crowdfunding' blog ID
        blog_id = self.env['blog.blog'].create_crowdfunding_blog()
        if blog_id:
            # Set the blog_id to the Crowdfunding blog
            vals['blog_id'] = blog_id
        return super(BlogPostInherit, self).create(vals)
