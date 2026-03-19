# Demo Scenarios: AI-Automated Auto Insurance Claims Platform

This document details three specific scenarios designed to showcase the platform's core capabilities during client demonstrations. Each scenario highlights a different aspect of the adjudication and AI analysis engines.

---

## Scenario 1: The "Happy Path" (Straight-Through Processing)

**Objective:** Demonstrate the platform's ability to completely automate a simple claim from FNOL to payout initiation in under two minutes. This highlights speed, cost reduction, and customer satisfaction.

**Claimant Profile:**
- **Name:** John Doe
- **Policy:** Active, Full Coverage (POL-123456)
- **Incident:** Backed into a pole at low speed.

**Inputs:**
- **Incident Description:** "I accidentally backed into a low pole while parking. Minor damage to the rear bumper."
- **Photos:** 3 clear, well-lit photos showing a visible but minor dent/scratch on the rear bumper of a 2020 Honda Civic.

**Expected System Behavior:**
1.  **AI Analysis:** The Claude Vision API correctly identifies the vehicle (Honda Civic) and the damaged part (Rear Bumper). It assesses the severity as "Minor".
2.  **Cost Estimation:** The rule-based engine estimates the repair cost between $800 - $1,200 (well below the $2,000 auto-approval threshold).
3.  **Fraud Check:** The system calculates a Fraud Score of 0. The incident date is recent, the description matches the damage, and there are no other red flags.
4.  **Adjudication:** The engine automatically sets the claim status to **Approved**.
5.  **Admin Action:** The presenter logs into the Admin Dashboard, locates the newly approved claim, and clicks "Initiate Payout" to demonstrate the Stripe integration.

---

## Scenario 2: The "Human Review" (Complex Claim)

**Objective:** Show that the AI knows its limits and safely escalates complex, high-value, or ambiguous claims to a human adjuster. This highlights safety, control, and the AI's role as an "assistant" rather than a fully autonomous black box for major incidents.

**Claimant Profile:**
- **Name:** Jane Smith
- **Policy:** Active, Liability + Collision (POL-987654)
- **Incident:** Multi-vehicle collision on the highway.

**Inputs:**
- **Incident Description:** "I was rear-ended on the highway, which pushed me into the car in front of me."
- **Photos:** 5 photos showing significant front and rear-end damage to a 2019 Toyota RAV4. The photos might be slightly blurry or taken in poor lighting (e.g., at night or in the rain).

**Expected System Behavior:**
1.  **AI Analysis:** The AI identifies multiple damaged parts (Front Bumper, Hood, Grille, Rear Bumper, Trunk lid). It assesses severity as "Major".
2.  **Cost Estimation:** The engine estimates the repair cost at $6,000 - $9,000.
3.  **Adjudication:** Because the estimate exceeds the $2,000 threshold (and potentially due to lower AI confidence from the blurry photos), the system flags the claim.
4.  **Admin Action:** The claim appears in the "Human Review Queue" on the Admin Dashboard. The presenter demonstrates how the adjuster uses the AI's annotated photos and cost breakdown to quickly understand the claim, adjust the final approved amount, and manually approve it.

---

## Scenario 3: The "Fraud Alert" (Suspicious Claim)

**Objective:** Demonstrate the platform's built-in rule-based Fraud Detection Engine. This highlights the system's ability to protect the carrier's bottom line by catching common deceptive practices before a payout occurs.

**Claimant Profile:**
- **Name:** Robert Johnson
- **Policy:** Active (POL-555555)
- **Incident:** Claiming a new scratch on a door.

**Inputs:**
- **Incident Description:** "Someone keyed my car in the grocery store parking lot today."
- **Incident Date:** Today's date.
- **Photos:** 2 photos of a scratch on the side door of a 2015 Ford F-150. *Crucially, the photos contain metadata or visual cues (e.g., rust in the scratch) indicating the damage is older than claimed.*

**Expected System Behavior:**
1.  **AI Analysis:** The AI identifies the scratch. However, it also detects anomalies—such as rust formation within the scratch—suggesting the damage is not recent. It adds a "Pre-existing damage suspected" Red Flag to its analysis.
2.  **Fraud Check:** The engine evaluates the AI's Red Flag. Additionally, the system checks the claimant's history and finds a similar claim filed (and rejected) 45 days ago. The Fraud Score spikes to 85 (High Risk).
3.  **Adjudication:** The claim is immediately routed to the Human Review Queue, regardless of the estimated cost.
4.  **Admin Action:** The presenter opens the claim in the Admin Dashboard. They highlight the high Fraud Score, the specific AI-generated Red Flags (rust detected), and the claimant's history. The presenter then clicks "Reject Claim" and selects "Suspected Fraud / Pre-existing Damage" as the reason.