import membership


class EphemeralMembership(membership.Membership):
    __sti_type__ = 'ephemeral'
