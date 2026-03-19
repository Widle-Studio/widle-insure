# Frequently Asked Questions (FAQ)

Welcome to the AI-Automated Auto Insurance Claims Platform FAQ. Here you can find answers to common questions about using our system.

## General Questions

**1. What is the AI-Automated Auto Insurance Claims Platform?**
It is a modern web application designed to streamline the First Notice of Loss (FNOL) process for auto insurance claims. By utilizing advanced AI (Computer Vision and Large Language Models), the platform can automatically assess vehicle damage from uploaded photos, estimate repair costs, and even auto-approve simple claims in minutes, significantly reducing processing time compared to traditional manual methods.

**2. Who is this platform for?**
This platform is primarily designed for mid-size auto insurance carriers and Managing General Agents (MGAs) looking to modernize their claims intake and adjudication processes, reduce operational costs, and improve customer experience. It provides tools for both policyholders (claimants) to submit claims and claims adjusters (admins) to manage and review them.

## For Claimants (Policyholders)

**1. How long does the FNOL process take?**
The initial online submission process is designed to take less than 5 minutes. You simply provide your details, describe the incident, and upload photos of the damage.

**2. What happens after I submit a claim?**
Our AI immediately begins analyzing the information and photos you provided.
- **Simple Claims:** If the damage is minor, the photos are clear, and your policy is active, the AI may auto-approve your claim and provide an estimated repair cost almost instantly.
- **Complex Claims:** If the damage is extensive, photos are unclear, or there are inconsistencies, your claim will be flagged for review by a human adjuster.

**3. How will I know the status of my claim?**
You will receive email notifications at key stages of the process: when your claim is received, when it's approved or rejected, and when a payout is initiated. You can also use the Claimant Portal (using the Claim Number provided in your confirmation email) to check the status at any time.

**4. What kind of photos should I upload?**
For the AI to accurately assess the damage, please upload clear, well-lit photos. We recommend taking photos from multiple angles: wide shots showing the entire vehicle and close-ups of the specific damage. Ensure the photos are in JPEG or PNG format.

## For Claims Adjusters (Admins)

**1. How does the AI assess damage?**
The platform utilizes advanced Computer Vision models (like Claude Vision) to analyze the uploaded photos. It identifies the vehicle parts, detects the type and severity of damage (e.g., scratches, dents, broken glass), and calculates an estimated repair cost based on predefined rules and market data.

**2. What does "Straight-Through Processing" (STP) mean?**
STP refers to claims that are processed from start to finish—submission, assessment, approval, and payout initiation—entirely automatically, without human intervention. Our goal is to achieve an STP rate of 70-80% for simple claims.

**3. Why would a claim be flagged for human review?**
The Adjudication Engine uses strict rules to ensure accuracy and prevent fraud. Claims are routed to the human review queue if they meet certain criteria, such as:
- The estimated damage exceeds a predefined threshold (e.g., $2000).
- The AI confidence score is low (e.g., blurry or unclear photos).
- The Fraud Detection Engine identifies potential red flags (e.g., delayed reporting, mismatched locations, pre-existing damage).
- The policy information is incomplete or requires verification.

**4. How does the Fraud Detection Engine work?**
The engine uses rule-based logic to calculate a "Fraud Score" for each claim. It looks for common fraud patterns, such as claims submitted long after the incident date, multiple recent claims on the same policy, or inconsistencies between the incident description and the photo evidence. A high fraud score automatically routes the claim for human review.

**5. How are payouts handled?**
Once a claim is approved (either automatically or by an adjuster), you can initiate a payout directly from the Admin Dashboard. The platform integrates with Stripe to securely transfer the approved funds to the claimant's bank account.