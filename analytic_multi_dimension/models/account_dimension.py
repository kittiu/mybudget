# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models


class account_dimension(models.Model):
    _name = 'account.dimension'
    _description = 'Account Dimension'
    _order = 'level'

    name = fields.Char(
        string='Dimension',
        required=True,
    )
    level = fields.Selection(
        [('1', '1'),
         ('2', '2'),
         ('3', '3'),
         ('4', '4'),
         ('5', '5'),
         ('6', '6'),
         ],
        string='Level',
    )
    activity = fields.Boolean(
        string='Activity Level',
        default=False,
    )
    line_ids = fields.One2many(
        'account.dimension.line',
        'dimension_id',
        string='Dimension Lines',
    )


class account_dimension_line(models.Model):
    _name = 'account.dimension.line'
    _description = 'Account Dimension'

    dimension_id = fields.Many2one(
        'account.dimension',
        string='Dimension',
        ondelete='restrict',
    )
    name = fields.Char(
        string='Dimension',
        required=True,
    )
    