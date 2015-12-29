# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import itertools
from openerp import api, fields, models, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


# class AccountActivityGroup(models.Model):
#     _name = 'account.activity.group'
#     _description = 'Activity Group'
# 
#     name = fields.Char(
#         string='Activity Group',
#         required=True,
#     )
#     activity_ids = fields.One2many(
#         'account.activity',
#         'group_id',
#         string='Activities',
#     )
#     _sql_constraints = [
#         ('activity_uniq', 'unique(name)',
#          'Activity Group must be unique!'),
#     ]


class AccountActivity(models.Model):
    _name = 'account.activity'
    _description = 'Activity'

    budget_post_id = fields.Many2one(
        'account.budget.post',
        string='Budgetary Position',
        required=True,
    )
    name = fields.Char(
        string='Activity',
        required=True,
    )
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        required=True,
    )
    _sql_constraints = [
        ('activity_uniq', 'unique(name, budget_post_id)',
         'Activity must be unique per group!'),
    ]

    @api.constrains('account_id')
    def _check_account_id(self):
        if self.account_id not in self.budget_post_id.account_ids:
            raise ValidationError(_('Activity account must be within '
                                    'accounts of budgetary position'))

