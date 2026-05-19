# SALES.md — GTM Playbook for attribu.io

> Solo founder, pre-revenue, pre-product
> Current setup: Apollo outreach, HubSpot CRM, inbox warmup active since May 6
> Goal: 10 discovery calls → 2-3 free audits → 1 case study → paid pilot
> Last updated: May 2026

---

## The Core Loop

```
Apollo → Research → Email → HubSpot → Follow-up → Call → Discovery → Free Audit → Case Study → Paid Pilot
```

---

## Current Tooling Stack

| Tool | Purpose |
|------|---------|
| **Apollo.io** | Prospect lists, email sequences, 400+ contacts loaded |
| **HubSpot** | CRM, pipeline, email open/click tracking via Sales Extension |
| **Inbox warmup** | Domain reputation (started May 6 — ~12 days in at ~10/day) |
| **Gmail (joe@attribu.io)** | Sending via Google Workspace |
| **Calendly** | Booking discovery calls (link in email signature) |
| **Google Sheets** | Manual optimization work (pre-software) |
| **Stripe** | Payment collection for paid audits and pilots |

---

## Phase 1: Inbox Warmup & Volume Ramp

You're 12 days into warmup. Here's the ramp schedule based on domain age:

| Week | Max emails/day | Warmup status |
|------|---------------|---------------|
| Week 1-2 (May 6–19) | 10/day | Warming |
| Week 3-4 (May 20–Jun 2) | 25/day | Partially warmed |
| Week 5+ (Jun 3+) | 50/day | Ready for volume |

**Do not jump to 50/day before Week 5.** Google Workspace flags new senders who spike volume. You'll land in spam and lose all the warmup progress.

### Email Hygiene Checklist

