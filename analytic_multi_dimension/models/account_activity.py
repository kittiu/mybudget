# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import itertools
from openerp import api, fields, models, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class AccountActivity(models.Model):
    _name = 'account.activity'
    _description = 'Activity'

    name = fields.Char(
        string='Activity',
        required=True,
    )
    budget_post_id = fields.Many2one(
        'account.budget.post',
        string='Budgetary Position',
        required=True,
    )
    _sql_constraints = [
        ('activity_uniq', 'unique(name)', 'Activity must be unique!'),
    ]
