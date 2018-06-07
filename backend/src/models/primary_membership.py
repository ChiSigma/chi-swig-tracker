import membership


class PrimaryMembership(membership.Membership):
    __sti_type__ = 'primary'
