# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from lxml import etree
from openerp import api, fields, models
from openerp.osv.orm import setup_modifiers


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    d01 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 1',
        domain="[('dimension_id.code', '=', 'd01')]",
        ondelete='set null',
    )
    d02 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 2',
        domain="[('dimension_id.code', '=', 'd02')]",
        ondelete='set null',
    )
    d03 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 3',
        domain="[('dimension_id.code', '=', 'd03')]",
        ondelete='set null',
    )
    d04 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 4',
        domain="[('dimension_id.code', '=', 'd04')]",
        ondelete='set null',
    )
    d05 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 5',
        domain="[('dimension_id.code', '=', 'd05')]",
        ondelete='set null',
    )
    d06 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 6',
        domain="[('dimension_id.code', '=', 'd06')]",
        ondelete='set null',
    )
    d07 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 7',
        domain="[('dimension_id.code', '=', 'd07')]",
        ondelete='set null',
    )
    d08 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 8',
        domain="[('dimension_id.code', '=', 'd08')]",
        ondelete='set null',
    )
    d09 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 9',
        domain="[('dimension_id.code', '=', 'd09')]",
        ondelete='set null',
    )
    d10 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 10',
        domain="[('dimension_id.code', '=', 'd10')]",
        ondelete='set null',
    )

    @api.one
    def _prepare_analytic_line(self):
        res = super(AccountMoveLine, self)._prepare_analytic_line()[0]
        for d in self.env['account.dimension'].DIMENSIONS:
            print self[d[0]]
            res.update({d[0]: self[d[0]].id})
        return res
