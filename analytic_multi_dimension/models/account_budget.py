# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from lxml import etree
from openerp import api, fields, models
from openerp.osv.orm import setup_modifiers


class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    dimension_group_id = fields.Many2one(
        'account.dimension.group',
        string='Dimension Group',
    )
    # Active Flag
    d1_active = fields.Boolean(compute='_compute_dimension_active')
    d2_active = fields.Boolean(compute='_compute_dimension_active')
    d3_active = fields.Boolean(compute='_compute_dimension_active')
    d4_active = fields.Boolean(compute='_compute_dimension_active')
    d5_active = fields.Boolean(compute='_compute_dimension_active')
    d6_active = fields.Boolean(compute='_compute_dimension_active')
    d7_active = fields.Boolean(compute='_compute_dimension_active')
    d8_active = fields.Boolean(compute='_compute_dimension_active')
    d9_active = fields.Boolean(compute='_compute_dimension_active')
    d10_active = fields.Boolean(compute='_compute_dimension_active')
    # --
    d1 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 1',
        domain="[('dimension_id.code', '=', 'd1')]",
        ondelete='set null',
    )
    d2 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 2',
        domain="[('dimension_id.code', '=', 'd2')]",
        ondelete='set null',
    )
    d3 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 3',
        domain="[('dimension_id.code', '=', 'd3')]",
        ondelete='set null',
    )
    d4 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 4',
        domain="[('dimension_id.code', '=', 'd4')]",
        ondelete='set null',
    )
    d5 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 5',
        domain="[('dimension_id.code', '=', 'd5')]",
        ondelete='set null',
    )
    d6 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 6',
        domain="[('dimension_id.code', '=', 'd6')]",
        ondelete='set null',
    )
    d7 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 7',
        domain="[('dimension_id.code', '=', 'd7')]",
        ondelete='set null',
    )
    d8 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 8',
        domain="[('dimension_id.code', '=', 'd8')]",
        ondelete='set null',
    )
    d9 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 9',
        domain="[('dimension_id.code', '=', 'd9')]",
        ondelete='set null',
    )
    d10 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 10',
        domain="[('dimension_id.code', '=', 'd10')]",
        ondelete='set null',
    )
    _sql_constraints = [
        ('dimension_uniq',
         'unique(creating_user_id, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10)',
         'Analytic Account Dimensions must be unique!'),
    ]

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(CrossoveredBudget, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
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
        print result
        return result

    @api.multi
    @api.depends('dimension_group_id')
    def _compute_dimension_active(self):
        for analytic in self:
            codes = [(line.dimension_id.code, line.dimension_id.name) for
                     line in analytic.dimension_group_id.dimension_ids]
            for d in self.env['account.dimension'].DIMENSIONS:
                analytic[d[0] + '_active'] = False
            for d in codes:
                analytic[d[0] + '_active'] = True
