# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from lxml import etree
from openerp import api, fields, models
from openerp.osv.orm import setup_modifiers


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

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
    d6 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 6',
        domain="[('dimension_id.code', '=', 'd06')]",
        ondelete='set null',
    )
    d07 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 7',
        domain="[('dimension_id.code', '=', 'd7')]",
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


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    dimension_group_id = fields.Many2one(
        'account.dimension.group',
        string='Dimension Group',
    )
    # Active Flag
    d01_active = fields.Boolean(compute='_compute_dimension_active')
    d02_active = fields.Boolean(compute='_compute_dimension_active')
    d03_active = fields.Boolean(compute='_compute_dimension_active')
    d04_active = fields.Boolean(compute='_compute_dimension_active')
    d05_active = fields.Boolean(compute='_compute_dimension_active')
    d06_active = fields.Boolean(compute='_compute_dimension_active')
    d07_active = fields.Boolean(compute='_compute_dimension_active')
    d08_active = fields.Boolean(compute='_compute_dimension_active')
    d09_active = fields.Boolean(compute='_compute_dimension_active')
    d10_active = fields.Boolean(compute='_compute_dimension_active')
    # --
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
    activity_id = fields.Many2one(
        'account.activity',
        string='Activity',
        ondelete='set null',
    )
    _sql_constraints = [
        ('dimension_uniq',
         'unique(d01, d02, d03, d04, d05, d06, d07, d08, d09, d10,'
         'activity_id)',
         'Analytic Account Dimensions must be unique!'),
    ]

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(AccountAnalyticAccount, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(result['arch'])
        dimensions = [(x.code, x.name) for x in
                      self.env['account.dimension'].search([])]
        for d in dimensions:
            nodes = doc.xpath("//field[@name='%s']" % d[0])
            if nodes:
                node = nodes[0]
                node.set('string', d[1])
                setup_modifiers(node, result['fields'][d[0]])
        result['arch'] = etree.tostring(doc)
        return result

    @api.onchange('dimension_group_id')
    def onchange_dimension_group_id(self):
        for d in self.env['account.dimension'].DIMENSIONS:
            self[d[0]] = False

    @api.multi
    @api.depends('dimension_group_id')
    def _compute_dimension_active(self):
        for rec in self:
            codes = [(line.dimension_id.code, line.dimension_id.name) for
                     line in rec.dimension_group_id.dimension_ids]
            for d in self.env['account.dimension'].DIMENSIONS:
                rec[d[0] + '_active'] = False
            for d in codes:
                rec[d[0] + '_active'] = True
