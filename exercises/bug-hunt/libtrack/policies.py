"""Lending policy configuration for the membership categories.

Every member gets the branch-wide defaults; the ``student`` and
``faculty`` categories adjust a handful of values on top of those.
"""

from typing import Dict, Optional

from .models import Member

Policy = Dict[str, int]

DEFAULT_POLICY: Policy = {
    "loan_days": 21,
    "max_active_loans": 5,
    "renewal_limit": 2,
    "grace_days": 2,
    "daily_fine_cents": 25,
    "max_fine_cents": 1000,
}

CATEGORY_OVERRIDES: Dict[str, Policy] = {
    "student": {
        "loan_days": 28,
        "max_active_loans": 8,
    },
    "faculty": {
        "loan_days": 42,
        "renewal_limit": 4,
        "daily_fine_cents": 0,
        "max_fine_cents": 0,
    },
}


class PolicyEngine:
    """Resolves the effective lending policy for a member."""

    def __init__(self, base_policy: Optional[Policy] = None) -> None:
        self._base = dict(base_policy or DEFAULT_POLICY)

    def policy_for(self, member: Member) -> Policy:
        """Return the effective policy values for ``member``."""
        # Copy so category overrides never leak into the shared base policy.
        policy = dict(self._base)
        overrides = CATEGORY_OVERRIDES.get(member.category)
        if overrides:
            policy.update(overrides)
        return policy
