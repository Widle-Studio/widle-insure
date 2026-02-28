import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.adjudication_service import AdjudicationService

class TestAdjudicationService(unittest.TestCase):

    def setUp(self):
        self.valid_policy = {
            "status": "Active",
            "coverage_limit": 50000.0,
            "deductible": 500.0
        }
        self.valid_claim = {
            "estimated_damage_cost": 1500.0
        }
        self.valid_ai_analysis = {
            "confidence": 0.95,
            "red_flags": []
        }
        self.valid_fraud_score = 5

    def test_auto_approve_valid_claim(self):
        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            self.valid_ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Approved")

    def test_reject_inactive_policy(self):
        policy = self.valid_policy.copy()
        policy["status"] = "Expired"
        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            policy,
            self.valid_ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Rejected")
        self.assertIn("Policy is not active.", result["reason"])

    def test_review_high_cost(self):
        claim = self.valid_claim.copy()
        claim["estimated_damage_cost"] = 2500.0 # Above the $2000 limit
        result = AdjudicationService.evaluate_claim(
            claim,
            self.valid_policy,
            self.valid_ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("exceeds auto-approval limit", result["reason"])

    def test_review_high_fraud_score(self):
        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            self.valid_ai_analysis,
            15 # Above the 10 limit
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("Fraud score (15.0) exceeds acceptable limit", result["reason"])

    def test_review_ai_red_flags(self):
        ai_analysis = self.valid_ai_analysis.copy()
        ai_analysis["red_flags"] = ["Possible pre-existing damage"]
        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("AI identified red flags", result["reason"])

    def test_review_low_ai_confidence(self):
        ai_analysis = self.valid_ai_analysis.copy()
        ai_analysis["confidence"] = 0.85 # Below the 0.90 limit
        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("AI confidence (0.85) is below required threshold", result["reason"])

    def test_review_exceeds_coverage(self):
        claim = self.valid_claim.copy()
        claim["estimated_damage_cost"] = 1500.0
        policy = self.valid_policy.copy()
        policy["coverage_limit"] = 1000.0
        policy["deductible"] = 0.0
        # Wait, coverage_limit 1000, deductible 0 => max is 1000. 1500 > 1000. This should review.
        result = AdjudicationService.evaluate_claim(
            claim,
            policy,
            self.valid_ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("exceeds coverage limit minus deductible", result["reason"])

    def test_handles_explicit_none_values(self):
        # Even if values are explicit None, the service should not crash
        claim = { "estimated_damage_cost": None }
        policy = { "status": None, "coverage_limit": None, "deductible": None }
        ai_analysis = { "confidence": None, "red_flags": None }
        fraud_score = None

        # Policy is None, so it should be rejected
        result = AdjudicationService.evaluate_claim(
            claim,
            policy,
            ai_analysis,
            fraud_score
        )
        self.assertEqual(result["status"], "Rejected")

        # Now pass policy, but others are None
        policy["status"] = "ACTIVE"
        result2 = AdjudicationService.evaluate_claim(
            claim,
            policy,
            ai_analysis,
            fraud_score
        )
        self.assertEqual(result2["status"], "Manual Review")
        self.assertIn("AI confidence (0.0)", result2["reason"])

if __name__ == '__main__':
    unittest.main()
