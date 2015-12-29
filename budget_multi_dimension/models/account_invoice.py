# -*- coding: utf-8 -*-
import itertools
from lxml import etree
from openerp.osv.orm import setup_modifiers
from openerp import api, fields, models, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from samba.netcmd import domain


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

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

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        for line in self.invoice_line_ids:
            for move_line_dict in res:
                if move_line_dict.get('invl_id') == line.id:
                    for d in self.env['account.dimension'].DIMENSIONS:
                        move_line_dict.update({d[0]: line[d[0]].id})
                    break
        return res

    @api.model
    def line_get_convert(self, line, part):
        res = super(AccountInvoice, self).line_get_convert(line, part)
        for d in self.env['account.dimension'].DIMENSIONS:
            res.update({d[0]: line.get(d[0], False)})
        return res
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
        invisible=True,
        ondelete='set null',
        default=lambda self: self._context.get('d01'),
    )
    d02 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 2',
        domain="[('dimension_id.code', '=', 'd02')]",
        ondelete='set null',
        default=lambda self: self._context.get('d02'),
    )
    d03 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 3',
        domain="[('dimension_id.code', '=', 'd03')]",
        ondelete='set null',
        default=lambda self: self._context.get('d03'),
    )
    d04 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 4',
        domain="[('dimension_id.code', '=', 'd04')]",
        ondelete='set null',
        default=lambda self: self._context.get('d04'),
    )
    d05 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 5',
        domain="[('dimension_id.code', '=', 'd05')]",
        ondelete='set null',
        default=lambda self: self._context.get('d05'),
    )
    d06 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 6',
        domain="[('dimension_id.code', '=', 'd06')]",
        ondelete='set null',
        default=lambda self: self._context.get('d06'),
    )
    d07 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 7',
        domain="[('dimension_id.code', '=', 'd07')]",
        ondelete='set null',
        default=lambda self: self._context.get('d07'),
    )
    d08 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 8',
        domain="[('dimension_id.code', '=', 'd08')]",
        ondelete='set null',
        default=lambda self: self._context.get('d08'),
    )
    d09 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 9',
        domain="[('dimension_id.code', '=', 'd09')]",
        ondelete='set null',
        default=lambda self: self._context.get('d09'),
    )
    d10 = fields.Many2one(
        'account.dimension.item',
        string='Dimension 10',
        domain="[('dimension_id.code', '=', 'd10')]",
        ondelete='set null',
        default=lambda self: self._context.get('d10'),
    )
    # --
    budget_post_id = fields.Many2one(
        'account.budget.post',
        string='Budgetary Position',
    )
    activity_id = fields.Many2one(
        'account.activity',
        string='Activity',
        domain="[('budget_post_id', '=', budget_post_id)]",
    )

    @api.multi
    def _get_analytic_line(self):
        res = super(AccountInvoiceLine, self)._get_analytic_line()
        for d in self.env['account.dimension'].DIMENSIONS:
            res.update({d[0]: self[d[0]].id})
        return res

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

    @api.onchange('activity_id')
    def _onchange_activity_id(self):
        """ Set Analytic and Account """
        Analytic = self.env['account.analytic.account']
        analytic = Analytic.get_analytic_by_full_dimension(self)
        if analytic:
            analytic.ensure_one()
            self.account_analytic_id = analytic[0]
            self.account_id = self.activity_id.account_id
        else:
            self.account_analytic_id = False
            self.account_id = False

