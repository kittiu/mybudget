# -*- coding: utf-8 -*-
import itertools
from lxml import etree
from openerp.osv.orm import setup_modifiers
from openerp import api, fields, models, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

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

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(AccountInvoice, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
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

# 
#     @api.model
#     def fields_view_get(self, view_id=None, view_type=False, toolbar=False, submenu=False):
#         def get_view_id(xid, name):
#             try:
#                 return self.env.ref('account.' + xid)
#             except ValueError:
#                 view = self.env['ir.ui.view'].search([('name', '=', name)], limit=1)
#                 if not view:
#                     return False
#                 return view.id
# 
#         context = self._context
#         if context.get('active_model') == 'res.partner' and context.get('active_ids'):
#             partner = self.env['res.partner'].browse(context['active_ids'])[0]
#             if not view_type:
#                 view_id = get_view_id('invoice_tree', 'account.invoice.tree')
#                 view_type = 'tree'
#             elif view_type == 'form':
#                 if partner.supplier and not partner.customer:
#                     view_id = get_view_id('invoice_supplier_form', 'account.invoice.supplier.form').id
#                 elif partner.customer and not partner.supplier:
#                     view_id = get_view_id('invoice_form', 'account.invoice.form').id
#         return super(AccountInvoice, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
# #
# 
#     @api.model
#     def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
#         result = super(AccountInvoice, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
#         doc = etree.XML(result['arch'])
#         dimensions = [(x.code, x.name) for x in
#                       self.env['account.dimension'].search([])]
#         for d in dimensions:
#             nodes = doc.xpath("//field[@name='d1']")
#             if nodes:
#                 node = nodes[0]
#                 node.set('string', d[1])
#                 node.set('invisible', False)
#                 setup_modifiers(node, result['fields'][d[0]])
#         result['arch'] = etree.tostring(doc)
#         print result
#         return result


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

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
        invisible=True,
        ondelete='set null',
        default=lambda self: self._context.get('d1'),
    )
    d2 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 2',
        domain="[('dimension_id.code', '=', 'd2')]",
        ondelete='set null',
        default=lambda self: self._context.get('d2'),
    )
    d3 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 3',
        domain="[('dimension_id.code', '=', 'd3')]",
        ondelete='set null',
        default=lambda self: self._context.get('d3'),
    )
    d4 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 4',
        domain="[('dimension_id.code', '=', 'd4')]",
        ondelete='set null',
        default=lambda self: self._context.get('d4'),
    )
    d5 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 5',
        domain="[('dimension_id.code', '=', 'd5')]",
        ondelete='set null',
        default=lambda self: self._context.get('d5'),
    )
    d6 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 6',
        domain="[('dimension_id.code', '=', 'd6')]",
        ondelete='set null',
        default=lambda self: self._context.get('d6'),
    )
    d7 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 7',
        domain="[('dimension_id.code', '=', 'd7')]",
        ondelete='set null',
        default=lambda self: self._context.get('d7'),
    )
    d8 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 8',
        domain="[('dimension_id.code', '=', 'd8')]",
        ondelete='set null',
        default=lambda self: self._context.get('d8'),
    )
    d9 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 9',
        domain="[('dimension_id.code', '=', 'd9')]",
        ondelete='set null',
        default=lambda self: self._context.get('d9'),
    )
    d10 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 10',
        domain="[('dimension_id.code', '=', 'd10')]",
        ondelete='set null',
        default=lambda self: self._context.get('d10'),
    )

    @api.multi
    @api.depends('invoice_id.dimension_group_id')
    def _compute_dimension_active(self):
        for rec in self:
            codes = [(line.dimension_id.code, line.dimension_id.name) for
                     line in rec.invoice_id.dimension_group_id.dimension_ids]
            for d in self.env['account.dimension'].DIMENSIONS:
                rec[d[0] + '_active'] = False
            for d in codes:
                rec[d[0] + '_active'] = True

    @api.onchange('account_analytic_id')
    def _onchange_account_analytic_id(self):
        activity = self.account_analytic_id.activity_id
        accounts = activity.budget_post_id.account_ids
        self.account_id = accounts and accounts[0].id or False
        return

