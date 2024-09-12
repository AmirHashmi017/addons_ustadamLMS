{
    'name': 'Loan Management',
    'version': '17.0.1.0.0',

    'summary': 'Helps You To Manage Loan Requests/Disbursement/Repayments/Amortization Operations',
    'description': """
        This module allows you to create different types of loans,
        manage loan requests and amortization operations simply,
        and create invoices for each repayment amount.
    """,

    'author': 'SincSol',
    'depends': ['mail', 'account', 'base'],

    'data': [
        'security/loan_management_groups.xml',
        'security/loan_management_security.xml',
        'security/ir.model.access.csv',
        'data/loan_journal_data.xml',
        'data/ir_sequence_data.xml',
        'views/loan_type_views.xml',
        'views/loan_request_views.xml',
        'views/manager_request_views.xml',
        'views/user_request_views.xml',
        'views/repayment_lines_views.xml',
        'views/loan_documents_views.xml',
        'views/res_config_settings_views.xml',
        'views/loan_management_menus.xml',
        'views/res_partner_views.xml',
        'wizard/message_popup_views.xml',
        'wizard/reject_reason_views.xml',
        'report/loan_management_reports.xml',
        'report/loan_report_templates.xml',
        'views/website_loan_request_templates.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
