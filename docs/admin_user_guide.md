# Admin User Guide

Welcome to the Admin Dashboard for the AI-Automated Auto Insurance Claims Platform. This guide will help you navigate and utilize the core features of the system.

## Logging In

1. Navigate to the Admin Portal URL (e.g., `https://admin.your-insurance-platform.com`).
2. Enter your administrative credentials (Email and Password).
3. Upon successful authentication, you will be redirected to the **Claims Dashboard**.

## Dashboard Overview

The main dashboard provides a high-level view of your claims processing pipeline.
- **Analytics Cards:** View key metrics such as Total Claims, Straight-Through Processing (STP) Rate, and Average Cost.
- **Recent Claims Table:** A sortable, filterable list of all claims currently in the system.

## Managing Claims

### 1. The Claims Table
The table lists all claims. You can filter by:
- **Status:** Pending, Processing, Approved, Rejected, Paid.
- **Date Range:** Filter by the date the claim was submitted.
- **Amount:** Filter by estimated damage cost.

### 2. Reviewing a Claim (Human Review Queue)
Claims that fall outside the auto-adjudication rules (e.g., damage > $2,000, low AI confidence, or flagged for fraud) will be placed in the **Human Review Queue**.

To review a claim:
1. Click on the **Claim ID** in the table to open the Detailed View.
2. **Review Claimant Info:** Verify the policyholder details and incident description.
3. **Review Photos:** Examine the uploaded photos of the vehicle damage.
4. **AI Analysis Results:** Review the AI's assessment, including the estimated cost, identified damaged parts, confidence score, and any generated "Red Flags".
5. **Fraud Indicators:** Check the fraud score section. High scores indicate potential issues (e.g., mismatched locations, delayed reporting).

### 3. Approving or Rejecting
At the bottom of the Detailed View, you will find action buttons:
- **Approve Claim:** Approves the claim for the estimated amount. This will move the claim to the 'Approved' status and prepare it for payout.
- **Reject Claim:** Denies the claim. You must provide a reason for the rejection, which will be logged in the audit trail and sent to the claimant.
- **Edit Amount:** If you disagree with the AI's estimate, you can manually override the approved amount before clicking 'Approve'.

## Payouts

For Approved claims, you can initiate a payment via Stripe.
1. Navigate to an Approved claim.
2. Click the **"Initiate Payout"** button.
3. Confirm the amount and claimant banking details in the resulting modal.
4. Once initiated, the claim status changes to 'Paid', and the claimant receives an email notification.

## Audit Logs

Every action taken on a claim (submission, AI analysis, status changes, approval/rejection) is permanently recorded in the `claim_audit_log`. This log is visible at the very bottom of the Claim Detail View for transparency and compliance.