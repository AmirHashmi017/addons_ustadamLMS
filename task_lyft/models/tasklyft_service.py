from odoo import fields, models

class tasklyft_service(models.Model):
    _name = 'tasklyft.service'
    _description = 'TaskLyft Service'

    title = fields.Char(string='Title', required=True)
    category = fields.Selection([
        ('Software Developer', 'Software Developer'), 
        ('Web Developer', 'Web Developer'), 
        ('Mobile App Developer', 'Mobile App Developer'), 
        ('Graphic Designer', 'Graphic Designer'), 
        ('UI/UX Designer', 'UI/UX Designer'), 
        ('Data Analyst', 'Data Analyst'), 
        ('Odoo Developer', 'Odoo Developer'), 
        ('Word-Press Developer', 'Word-Press Developer')
    ], string='Category', required=True)
    experience_level = fields.Selection([
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'), 
        ('Professional', 'Professional')
    ], string='Experience Level')
    picture = fields.Image(string='Picture', required=True)    
    price_per_hour = fields.Float(string='Price Per Hour(PKR)', required=True)
    
    user_id = fields.Many2one('res.partner', string="User")
