# This file is part of the party_partner module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import party
from . import configuration


def register():
    Pool.register(
        party.Party,
        configuration.Configuration,
        module='party_partner', type_='model')
