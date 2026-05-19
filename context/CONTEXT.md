# attribu.io — Business Context & Claude Memory File

> Last updated: May 2026
> Founder: Joe Waugh (joe@attribu.io)

---

## Who I Am

**Joe Waugh** — Sr. ML Engineer at ThredUp (current day job, ~$300K TC — this is my runway).

Core skills:
- Production ML systems (TensorFlow, Python, GCP/AWS, Spark) — shipped at FedEx and ThredUp scale
- Computer vision: image classification models deployed in logistics operations at FedEx
- Delivery prediction and process optimization: built models that reduced FedEx churn, improved EDD accuracy
- Full-stack web dev (Django, PostgreSQL, React)
- Can deploy anything to VPS, build iOS/React Native if needed
- MS Computer Science, Georgia Tech (ML specialization)

**Credibility anchor for sales:** "I spent two years as a production ML engineer at FedEx building systems that touched delivery operations at scale — fraud detection, package prediction, logistics pipelines. I know exactly where the waste is in field service routing because I've seen what it looks like at the FedEx level, and most operators don't come close to that efficiency."

Do NOT say "I led route optimization at FedEx" — that specific claim is not accurate and will fall apart under questioning. The honest framing above is still compelling.

---

## The Business: AI Dispatch & Route Optimization for Field Service

**Core problem:** Field service operators (HVAC, plumbing, electrical, pest control, landscaping) route their technicians with Google Maps and a whiteboard. The difference between optimized and unoptimized routing at 30–50 technicians is $150K–$300K/year in wasted fuel and labor.

**Our solution:** ML-powered dispatch and route optimization. Not a checkbox feature like Route4Me — actual optimization engineering with real constraint handling:
- Time windows
- Skill-to-job matching (right tech, not just nearest tech)
- Dynamic rerouting when jobs run long or techs call out
- Predictive scheduling based on demand patterns

