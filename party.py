# This file is part of the party_partner module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, And, Bool, Or
from trytond.modules.party.party import STATES, DEPENDS

__all__ = ['Party']

_STATES = STATES.copy()
_STATES.update({
    'readonly': Or(~Eval('active', True), And(Eval('partner', False),
                Bool(Eval('partner_code', ''))))
    })

class Party:
    __name__ = 'party.party'
    __metaclass__ = PoolMeta

    partner = fields.Boolean('Partner', states=_STATES,
        depends=DEPENDS + ['partner', 'partner_code'])
    partner_code = fields.Char('Partner code', select=True,
        states={
            'readonly': True,
            'required': Eval('partner', False),
            }, depends=['partner'])

    @classmethod
    def create(cls, vlist):
        Sequence = Pool().get('ir.sequence')
        Configuration = Pool().get('party.configuration')

        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if values.get('partner') is True and not values.get('partner_code'):
                config = Configuration(1)
                values['partner_code'] = Sequence.get_id(config.partner_sequence.id)
        return super(Party, cls).create(vlist)

    @classmethod
    def write(cls, *args):
        Sequence = Pool().get('ir.sequence')
        Configuration = Pool().get('party.configuration')
        actions = iter(args)
        args = []
        for parties, values in zip(actions, actions):
            values = values.copy()
            if values.get('partner') == True:
                for party in parties:
                    if party.partner_code is None or party.partner_code == '':
                        config = Configuration(1)
                        values['partner_code'] = Sequence.get_id(config.partner_sequence.id)
            args.extend((parties, values))
        super(Party, cls).write(*args)


    @classmethod
    def copy(cls, parties, default=None):
        default = super(Party, cls).copy(parties, default=default)
        default['partner_code'] = None
        return default

    def get_rec_name(self, name):
        name = super(Party, self).get_rec_name(name)
        codes = []
        if self.partner and self.partner_code:
            codes.append('[' + self.partner_code + ']')
            return ''.join(codes) + name
        return name

    @classmethod
    def search_rec_name(cls, name, clause):
        domain = super(Party, cls).search_rec_name(name, clause),
        return ['OR',
                domain,
                ('partner_code',) + tuple(clause[1:]),
                ]
