# This file is part of the party_partner module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Configuration']

class Configuration:
    __name__ = 'party.configuration'
    __metaclass__ = PoolMeta
    partner_sequence = fields.Property(fields.Many2One('ir.sequence',
            'Partner sequence', domain=[
                ('code', '=', 'party.party'),
                ]))
