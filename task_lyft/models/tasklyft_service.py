from odoo import fields, models

class tasklyft_service(models.Model):
    _name = 'tasklyft.service'
    _description = 'TaskLyft Service'

    title = fields.Char(string='Title', required=True)
    category = fields.Selection([
        ('Matric', 'Matric'), 
        ('FSC(Pre Engineering)', 'FSC(Pre Engineering)'), 
        ('FSC(Pre Medical)', 'FSC(Pre Medical)'), 
        ('ICS', 'ICS'), 
        ('ICOM', 'ICOM'), 
        ('FA', 'FA'), 
        ('Pyhton', 'Pyhton'), 
        ('Web Development', 'Web Development'),
        ('C++', 'C++'),
        ('OOP and C#', 'OOP and C#'),
        ('ODOO Development', 'ODOO Development'),
        ('Graphic Designing', 'Graphic Designing'),
        ('Wordpress', 'Wordpress')
    ], string='Category', required=True)
    experience_level = fields.Selection([
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'), 
        ('Professional', 'Professional')
    ], string='Experience Level')
    Location=fields.Selection([
        ('UET Lahore','UET Lahore'),
        ('Shalamar Garden','Shalamar Garden'),
        ('Model Town','Model Town'),
        ('Gulberg','Gulberg'),
        ('Town Ship','Town Ship'),
        ('Muslim Town','Muslim Town'),
        ('Wahdat Road','Wahdat Road')
        ],string='Location',required=True)
    picture = fields.Image(string='Picture', required=True)

    price_per_month = fields.Float(string='Price Per Month(PKR)', required=True)
    
    user_id = fields.Many2one('res.partner', string="User")
