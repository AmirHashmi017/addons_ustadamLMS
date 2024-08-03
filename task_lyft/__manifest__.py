# -*- coding: utf-8 -*-
{
    'name': "task_lyft",

    'summary': "Freelance Web Platform for Students",

    'description': """
        Freelance Platform for UET students 
    """,

    'author': "Sheri Moon & Amir",
    'website': "https://www.tasklyft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/tasklyft_homepage.xml',
        'views/tasklyft_servicepage.xml',
        'views/tasklyft_gigpage.xml',
        'views/tasklyft_nav.xml',
        'views/tasklyft_footer.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

