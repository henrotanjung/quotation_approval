
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

import logging
_logger = logging.getLogger(__name__)


from werkzeug.urls import url_encode

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    state = fields.Selection(
        selection_add=[('first_approval', 'Waiting 1st Approval'), ('second_approval', 'Waiting 2nd Approval'), ('reject', 'Reject')],
    )
    
    reject_reason = fields.Text(string='Reject Reason')
    
    # is_approver = fields.Boolean(compute="_get_approver")
    
    # is_first_approver = fields.Boolean(compute="_get_first_approver")
    # is_second_approver = fields.Boolean(compute="_get_second_approver")
    
    
    def action_confirm(self):
        
        approver = self._get_approver()
        
        if approver and approver.level != 'first_approval':
            raise Exception("You don't have access to confirm this quotation")
        
        self.write({'state': 'first_approval'})
        
    
    def approve_quotaton(self):
        approver = self._get_approver()
        if self.state == 'first_approval':
            if not approver or approver.level != 'first_approval':
                raise UserError(_("You don't have access to approve this quotation"))
            self.write({'state': 'second_approval'})
            return
            
        elif self.state == 'second_approval':
            
            if not approver or approver.level != 'second_approval':
                raise UserError(_("You don't have access to approve this quotation"))
            
            res = super(SaleOrder, self).action_confirm()
        
            return res
    
    def action_reject_quotation(self):
        
        action = self.env.ref('quotation_approval.action_view_reject_quotation').read()[0]
        return action
        
        # return {
        #     'name': _('Confirmation'),
        #     'view_mode': 'form',
        #     'res_model': 'reject.quotation.wizard',
        #     'views': [(self.env.ref('quotation_approval.action_view_reject_quotation').id, 'form')],
        #     'type': 'ir.actions.act_window',
        #     'res_id': self.id,
        #     'target': 'new',
        #     'context': self.env.context,
        # }
    
    def _get_approver(self):
        emp_obj = self.env['hr.employee']
        emp = emp_obj.search([('user_id', '=', self.env.uid)])
        sale_order_approval_obj = self.env['sale.order.approval']
        emp_cur_login_id = self.env.uid
        approver = sale_order_approval_obj.search([('approver_id', '=', emp.id)])
        
        return approver
    
class SaleOrderApproval(models.Model):
    _name = 'sale.order.approval'
    
    name = fields.Char()
    level = fields.Selection([('first_approval', '1st Approval'), ('second_approval', '2nd Approval'), ('third approval', 'Third Approval')])
    approver_id = fields.Many2one('hr.employee', string='Approver')
    
    