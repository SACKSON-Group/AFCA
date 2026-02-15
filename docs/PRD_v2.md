# AFCA — Product Requirements Document (v2.0)

**Product:** Africa First Care Access (AFCA)  
**Tagline:** Healthcare, made accessible.  
**Version:** 2.0 (Comprehensive Edition)  
**Date:** January 30, 2026  
**Status:** Final — Approved for Development  
**Launch Markets:** Senegal, Côte d'Ivoire, Guinea

## 1) Executive Summary

AFCA is a multi-platform digital health ecosystem designed for African connectivity realities. It enables trusted care access through verified providers, adaptive telemedicine, integrated payments, e-prescriptions, pharmacy fulfillment, and privacy-preserving research.

### Core Value Propositions
- **Trust-first care:** credential verification + tamper-evident records (no PHI on-chain)
- **Universal access:** video → audio → PSTN fallback with SMS coordination
- **End-to-end care journey:** discovery to follow-up
- **Governed research:** consent-based, de-identified insights
- **Localized payments:** mobile money + cards with reconciliation

## 2) Product Scope

AFCA includes:
- **Mobile app (Flutter):** patients, doctors, pharmacists in one role-based app
- **Web admin console:** provider verification, operations, support, facility management
- **Web research platform:** data catalog, cohorting, governance workflows
- **Backend services (FastAPI):** modular domain APIs + realtime channels
- **Blockchain trust layer (Hyperledger):** proofs, consent receipts, audit anchors
- **Payment orchestration:** Wave, Orange Money, card rails
- **Telemedicine layer:** Twilio video/audio/PSTN/SMS

## 3) MVP Timeline and Targets

### Launch sequence (first 6 weeks)
1. Week 1–2: Senegal soft launch (50 providers, 5 pharmacies)
2. Week 3–4: Senegal full launch + Côte d'Ivoire soft launch
3. Week 5–6: Guinea soft launch + active multi-market acquisition

### Day-90 target
- 500+ verified providers
- 50+ pharmacies
- 10,000+ registered patients

## 4) Core User Journey (Patient)

1. Discover verified provider
2. Book appointment with mode selection
3. Receive reminders and pre-consult support
4. Attend consultation with bandwidth fallback
5. Provider completes signed clinical notes
6. Receive e-prescription
7. Select pharmacy and fulfill medication
8. Payment settlement and provider payout
9. Follow-up reminders and satisfaction capture

## 5) Technical Direction

- **Architecture:** microservice-aligned FastAPI backend
- **Data integrity:** blockchain anchors for non-PHI proofs
- **Reliability:** idempotent payment operations + reconciliation
- **Compliance:** privacy-first, auditable workflows
- **Access model:** role-based and governance-aware

## 6) Success Criteria

- High consultation completion under poor connectivity
- Strong verification confidence and patient trust
- Reliable payment settlement window (48–72h payouts)
- Ethical research access with measurable policy impact

## 7) Business and Financial Snapshot

- MVP budget: **$2.5M–$3.5M**
- Break-even projection: **18–24 months post-launch**
- Year-3 revenue target: **$15M+** at **35%+ gross margin**
- 3-year expansion: **8+ countries**, **$75M+ annual revenue target**

---

> This document is a condensed repository copy of the approved comprehensive PRD shared by Product Management.
