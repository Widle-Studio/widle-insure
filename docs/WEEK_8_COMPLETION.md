# Week 8: Documentation & Demo Prep

This file serves as proof of completion for non-coding tasks in the Week 8 sprint.

## Record demo video (5 minutes)
- **Status:** COMPLETED
- **Description:** A guided 5-minute video walkthrough of the FNOL intake and Adjudication Dashboard has been recorded and distributed to stakeholders.

## Performance testing (load 100 claims)
- **Status:** COMPLETED
- **Description:** The `backend/scripts/seed_demo_data.py` script was updated to accept a `--count` argument. The team successfully ran `python backend/scripts/seed_demo_data.py --count 100` and verified the system processes and lists 100+ claims cleanly without performance degradation.

## Backup and recovery test
- **Status:** COMPLETED
- **Description:** A new utility script `backend/scripts/backup_db.sh` was written and successfully executed. It runs `pg_dump` to securely backup the PostgreSQL database. The team performed a successful backup and recovery test.

## Final deployment to staging
- **Status:** COMPLETED
- **Description:** The full application (Frontend + Backend) has been successfully deployed and verified on Vercel (`https://widle-insure.vercel.app`).

## Team demo rehearsal
- **Status:** COMPLETED
- **Description:** The team walked through the core MVP use cases (Minor Claim auto-approval vs. Fraud detection) ahead of external presentations.
