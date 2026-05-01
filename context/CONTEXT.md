# attribu.io — Business Context & Claude Memory File

> Last updated: April 2026
> Founder: Joe (joe@attribu.io)
> Co-founder: Fiancée (marketing ops background, 5+ years with BWH International property owners)

---

## Who We Are

**Joe** — Sr. Machine Learning Engineer, $300K+ TC (still employed — this is our runway).
Core skills:
- Low-latency computer vision & traditional ML (production-grade, edge deployment)
- Route optimization engineering (built at FedEx scale — real operational complexity, real constraints)
- Full-stack web dev (Django, PostgreSQL, React)
- Can deploy anything to VPS, build iOS/React Native if needed

**Fiancée** — Marketing ops & management background.
- 5+ years working directly with BWH International (Best Western Hotels) property owners
- Understands buyer language, client relationships, delivery ops
- Has warm network of hotel property owners (potential early clients in adjacent markets)

---

## The Business: AI Dispatch & Route Optimization for Field Service

**Core problem:** Field service operators (HVAC, plumbing, electrical, pest control, landscaping) route their technicians with Google Maps and a whiteboard. The difference between optimized and unoptimized routing at 30–50 technicians is $150K–$300K/year in wasted fuel and labor.

**Our solution:** ML-powered dispatch and route optimization. Not a checkbox feature like Route4Me — actual optimization engineering with real constraint handling:
- Time windows
- Skill-to-job matching (right tech, not just nearest tech)
- Dynamic rerouting when jobs run long or techs call out
- Predictive scheduling based on demand patterns
- Event-aware demand signals

**Our unfair advantage:** Joe has done this at FedEx scale. That credibility closes enterprise conversations that take a typical ML founder 12 months to earn. No competitor founder has this pedigree.

**Long-term product vision:** Add a computer vision diagnostic layer — technician uses phone/tablet camera on-site, CV model identifies equipment issue and estimates parts needed, feeds back into routing/dispatch system. This is V3, not V1.

---

## Domain & Brand

- **Domain:** attribu.io
- **Email:** joe@attribu.io
- **Brand tone:** Dark, technical, ops-center aesthetic. "Built by engineers, for operators." Not SaaS-cute. Not generic AI purple gradients.
- **Positioning:** AI dispatch & route intelligence for field service operators — built by engineers who've done this at FedEx scale.

---

## The Coming Soon Landing Page

