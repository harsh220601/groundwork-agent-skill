import unittest

from libtrack.models import Member
from libtrack.policies import DEFAULT_POLICY, PolicyEngine


class PolicyEngineTest(unittest.TestCase):
    def setUp(self):
        self.engine = PolicyEngine()

    def test_regular_member_gets_defaults(self):
        policy = self.engine.policy_for(Member("M-1", "Ada", category="regular"))
        self.assertEqual(policy["loan_days"], 21)
        self.assertEqual(policy["max_active_loans"], 5)
        self.assertEqual(policy["renewal_limit"], 2)
        self.assertEqual(policy["daily_fine_cents"], 25)
        self.assertEqual(policy["max_fine_cents"], 1000)

    def test_student_overrides(self):
        policy = self.engine.policy_for(Member("M-2", "Ben", category="student"))
        self.assertEqual(policy["loan_days"], 28)
        self.assertEqual(policy["max_active_loans"], 8)
        # Everything else is inherited from the defaults.
        self.assertEqual(policy["renewal_limit"], 2)
        self.assertEqual(policy["daily_fine_cents"], 25)

    def test_faculty_overrides(self):
        policy = self.engine.policy_for(Member("M-3", "Prof. Cho", category="faculty"))
        self.assertEqual(policy["loan_days"], 42)
        self.assertEqual(policy["renewal_limit"], 4)
        self.assertEqual(policy["daily_fine_cents"], 0)
        self.assertEqual(policy["max_fine_cents"], 0)
        self.assertEqual(policy["max_active_loans"], 5)

    def test_unknown_category_falls_back_to_defaults(self):
        policy = self.engine.policy_for(Member("M-4", "Dee", category="visitor"))
        self.assertEqual(policy["loan_days"], 21)

    def test_custom_base_policy(self):
        base = {
            "loan_days": 7,
            "max_active_loans": 1,
            "renewal_limit": 0,
            "grace_days": 0,
            "daily_fine_cents": 100,
            "max_fine_cents": 500,
        }
        engine = PolicyEngine(base_policy=base)
        policy = engine.policy_for(Member("M-5", "Eve", category="regular"))
        self.assertEqual(policy["loan_days"], 7)
        self.assertEqual(policy["daily_fine_cents"], 100)

    def test_module_defaults_are_not_modified(self):
        self.engine.policy_for(Member("M-6", "Prof. Fox", category="faculty"))
        self.assertEqual(DEFAULT_POLICY["loan_days"], 21)
        self.assertEqual(DEFAULT_POLICY["daily_fine_cents"], 25)


if __name__ == "__main__":
    unittest.main()
