# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

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
