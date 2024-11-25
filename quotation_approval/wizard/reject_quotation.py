# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class SaleAdvancePaymentInv(models.TransientModel):
    _name = "reject.quotation.wizard"
    _description = "Reject quotation"
    
    name = fields.Char(string='Reason')
    
    
    def action_archive(self):

        return {
            'name': _('Confirmation'),
            'view_mode': 'form',
            'res_model': 'reject.quotation.wizard',
            'views': [(self.env.ref('quotation_approval.action_view_reject_quotation').id, 'form')],
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context,
        }
        
    def submit_reject(self):
        _logger.info("sale orderrrrrrrrrrrrrrr id active")
        _logger.info(self._context.get('active_ids', []))
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for order in sale_orders:
            order.write({'reject_reason': self.name, 'state' : 'reject'})