Before ramping past 25/day:
- [ ] SPF: `v=spf1 include:_spf.google.com ~all`
- [ ] DKIM from Gmail Workspace setup
- [ ] DMARC: `v=dmarc1; p=quarantine; rua=mailto:joe@attribu.io`
- [ ] Verify at [mxtoolbox.com](https://mxtoolbox.com)

### Calendly Link in Cold Email

You're including a Calendly link in the email signature — this is a tradeoff:
- **Pro:** Reduces friction, prospect can book without a back-and-forth
- **Con:** Links in cold emails slightly hurt deliverability, can look less personal

**Recommendation:** Keep the Calendly link in the signature (not inline in the body). This is the current approach and it's fine. If reply rates stay below 3% after 40+ sends, test a version with no link and just "Worth a quick call?" as the CTA.

---

## Phase 2: Prospect Research (5-10 min per contact)

Before emailing anyone from the Apollo list, do this:

### Research Checklist

- [ ] Google the company — website, service area, fleet mentions
- [ ] Check Google Maps — reviews, complaints about scheduling/delays, photos of vans
- [ ] LinkedIn — employee count, any ops/dispatch mentions
- [ ] Find one **geo-specific or company-specific detail** for line 2 of your email

### What You're Looking For

**Green flags:**
- 15-100 technicians (sweet spot)
- Multi-location or wide service area ("serving 6 counties", "3 branches")
- Google reviews mentioning late arrivals, missed windows, scheduling issues
- Owner-operated (faster decisions)
- ServiceTitan or Housecall Pro user (you can integrate later)

**Red flags:**
- <10 employees (too small, pain not acute)
- National chain (slow procurement, wrong buyer)
- Parts distributor or sales-only (not field service operators)
- No visible fleet/trucks

---

## Phase 3: Cold Email

### The Template

You've evolved past the original 5-sentence template. The geo-specific, problem-first format is working better. Use this structure:

```
Subject: [City] [vertical] + routing = expensive problem

Hi [First Name],

[City]-specific pain point — something true about operating in their market that makes routing harder. One sentence.

I'm building Attribu, a tool that shows field service companies exactly where their scheduling waste lives — wasted drive time, back-to-back jobs on opposite ends of [area], and routes that look fine on paper but bleed hours every week.

[Credibility line: "I spent two years as a production ML engineer at FedEx building systems that touched delivery operations at scale — I know what optimized routing looks like and most operators don't come close."]

We're in early access and offering free routing audits for a handful of [City] [HVAC/pest control/plumbing] companies before we launch. No pitch — just a 30-minute look at your current routes and a straight read on where you're losing time.

Worth a quick call? Happy to work around your schedule.

Joe Waugh
Attribu.io — Route intelligence for field ops
Book a 30-minute call: [Calendly link]
```

### Phoenix HVAC Example (Your Current Version)

```
Subject: Phoenix HVAC + summer routing = expensive problem

Hi [Name],

Phoenix summers are brutal for HVAC scheduling. Your techs cover more ground in more heat than almost anywhere else in the country — and most routing tools aren't built for that kind of pressure.

I'm building Attribu, a tool that shows field service companies exactly where their scheduling waste lives — wasted drive time, back-to-back jobs on opposite ends of the valley, and routes that look fine on paper but bleed hours every week.

We're in early access and offering free routing audits for a handful of Phoenix HVAC companies before we launch. No pitch — just a 30-minute look at your current routes and a straight read on where you're losing time.

Worth a quick look? Happy to work around your schedule.

Joe Waugh
Attribu.io — Route intelligence for field ops
Book a 30-minute call: [Calendly link]
```

**Note:** The FedEx credibility line is missing from this version. Consider testing a version that adds it — it is your single strongest differentiator. Something like: *"I'm a production ML engineer — I spent two years at FedEx building systems that touched delivery ops at scale."*

### Other Market Variants

**Pest Control (Phoenix):**
```
Subject: Phoenix pest control + routing = expensive summer

Hi [Name],

Phoenix summer demand is a different beast — your techs are covering the same neighborhoods in 110° heat and most routing systems weren't designed for the density and repeat-service patterns that pest control runs on.
```

**Plumbing:**
```
Subject: [City] plumbing + emergency routing = expensive problem

Hi [Name],

Emergency plumbing calls are already expensive to dispatch — when techs are routed inefficiently on top of that, you're burning fuel and time before a wrench even touches a pipe.
```

### Personalization — Line 1 Alternatives

Replace the opening line with something specific to their company:

- "Noticed you just expanded to a second location in [City] — congrats."
- "Your Google reviews mention a few scheduling complaints — common issue at your scale."
- "Saw you're covering [X] cities across [Region] with your fleet."
- "Congrats on the Best of [City] award — clearly doing something right operationally."

**Why personalize:** Proves you're not mass-blasting. Increases reply rate 2-3x. HubSpot tracking will show who's opening but not replying — those are your prioritized follow-ups.

### Email Rules

- **Plain text body** — no HTML, no images, no fancy formatting
- **Signature is fine** — Attribu.io tagline + Calendly link
- **Send 8am–11am** their local time
- **One email per contact per thread** — no BCC, no mass merge
- **Compose individually or use Apollo sequences** — see next section

---

## Phase 4: Apollo Sequences

Apollo handles your 3-touch follow-up automatically. Set up a sequence:

### Sequence Structure

**Step 1 — Day 0: Initial email** (the template above)

**Step 2 — Day 4: One-line bump**
```
[First Name] — any interest in a quick look at where your routing hours are going?
```
- Reply in same thread
- One sentence
- No links, no attachments

**Step 3 — Day 10: Close-out**
```
[First Name] — last note from me. If routing ever becomes a priority, I'm at joe@attribu.io.
```
- Move on after this. 3 touches is enough.

### Apollo → HubSpot Sync

Make sure your Apollo sequence syncs contact activity back to HubSpot. If it doesn't auto-sync:
- After Step 1 sends: log contact in HubSpot → stage "Contacted"
- After any open or click: check HubSpot tracking, flag for manual follow-up if multiple opens with no reply

**Multiple opens = interested but hesitant.** Call them. Don't wait for a reply.

---

## Phase 5: HubSpot Pipeline

### Pipeline Stages

1. **Identified** — found in Apollo, researched
2. **Contacted** — initial email sent
3. **Replied** — they responded (any response)
4. **Call Scheduled** — discovery call on calendar
5. **Discovery Done** — call completed, pain validated
6. **Audit Proposed** — free or paid audit offer sent
7. **Audit Active** — they've agreed / data coming in
8. **Pilot Proposed** — 90-day pilot offer sent
9. **Pilot Active** — paying, work underway
10. **Full Client** — converted to full pricing (Closed Won)
11. **Closed Lost** — no response after 3 touches, or explicit pass

### After Every Email — Log It

1. HubSpot → CRM → Contacts → find or create contact
2. Add note: `Sent initial outreach [date]. Subject: [subject]. Personalization: [detail used].`
3. Set stage: "Contacted"

### HubSpot Email Tracking Intel

HubSpot shows you who opened and clicked even without a reply. Use this:
- **2+ opens, no reply after 5 days** → send a direct follow-up: *"[Name] — saw you opened this — worth a quick 15 minutes?"*
- **0 opens after 7 days** → try a different subject line variant on the bump

---

## Phase 6: Handling Responses

### Scenario A: Positive ("Tell me more" / "Let's talk" / Calendly booking)

1. Move deal to "Replied" in HubSpot
2. **Respond within 2 hours** if they emailed. If they booked Calendly, send a quick confirmation note.
3. Propose specific times if no Calendly booking:
```
Great — how about [Day] at [time] or [Day] at [time] [timezone]?

We can do Zoom or phone, whatever works.

— Joe
```
4. Once scheduled → move to "Call Scheduled" in HubSpot, add call time to notes

### Scenario B: Objections

**"We already use ServiceTitan/Housecall Pro"**
```
Those are great for scheduling — Attribu optimizes the actual routes between jobs.

Think Google Maps vs. what a logistics company uses internally. Happy to show you the difference on a short call.
```

**"How much does it cost?"**
```
Right now I'm offering free routing audits for a handful of early operators — 30-minute look at your routes, no cost, no pitch.

If you see value in it, we can talk about what a pilot looks like. Want to grab 20 minutes?
```

**"Send me more info"**
```
I can, but a 15-minute call will answer your questions faster than anything I could write.

How about [day] at [time]?
```

**Don't send decks, case studies, or long emails.** Get them on a call.

### Scenario C: Hard No

```
No problem — appreciate you letting me know.

If anything changes, I'm at joe@attribu.io.
```
Move to Closed Lost. Add note. Move on.

---

## Phase 7: Discovery Call (20-30 minutes)

This is NOT a sales call. This is customer discovery.

### Call Structure

**Minutes 1-2: Intro**
```
Thanks for making time. Quick background — I'm a production ML engineer, spent two years at FedEx building systems that touched delivery operations at scale. Now I'm building Attribu for field service operators.

I'm in early stages and honestly just trying to understand how companies like yours handle routing today. Mind if I ask a few questions?
```

**Minutes 3-15: Discovery (DO NOT PITCH)**

1. **"Walk me through how you dispatch techs today."**
   Listen for: ServiceTitan, Housecall Pro, whiteboard, manual calls

2. **"What does a bad dispatch day look like for you?"**
   Listen for: techs crossing the city, late arrivals, overtime, complaints

3. **"What does that cost you — roughly?"**
   Listen for: fuel waste, labor hours, lost jobs, angry customers
   *If they can't give you a dollar figure, pain isn't acute enough.*

4. **"Have you tried to solve this before?"**
   Listen for: tried Route4Me/Samsara, built a spreadsheet, hired a consultant

5. **"If you could fix routing overnight, what would change?"**
   Listen for: fewer miles driven, more jobs per tech, better customer experience

6. **"Who makes the call on software like this?"**
   Listen for: owner, ops manager, CFO — map the buying process

**Minutes 16-18: Light framing**

If they've described real pain in dollar terms:
```
That lines up with what I'm hearing from other [HVAC/pest control] operators.

I'm building a system that optimizes routes using the same ML techniques applied in large-scale logistics — time windows, tech skill matching, dynamic rerouting.

Most operators at your scale save $100K–$200K/year in fuel and drive time.

Would it be useful if I ran a free audit on your last 30 days of job data and showed you exactly where you're losing time?
```

**Minutes 18-20: Next steps**

If they say yes to the audit:
```
Great. Can you export your job data from [ServiceTitan/their system] as a CSV?

I'll run the analysis and show you what optimized routing would have looked like. Takes about a week.

Right now I'm doing these free for early operators while we're building — if you see real savings, we can talk about what a pilot looks like.
```

Move deal to "Discovery Done" in HubSpot. Add detailed notes: pain points, willingness to pay, decision-maker, data access.

---

## Phase 8: The Free Audit (First 2-3 Customers)

### Why Free First

You have zero case studies, zero social proof. Asking for $500 before you can show results is harder. The first 2-3 audits are an investment in your first case study.

**Free audit scope:**
- Their last 30 days of job data
- Your manual optimization analysis
- A 2-page deliverable: current state → optimized state → dollar delta
- Total your time: 4-8 hours

**What you're building:** "We saved [Company] $X in one month" — your first proof point.

### Transition to Paid

Once you have 1 delivered case study with real numbers, switch to paid:
- < 30 techs: $500
- 30–50 techs: $750
- 50+ techs: $1,000

**Get paid upfront.** Stripe invoice, Venmo, check — doesn't matter. No payment = no start.

**HubSpot:** Move to "Audit Active" when they agree and data is incoming.

---

## Metrics to Track (Weekly Review — Every Friday)

| Metric | Target | Action if missed |
|--------|--------|-----------------|
| Emails sent this week | 10 (wk 1-2), 25 (wk 3-4), 50 (wk 5+) | Hitting volume? |
| Reply rate | 10–20% | If <5% after 30 sends: message is broken |
| Open rate (HubSpot) | 40–60% | If <20%: subject lines need testing |
| Calls scheduled | 1–2/week | Are replies converting to calls? |
| Discovery calls done | 1–2/week | Are you learning? |
| Free audits agreed | 1 in first month | Validates pain is real |
| Paid audits sold | 1 after first case study | Validates willingness to pay |

**Open but no reply after 5 days:** Follow up directly — *"Saw you opened this — worth 15 minutes?"*

**Reply rate <5% after 30 sends:** Stop. Rewrite subject line and opening line. Test 10 more. Iterate.

---

## Do's and Don'ts

### DO

- Talk to every prospect who opens 2+ times without replying — they're interested
- Ask for money after the first free audit — if they won't pay $500 for analysis, they won't pay $2,500/month for software
- Personalize every email with a company-specific or geo-specific line 1
- Track everything in HubSpot — you can't improve what you don't measure
- Respond to emails within 2 hours, schedule calls within 48 hours
- Stay in Phoenix market until you have 2-3 case studies — depth before breadth
- Add the FedEx credibility line — it is your strongest differentiator

### DON'T

- Don't pitch on the discovery call — listen and learn
- Don't send decks or case studies — get them on a call
- Don't let free audits scope-creep into ongoing consulting
- Don't let anyone stay at pilot pricing past 90 days — hold the line
- Don't chase past 3 touches — move on
- Don't say "I led route optimization at FedEx" — say "I was a production ML engineer at FedEx"
- Don't build software until you've done 1+ audits and can articulate the top 3 pain points in dollar terms

---

## What Success Looks Like at Each Stage

### Week 1-2 (now)
- 20 emails sent (within warmup limits)
- 2-4 replies
- 1-2 discovery calls scheduled

### Week 3-4
- 50 total emails sent
- 5-10 total replies
- 3-5 discovery calls completed
- 1 free audit agreed and started

### Month 2
- 100+ total emails sent
- 1 free audit delivered with case study numbers
- 1 paid audit sold ($500-$1K)
- 1 pilot proposal sent

### Month 3
- 1 paying pilot active ($500/month)
- 2-3 more audits in pipeline
- Starting to build V1 software based on what you learned

---

## Quick Reference: HubSpot Pipeline Stages

1. **Identified** — in Apollo, researched
2. **Contacted** — email sent
3. **Replied** — they responded
4. **Call Scheduled** — on calendar
5. **Discovery Done** — call complete, pain validated
6. **Audit Proposed** — free or paid audit offer sent
7. **Audit Active** — data incoming / work started
8. **Pilot Proposed** — 90-day offer sent
9. **Pilot Active** — paying and active
10. **Full Client** — converted to full price (Closed Won)
11. **Closed Lost** — no response or explicit pass
