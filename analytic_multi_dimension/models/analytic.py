# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    d1 = fields.Many2one(
        'account.dimension.line',
        string='Org',
        domain=[('dimension_id.level', '=', '1')],
        ondelete='set null',
    )
    d2 = fields.Many2one(
        'account.dimension.line',
        string='Dept',
        domain=[('dimension_id.level', '=', '2')],
        ondelete='set null',
    )
    d3 = fields.Many2one(
        'account.dimension.line',
        string='Programme',
        domain=[('dimension_id.level', '=', '3')],
        ondelete='set null',
    )
    d4 = fields.Many2one(
        'account.dimension.line',
        string='Project',
        domain=[('dimension_id.level', '=', '4')],
        ondelete='set null',
    )
    d5 = fields.Many2one(
        'account.dimension.line',
        string='Activity Group',
        domain=[('dimension_id.level', '=', '5')],
        ondelete='set null',
    )
    d6 = fields.Many2one(
        'account.dimension.line',
        string='Activity',
        domain=[('dimension_id.level', '=', '6')],
        ondelete='set null',
    )
    _sql_constraints = [
        ('dimension_uniq', 'unique(d1, d2, d3, d4, d5, d6)', 'Analytic Account Dimensions must be unique!'),
    ]
