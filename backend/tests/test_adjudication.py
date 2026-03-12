import os
import sys
import unittest

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

    def test_auto_approve_exact_boundaries(self):
        # Claim with values exactly at the boundary of acceptable limits
        claim = self.valid_claim.copy()
        claim["estimated_damage_cost"] = AdjudicationService.MAX_AUTO_APPROVE_AMOUNT

        policy = self.valid_policy.copy()
        policy["coverage_limit"] = AdjudicationService.MAX_AUTO_APPROVE_AMOUNT
        policy["deductible"] = 0.0

        ai_analysis = self.valid_ai_analysis.copy()
        ai_analysis["confidence"] = AdjudicationService.REQUIRED_AI_CONFIDENCE

        fraud_score = AdjudicationService.MAX_FRAUD_SCORE

        result = AdjudicationService.evaluate_claim(
            claim,
            policy,
            ai_analysis,
            fraud_score
        )
        self.assertEqual(result["status"], "Approved")

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

    def test_safe_float_invalid_types(self):
        # Testing TypeError (list) and ValueError (invalid string)
        claim = { "estimated_damage_cost": [] }
        policy = self.valid_policy.copy()
        ai_analysis = { "confidence": "invalid_string", "red_flags": [] }
        fraud_score = {}

        result = AdjudicationService.evaluate_claim(
            claim,
            policy,
            ai_analysis,
            fraud_score
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("AI confidence (0.0) is below required threshold", result["reason"])

    def test_review_cost_barely_exceeds(self):
        claim = self.valid_claim.copy()
        claim["estimated_damage_cost"] = AdjudicationService.MAX_AUTO_APPROVE_AMOUNT + 0.01

        result = AdjudicationService.evaluate_claim(
            claim,
            self.valid_policy,
            self.valid_ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("exceeds auto-approval limit", result["reason"])

    def test_review_confidence_barely_below(self):
        ai_analysis = self.valid_ai_analysis.copy()
        ai_analysis["confidence"] = AdjudicationService.REQUIRED_AI_CONFIDENCE - 0.001

        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("is below required threshold", result["reason"])

    def test_review_fraud_score_barely_exceeds(self):
        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            self.valid_ai_analysis,
            AdjudicationService.MAX_FRAUD_SCORE + 0.01
        )
        self.assertEqual(result["status"], "Manual Review")
        self.assertIn("exceeds acceptable limit", result["reason"])

    def test_exact_2000_cost(self):
        claim = self.valid_claim.copy()
        claim["estimated_damage_cost"] = 2000.00

        result = AdjudicationService.evaluate_claim(
            claim,
            self.valid_policy,
            self.valid_ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Approved")

    def test_exact_090_confidence(self):
        ai_analysis = self.valid_ai_analysis.copy()
        ai_analysis["confidence"] = 0.90

        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Approved")

    def test_exact_10_fraud_score(self):
        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            self.valid_ai_analysis,
            10
        )
        self.assertEqual(result["status"], "Approved")

    def test_boundary_max_auto_approve_amount(self):
        claim = self.valid_claim.copy()
        # Test exact $2000 cost boundary (MAX_AUTO_APPROVE_AMOUNT)
        claim["estimated_damage_cost"] = AdjudicationService.MAX_AUTO_APPROVE_AMOUNT

        result = AdjudicationService.evaluate_claim(
            claim,
            self.valid_policy,
            self.valid_ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Approved")

    def test_boundary_required_ai_confidence(self):
        ai_analysis = self.valid_ai_analysis.copy()
        # Test exact 0.90 AI confidence boundary (REQUIRED_AI_CONFIDENCE)
        ai_analysis["confidence"] = AdjudicationService.REQUIRED_AI_CONFIDENCE

        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            ai_analysis,
            self.valid_fraud_score
        )
        self.assertEqual(result["status"], "Approved")

    def test_boundary_max_fraud_score(self):
        # Test exact 10 fraud score boundary (MAX_FRAUD_SCORE)
        result = AdjudicationService.evaluate_claim(
            self.valid_claim,
            self.valid_policy,
            self.valid_ai_analysis,
            AdjudicationService.MAX_FRAUD_SCORE
        )
        self.assertEqual(result["status"], "Approved")


if __name__ == '__main__':
    unittest.main()