**My unfair advantage:** Production ML pedigree at FedEx + Georgia Tech ML degree + full-stack shipping ability. I can build the product, close technical buyers, and deploy it myself. Most competitors in this space are either pure operators (no ML depth) or pure ML engineers (can't build product).

**Long-term product vision:** Add a computer vision diagnostic layer — technician uses phone/tablet camera on-site, CV model identifies equipment issue and estimates parts needed, feeds back into routing/dispatch system. This is V3, not V1.

---

## Domain & Brand

- **Domain:** attribu.io
- **Email:** joe@attribu.io
- **Brand tone:** Dark, technical, ops-center aesthetic. "Built by engineers, for operators." Not SaaS-cute.
- **Positioning:** AI dispatch & route intelligence for field service operators — built by an ML engineer who shipped production systems at FedEx.

---

## Current State (May 2026)

- Pre-revenue, pre-product
- Inbox warmup running (started May 6, ~12 days in) on joe@attribu.io — at ~10 warmup emails/day, ramping
- 400+ cold prospects loaded in Apollo, ready to send
- HubSpot CRM active with email tracking (opens, clicks) via Sales Extension
- ~16 contacts in HubSpot from initial outreach batch
- Targeting Phoenix market first (HVAC + pest control) — geographic concentration helps with personalization and word-of-mouth
- Landing page live at attribu.io (coming soon / waitlist)

---

## Go-To-Market Strategy (YC-Style)

### Phase 1: Customer Discovery (NOW — Weeks 1–4)

Inbox is warming up. Ramp cold emails via Apollo:
- Week 1-2: 10/day
- Week 3-4: 25/day
- Week 5+: 50/day

Goal: 10 conversations with HVAC/plumbing/electrical/pest control operators (15–100 techs).

**What to learn:**
- How do they dispatch today?
- What does a bad dispatch day cost them in dollars?
- Have they tried to solve this?
- Who makes the buying decision?

**Rules:**
- Do NOT pitch on the first call. Just listen.
- Look for the same 3–4 problems with emotional/dollar language
- "We waste $X every time a tech drives across town" = green light
- "It would be nice to have better routing" = red flag (vitamin, not painkiller)

### Phase 2: Free Audit → Case Study (Weeks 3–6)

Before charging, offer the first 2-3 prospects a **free routing audit**. This is strategic:
- You have zero case studies, zero social proof
- A free audit gets you real data to understand constraints before you architect anything
- It produces your first case study: "We saved [Company] $22K in one month"
- Once you have 1 case study, switch to $500–$1,000 paid audits

**Free audit scope:** Take their last 30 days of job data, run manual optimization, deliver a 2-page doc showing current vs. optimized routing with a dollar figure attached. Total work: 4-8 hours.

**After the free audit:** If savings are real, propose a 90-day pilot at $500/month. The case study sells the pilot.

### Phase 3: V1 Software (Weeks 5–8)

**Build the smallest thing that delivers core value:**
- Django + PostgreSQL
- OR-Tools for the routing engine
- Celery for async job processing
- Simple React frontend or Django templates
- CSV upload or ServiceTitan API integration
- One output: recommended dispatch sequence with map view, emailed to dispatcher at 6am

Deploy on Hetzner or DigitalOcean VPS. Single monolith. Ship fast.

### Phase 4: First Paying Pilot (Week 8–10)

**Pilot pricing:** $500/month for 90 days
- Low enough to skip procurement
- Credit card on file before starting

**Full pricing after pilot:** $2,000–$5,000/month based on fleet size

**The ROI pitch:** "If we don't save you at least 5x our monthly fee in fuel and labor, cancel anytime."

### Phase 5: Scale (Month 3–6+)

- Iterate only on what customers ask for
- Regional operators talk to each other — one reference closes deals faster than any pitch
- Target regional operators first (faster decisions, more acute pain)
- 3 case studies → start pursuing ServiceTitan marketplace integration as a distribution channel

---

## Revenue Model & Targets

| Milestone | Timeline | MRR |
|---|---|---|
| 3 pilot clients | Month 3 | $1,500 |
| 5 full-price clients | Month 6 | $12,500 |
| 15 clients | Month 12 | $37,500 |
| 30 clients | Month 18 | $75,000+ |

At 20 clients × $2,500/month avg = $600K ARR. Achievable in 18 months with focused vertical execution.

**Exit ceiling:** $5M–$20M ARR before thinking about expansion. Acquirable by ServiceTitan, Salesforce Field Service, or PE-backed roll-up.

---

## Tech Stack Decisions

| Layer | Choice | Why |
|---|---|---|
| Backend | Django + PostgreSQL | Ship fast, know it cold |
| Optimization engine | Google OR-Tools | Production-grade, open source |
| Async jobs | Celery + Redis | Nightly dispatch runs |
| Frontend V1 | Django templates | Dispatchers are at desks |
| Hosting | Hetzner or DigitalOcean VPS | Cheap, fast, full control |
| CRM | HubSpot (free tier) | Email tracking, pipeline |
| Outreach | Apollo.io | Prospect lists, sequencing |
| Email warmup | Instantly / Mailwarm | Domain reputation |
| Mobile | NOT YET | Add at V3 |
| Cloud (AWS/GCP) | NOT YET | After 10+ customers |

---

## What I Am NOT Building (Yet)

- ❌ A mobile app — dispatchers are at desks
- ❌ Microservices or Kubernetes — monolith until real load
- ❌ AWS/GCP infrastructure — unnecessary pre-10 customers
- ❌ General-purpose routing SaaS — field service vertical only
- ❌ Hotel/hospitality software — different market, different buyer motion

---

## Future Product Roadmap

**V1:** Route optimization dashboard, CSV/API job import, morning dispatch email, map view
**V2:** ServiceTitan / Housecall Pro native integration, dynamic rerouting, skill-to-job matching
**V3:** Computer vision diagnostic layer — tech scans equipment on-site, CV model identifies issue and parts needed, feeds back into dispatch
**V4:** Predictive demand forecasting, automated scheduling, cross-client benchmarking

---

## Key Risks & Cautions

1. **Free audit scope creep:** Keep free audits scoped — 30 days of data, 1 deliverable doc. Not an open-ended consulting engagement. The goal is a case study, not billable hours.

2. **Sales cycle length:** Even small operators take 2–6 weeks to decide. W2 income is runway. Do not quit until $15K+ MRR.

3. **ServiceTitan dependency:** Many operators are locked in. Build the API integration early. Pursue the ServiceTitan marketplace after V1.

4. **The FedEx claim:** Always say "production ML engineer at FedEx" — not "led route optimization at FedEx." The honest version is compelling. The stretched version is a credibility liability.

5. **Pricing:** $500/month pilots are fine to get in the door. Do not let anyone stay at pilot pricing past 90 days. The ROI justifies full price.

---

## Notes for Future Claude Sessions

- Joe's background: production ML at FedEx (fraud detection, CV, prediction), Georgia Tech MS ML, full-stack Django/React
- Business is pre-revenue, pre-product as of May 2026
- Domain: attribu.io | Email: joe@attribu.io
- Target customer: HVAC/plumbing/electrical/pest control, 15–100 technicians, regional operators (Phoenix first)
- Current tooling: Apollo (outreach), HubSpot (CRM + email tracking), inbox warmup active
- Core stack: Django, PostgreSQL, OR-Tools, Celery, VPS (Hetzner/DO)
- Do not suggest: mobile apps, AWS, microservices, "led route optimization at FedEx" claim
- Always pressure-test: does this play to Joe's ML pedigree? Does it have a clear ROI story for an operator? Can it be built fast first?
