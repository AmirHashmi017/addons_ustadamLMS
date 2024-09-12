# -*- coding: utf-8 -*-
{
    'name': "Tamang CrowdFunding",

    'summary': "Tamang CrowdFunding",

    'description': """
Long description of module's purpose
    """,

    'author': "SincSol",
    'website': "https://www.sincsol.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'website_slides_forum', 'website_profile', 'tamang_influencer'],
    
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    
    'post_init_hook': 'post_init_hook',
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