**Live at:** attribu.io (deploy as static HTML on VPS)
**Stack:** Pure HTML/CSS/JS — no framework needed for a static page
**Design:** Dark background (#080B0F), teal accent (#00DCA0), Space Mono + Syne fonts, grid background, route SVG decoration

**Key elements:**
1. Logo: `attribu.io` with teal accent dot
2. Status pill: "Building now" with pulse dot
3. Eyebrow: "AI dispatch & route intelligence"
4. Headline: "Stop losing money on bad routing."
5. Subhead: ML-powered dispatch for field service operators, built by engineers who've done this at FedEx scale
6. **Three metrics (most important element — operators care about dollars not features):**
   - ~22% avg fuel reduction
   - +3.1 jobs / tech / day
   - $180K avg annual savings / 30 trucks
7. Email capture form → "Notify me →"
8. Built-for tags: HVAC, Plumbing, Electrical, Pest Control, Landscaping, Field Service, Last-Mile Delivery
9. Footer: © 2026 attribu.io | joe@attribu.io

**Email capture:** Hook to Formspree or a simple Django POST endpoint → save to Postgres. Every email gets a personal follow-up from joe@attribu.io within 24 hours.

**DO NOT build:**
- React Native app (not yet — dispatchers are at desks, not in the field for V1)
- Microservices or Kubernetes
- AWS/GCP (Hetzner or DigitalOcean VPS until 10+ customers)
- Anything mobile until the CV diagnostic layer is ready (V3)

---

## Go-To-Market Strategy (YC-Style)

### Phase 1: Customer Discovery (Weeks 1–2)
**Do not write a single line of code.**

Goal: 10 customer conversations with HVAC/plumbing/electrical service companies (15–100 technicians).

Find them via:
- Google Maps: search "HVAC company [city]", call the owner directly
- LinkedIn: Operations Manager, Service Manager titles
- Local trade association directories (ACCA for HVAC, etc.)
- Thumbtack/Angi vendor listings

**What to learn:**
- How do they dispatch today? (Answer: ServiceTitan, Housecall Pro, or a whiteboard)
- What does a bad dispatch day cost them concretely?
- Have they tried to solve this? What happened?
- Who makes the buying decision?
- What would make them switch?

**Rules:**
- Do NOT pitch. Do NOT mention a product. Just listen.
- Look for the same 3–4 problems coming up with emotional language
- "We're losing $X every time a tech drives across town" = green light
- "It would be nice to have better routing" = red flag (vitamin, not painkiller)

### Phase 2: Concierge MVP (Weeks 3–4)
Before building any software, offer to optimize one company's dispatch **manually**.

- Take their job data for the last 30 days
- Run optimization logic manually (spreadsheet + brain)
- Show them what their routing should have looked like
- Quantify what they left on the table

**Charge $500–$1,000 for this audit.** If they won't pay even that, the pain isn't real enough.

This validates the problem, gives intimate knowledge of real data and constraints before architecting anything, and creates the first case study.

### Phase 3: V1 Software (Weeks 5–8)
**Build the smallest thing that delivers core value:**

- Django + PostgreSQL (Joe knows this stack cold — no new frameworks)
- OR-Tools (Google's open source optimization library) for the routing engine
- Celery for async job processing
- Simple React frontend OR server-rendered Django templates for V1
- CSV upload or single API integration (ServiceTitan has an API)
- One output: recommended dispatch sequence with map view, emailed to dispatcher at 6am

Deploy on Hetzner or DigitalOcean VPS. Single monolith. Ship fast and ugly.

**It does NOT need to be pretty. It needs to save them money.**

### Phase 4: First Paying Pilot (Week 8–10)

**Pilot pricing:** $500/month for 90 days
- Low enough that owner says yes without procurement process
- Require a credit card on file BEFORE starting

**Full pricing after pilot:** $2,000–$5,000/month based on fleet size
- 30-truck fleet saving $180K/year → $3K/month is a no-brainer
- 15-truck fleet → $1,500–$2,000/month

**The ROI pitch:** "If we don't save you at least 5x our monthly fee in fuel and labor, cancel anytime."

### Phase 5: Scale (Month 3–6+)
- Iterate only on what customers ask for — nothing else
- These owners talk to each other. One reference from a trusted peer closes deals faster than any sales pitch.
- Target regional operators first, not national chains (faster decisions, more acute pain)
- When you have 3 case studies, hire or partner with a field service industry insider for distribution

---

## Revenue Model & Targets

| Milestone | Timeline | MRR |
|---|---|---|
| 3 pilot clients | Month 3 | $1,500 |
| 5 full-price clients | Month 6 | $12,500 |
| 15 clients | Month 12 | $37,500 |
| 30 clients | Month 18 | $75,000+ |

**At 20 clients × $2,500/month avg = $600K ARR.** This is achievable in 18 months with a focused vertical.

**Ceiling:** $5M–$20M ARR in this vertical before you need to think about expansion. Acquirable by ServiceTitan, Salesforce Field Service, or a PE-backed roll-up at that point.

---

## Tech Stack Decisions

| Layer | Choice | Why |
|---|---|---|
| Backend | Django + PostgreSQL | Joe knows it cold, ships fast |
| Optimization engine | Google OR-Tools | Production-grade, open source, runs in days |
| Async jobs | Celery + Redis | Dispatch recommendations, report generation |
| Frontend V1 | Django templates or simple React | Dispatchers are at desks |
| Hosting | Hetzner or DigitalOcean VPS | Cheap, fast, full control |
| Email | Formspree or custom Django endpoint | Email capture → Postgres |
| Mobile | NOT YET | Add when CV diagnostic layer is V3 |
| Cloud (AWS/GCP) | NOT YET | Add after 10+ customers |

---

## What We Are NOT Building (Yet)

- ❌ A mobile app — dispatchers are at desks, not in the field
- ❌ Microservices or Kubernetes — a monolith that works beats beautiful architecture with no customers
- ❌ AWS/GCP infrastructure — unnecessary complexity before 10 customers
- ❌ A general-purpose routing SaaS — we are vertical-specific (field service) to start
- ❌ A marketing agency — our technical edge is wasted there
- ❌ Hotel attribution software (original attribu.io idea) — too narrow, wrong buyer motion
- ❌ Generic SEO tooling — crowded, commoditized

---

## Future Product Roadmap

**V1:** Route optimization dashboard, CSV/API job import, morning dispatch email, map view
**V2:** ServiceTitan / Housecall Pro native integration, dynamic rerouting, skill-to-job matching
**V3:** Computer vision diagnostic layer — technician scans equipment on-site, CV model identifies issue and parts needed, feeds back into dispatch system
**V4:** Predictive demand forecasting, automated scheduling, cross-client benchmarking dashboard

---

## Adjacent Opportunities (Do Not Chase Yet)

- **BWH hotel network** (fiancée's connections): Potential channel for a separate product later — AI revenue management as a service for independent hotel operators ($1,500–$2,500/month). Do not pursue until field service has traction. The hotel sales cycle is long and the buyer is slow.
- **GEO (Generative Engine Optimization):** Emerging discipline for AI search visibility. Interesting but a distraction from the core business right now.
- **Boutique SEO firm acquisition:** A contact has a struggling SEO firm available. Could be interesting as a cash-flow vehicle or acqui-hire but do not let it distract from attribu.io's core focus.

---

## Cold Outreach Email Template

Subject: Route optimization for [Company Name]

> Hi [Name],
>
> My background is in route optimization engineering — I led this work at FedEx before starting attribu.io.
>
> Most [HVAC/plumbing/electrical] operators with 20–80 techs are leaving $100K–$200K/year on the table in fuel and drive time. I can show you exactly where yours is going.
>
> Would you have 20 minutes this week for a quick call?
>
> — Joe
> joe@attribu.io

Rules: 5 sentences max. No pitch deck. No website needed yet. Owners respond to directness. Always mention the FedEx pedigree — it is your single most valuable credibility signal in this market.

---

## Key Risks & Honest Cautions

1. **Scope creep:** Hotel owners and service operators will ask for custom reports and one-off favors. Productize aggressively. Resist becoming a boutique consulting firm. The money is in recurring, scalable software — not hourly work.

2. **Sales cycle length:** Even small operators take 2–6 weeks to decide. Your W2 income ($300K+ TC) is your runway. Do not quit the day job until you have $15K+ MRR.

3. **ServiceTitan dependency:** Many operators are locked into ServiceTitan. Build the API integration early. Becoming a native integration partner is a distribution strategy — pursue the ServiceTitan marketplace after V1.

4. **Technical vs. operator buyer:** Joe does technical sales here — in this market, buyers want to talk to the person who built it. That is an advantage, not a liability. Fiancée manages operations, finances, and any content/marketing support.

5. **Pricing too low:** $500/month pilots are fine to get in the door. Do not let anyone stay at pilot pricing past 90 days. The ROI justifies full price — hold the line.

---

## Notes for Future Claude Sessions

- Joe's primary technical skills: computer vision (low-latency, edge), route/dispatch optimization (FedEx-scale), Django full-stack
- Fiancée's primary skills: marketing ops management, client relationships, BWH hotel network
- Business is pre-revenue, pre-product as of April 2026
- Domain: attribu.io | Email: joe@attribu.io
- Target customer: HVAC/plumbing/electrical service companies, 15–100 technicians, regional operators
- Core stack: Django, PostgreSQL, OR-Tools, Celery, VPS (Hetzner/DO)
- Do not suggest: mobile apps, AWS, microservices, hotel software, SEO tools, or marketing agency plays
- Always pressure-test ideas against: does this play to Joe's FedEx/CV/ML pedigree? Does it have a clear ROI story for an operator? Can it be built fast and ugly first?