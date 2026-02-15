# AFCA Codebase Review & Improvement Plan

**Review Date:** February 1, 2026  
**Scope:** Backend (FastAPI), Mobile (Flutter), Web, DevOps

## Executive Summary

The architecture is strong, but production readiness depends on focused hardening in:
- Security and secrets management
- Error handling and validation
- Payments reliability and idempotency
- Test depth and coverage
- Logging, monitoring, and operability

## Priority 1 — Immediate (Week 1)

1. Tighten CORS from wildcard to explicit allowlist
2. Add auth endpoint rate limiting (OTP request/verify)
3. Replace deprecated `datetime.utcnow()` usage
4. Standardize request validation and error envelopes
5. Add structured JSON logging for API requests/responses

## Priority 2 — Short Term (Weeks 2–4)

1. Complete payment adapters (Wave / Orange Money) + webhook handling
2. Enforce idempotency keys for payment intent creation
3. Add database indexes for high-frequency query patterns
4. Build comprehensive automated tests (target ~80% coverage)
5. Introduce CI gates (lint/test/security scan)

## Priority 3 — Medium Term (Weeks 5–8)

1. Add APM + tracing (e.g., Sentry)
2. Introduce async job processing (Celery/Redis)
3. Implement caching strategy for hot endpoints
4. Expand mobile offline queue/sync reliability
5. Complete web admin/research interfaces

## Key Implementation Recommendations

### Security
- Move secrets from plain env to managed secret store in production
- Shorten access token expiry and rotate signing secrets
- Add brute-force protections and audit logs for auth flows

### Data & API Reliability
- Standard error format with machine-readable `error_code`
- Validate phone/email with strict schemas and cross-field checks
- Ensure payment operations are idempotent and replay-safe

### Observability
- Structured logs with request IDs and latency fields
- Alerting on elevated error rate, latency, and payment failures
- Telemetry dashboards for OTP funnel, booking completion, payout lag

## Suggested 8–12 Week Outcome

By following the phased plan, AFCA can move from strong prototype architecture to launch-grade product readiness across security, compliance posture, and operational resilience.
