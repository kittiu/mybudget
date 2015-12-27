# -*- coding: utf-8 -*-

{
    'name': 'Budget Multi Dimension',
    'version': '1.0',
    'website': 'http://ecosoft.co.th',
    'category': 'Hidden/Dependency',
    'depends': ['account',
                'analytic',
                'account_budget', ],
    'description': """
Extend Analytic to have multiple dimensions.
=============================================

    """,
    'data': [
#         'security/analytic_security.xml',
#         'security/ir.model.access.csv',
        'wizard/dimension_select_value_reference.xml',
        'views/account_dimension.xml',
        'views/analytic.xml',
        'views/account_budget.xml',
        'views/account_activity.xml',
        'views/account_invoice.xml',
#         'data/account.dimension.csv',
#         'data/account.dimension.line.csv',
#         'data/account.analytic.account.csv',
#         'data/crossovered.budget.csv',
#         'data/crossovered.budget.lines.csv',
#        'report/analytic_multi_dimension_report_view.xml',
#         'wizard/account_analytic_chart_view.xml',
    ],
    'demo': [
#         'data/analytic_demo.xml',
#         'data/analytic_account_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}
