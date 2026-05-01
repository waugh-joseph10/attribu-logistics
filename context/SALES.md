# SALES.md — Early-Stage Sales Playbook for attribu.io

> YC-style sales process for pre-product stage
> Goal: 10 customer discovery calls → 1 manual pilot → V1 validation
> Last updated: May 2026

---

## The Core Loop

```
Apollo → Research → Email → HubSpot → Follow-up → Call → Discovery → Pilot
```

Every interaction moves a prospect through this pipeline. Track everything. Learn fast.

---

## Phase 1: Prospect Research (5-10 min per contact)

You've downloaded contacts from Apollo. Before you email anyone, do this:

### Research Checklist (per company)

- [ ] **Google the company** — find their website, service area, fleet mentions
- [ ] **Check Google Maps** — look at reviews, photos of service vans, complaints about scheduling/delays
- [ ] **LinkedIn company page** — employee count, recent posts, any routing/dispatch mentions
- [ ] **Check if they use ServiceTitan/Housecall Pro** — look for integrations mentioned on their site
- [ ] **Find one specific detail** to personalize line 1 of your email

### What You're Looking For

**Green flags:**
- 15-100 technicians (sweet spot per CONTEXT.md)
- Multi-location service area ("serving 6 counties", "3 branches")
- Google reviews mentioning late arrivals, missed windows, scheduling issues
- Owner-operated (faster decision-making)
- ServiceTitan user (you can integrate later)

**Red flags:**
- <10 employees (too small, pain not acute)
- National chain (slow procurement, wrong buyer)
- Parts distributor or sales-only (not field service operators)
- No visible fleet/trucks

### Where to Record This

Create a simple spreadsheet or use HubSpot notes:

| Company | Contact | Title | Fleet Size Est. | Personalization Detail | Stage |
|---------|---------|-------|----------------|------------------------|-------|
| ABC HVAC | John Smith | Owner | ~30 trucks | Just expanded to 3 locations | Ready to email |

---

## Phase 2: Initial Outreach Email

### The Template (from CONTEXT.md)

```
Subject: Route optimization for [Company Name]

Hi [First Name],

My background is in route optimization engineering — I led this work at FedEx before starting attribu.io.

Most [HVAC/plumbing/electrical] operators with 20–80 techs are leaving $100K–$200K/year on the table in fuel and drive time. I can show you exactly where yours is going.

Would you have 20 minutes this week for a quick call?

— Joe
joe@attribu.io
```

### Personalization Examples (Line 1 alternatives)

Replace line 1 with something specific to their company:

- "Noticed you just expanded to a second location in [City] — congrats."
- "Saw you're covering 6 counties across [Region] with your HVAC fleet."
- "Your Google reviews mention occasional scheduling delays — common issue for operators at your scale."
- "Congrats on the Best of [City] award — clearly doing something right."

**Why personalize:** Proves you're not mass-emailing. Shows you did homework. Increases reply rate 2-3x.

### Email Rules (from TODO.md)

- **Plain text only** — no HTML, no logos, no fancy signatures
- **Max 10 emails/day week 1-2**, then ramp to 25/day week 3-4, 50/day week 5+ (TODO.md:23)
- **Send between 8am-11am** their local time (when owners check email)
- **Compose each email individually** — no BCC, no mail merge tools
- **5 sentences max** (per CONTEXT.md:227)

### Sending Process

1. Log into Gmail as **joe@attribu.io** (via send-as on attribu.app@gmail.com)
2. Compose email individually (copy/paste template, personalize line 1)
3. Send
4. **Immediately log in HubSpot** (next section)

---

## Phase 3: HubSpot Tracking (Do This After Every Email)

### Create Deal Flow

After sending each email:

1. Go to HubSpot → **CRM** → **Deals**
2. Click **Create deal**
3. Fill in:
   - **Deal name:** [Company Name]
   - **Pipeline stage:** "Contacted"
   - **Amount:** Leave blank
   - **Close date:** +30 days (placeholder)
4. Associate the contact:
   - If contact doesn't exist, create it (name, email, company, title)
5. Add a **Note**:
   ```
   Sent initial outreach email [date]
   Personalization: [the detail you used]
   ```

### Why This Matters

- Prevents double-emailing the same person
- Tracks your actual send volume (are you hitting 10/day?)
- Gives you a visual pipeline of where deals are stuck
- Forces you to review progress weekly

---

## Phase 4: Follow-Up Sequence (3-Touch Rule)

From TODO.md:24, use a 3-touch sequence:

### Touch 1: Initial Email (Day 0)

The template above.

### Touch 2: One-Line Bump (Day 4)

If no response after 4 days, send this:

```
[First Name] — any interest in seeing where your routing dollars are going?
```

**Rules:**
- Reply to the same email thread (don't start new thread)
- One sentence max
- No attachments, no links

**HubSpot action:**
- Add note: "Sent bump email [date]"
- Keep stage as "Contacted"

### Touch 3: Close-Out (Day 10)

If no response after 10 days total, send this and move on:

```
[First Name] — last note from me. If routing optimization ever becomes a priority, I'm at joe@attribu.io.
```

**HubSpot action:**
- Move deal to **"Closed Lost"** stage
- Add note: "No response after 3 touches — closed out"

**Don't chase beyond this.** Your time is worth more. If they care, they'll reply.

---

## Phase 5: Handling Responses

### Scenario A: Positive Reply ("Tell me more" / "Let's talk")

**Do this immediately:**

1. **Move deal to "Replied" stage** in HubSpot
2. **Respond within 2 hours** (speed matters at this stage)
3. **Propose specific times** for a 20-minute call:

```
Great — how about Tuesday at 10am or Wednesday at 2pm [your timezone]?

We can do Zoom or phone, whatever's easier.

— Joe
```

4. **Once call is scheduled:**
   - Move deal to **"Call Scheduled"** stage in HubSpot
   - Send calendar invite from Google Calendar (joe@attribu.io)
   - Add note in HubSpot with call time

### Scenario B: Objection or Question

Common objections:

**"We already use ServiceTitan/Housecall Pro for routing"**

Response:
```
Those are great for scheduling — attribu.io optimizes the actual routes between jobs.

Think Google Maps vs. what FedEx uses internally. Happy to show you the difference on a quick call.
```

**"How much does it cost?"**

Response:
```
Depends on fleet size, but typical ROI is 5-10x our monthly fee in fuel/labor savings.

Want to see what that looks like for your operation specifically?
```

**"Send me more info"**

Response:
```
I can, but honestly a 15-minute conversation will answer your questions faster than a PDF.

How about tomorrow at [time]?
```

**Don't send decks, case studies, or long emails.** Get them on a call. (YC principle: talk to users, don't email them.)

### Scenario C: Hard No ("Not interested")

Response:
```
No problem — appreciate you letting me know.

If anything changes, I'm at joe@attribu.io.
```

**HubSpot action:**
- Move to **"Closed Lost"** stage
- Add note: "Explicit pass — not interested"

---

## Phase 6: Discovery Call (20 minutes)

You got them on the phone. This is NOT a sales call. This is customer discovery.

### Call Structure (from CONTEXT.md Phase 1)

**Minutes 1-2: Quick intro**
```
Thanks for making time. Quick background — I led route optimization at FedEx before starting attribu.io. We're building ML-powered dispatch for field service operators.

I'm in the early stages and honestly just trying to learn how companies like yours handle routing today. Cool if I ask a few questions?
```

**Minutes 3-15: Discovery questions (DO NOT PITCH)**

Ask these in order:

1. **"How do you dispatch techs today?"**
   Listen for: ServiceTitan, Housecall Pro, whiteboard, manual

2. **"What does a bad dispatch day look like for you?"**
   Listen for: techs driving across town, late arrivals, overtime, customer complaints

3. **"What does that cost you — roughly?"**
   Listen for: fuel waste, labor hours, lost jobs, angry customers
   *If they can't quantify it, the pain isn't acute enough.*

4. **"Have you tried to solve this before? What happened?"**
   Listen for: tried Route4Me/Samsara and it didn't work, built a spreadsheet, hired a logistics consultant

5. **"If you could wave a wand and fix routing overnight, what would change?"**
   Listen for: fewer miles driven, more jobs per tech, better customer experience

6. **"Who makes the decision on software like this?"**
   Listen for: owner, operations manager, CFO (understand the buying process)

**Minutes 16-18: Light validation**

If they've described acute pain (in dollar terms), NOW you can mention what you're building:

```
That lines up with what I'm hearing from other [HVAC/plumbing] operators.

We're building a system that optimizes routes using the same ML techniques I used at FedEx — time windows, skill matching, dynamic rerouting.

Most operators at your scale save $100K–$200K/year in fuel and drive time.

Would it be useful if I ran an audit on your last 30 days of job data and showed you exactly what you left on the table?
```

**Minutes 18-20: Next steps**

If they say yes to the audit:
```
Great. Can you export your job data from [ServiceTitan/Housecall Pro] as a CSV?

I'll run the analysis manually and show you what optimized routing would have looked like. Takes me about a week.

I charge $500-$1,000 for this audit depending on complexity. Sound fair?
```

**HubSpot action:**
- Move deal to **"Discovery Done"** stage
- Add detailed notes from the call (pain points, willingness to pay, next steps)

---

## Phase 7: The Concierge MVP Audit (Before Building Anything)

From CONTEXT.md Phase 2:

### What You're Doing

- Take their last 30 days of job data (addresses, time windows, tech assignments)
- **Manually optimize it** (spreadsheet + brain + maybe OR-Tools script)
- Show them what their routing SHOULD have looked like
- Quantify what they left on the table (fuel miles, wasted hours, jobs per tech)

### Why This Matters

1. **Validates the problem is real** — if they won't pay $500-$1,000 for an audit, they won't pay $2,000/month for software
2. **Gives you intimate knowledge** of real data and constraints before you architect anything
3. **Creates your first case study** — "We saved ABC HVAC $22K in one month"

### Deliverable

A simple PDF or Google Doc with:
- **Current state:** Their actual routing from last 30 days
- **Optimized state:** What it should have looked like
- **Delta:** Miles saved, hours saved, estimated $ savings

### Pricing

- $500 for <30 techs
- $750 for 30-50 techs
- $1,000 for 50+ techs

**Get paid upfront.** Venmo, Stripe invoice, check — doesn't matter. No free audits.

**HubSpot action:**
- Move deal to **"Pilot Proposed"** stage when you send proposal
- Move to **"Pilot Active"** when they pay and you start work

---

## Phase 8: After the Audit → Pilot Offer

If the audit shows real savings and they're happy:

```
Based on this audit, you're leaving ~$180K/year on the table.

I'm building software to automate this — it'll give you optimized dispatch recommendations every morning at 6am.

Would you be interested in a 90-day pilot at $500/month?

If we don't save you at least 5x that in fuel and labor, you can cancel anytime.
```

### Pilot Terms (from CONTEXT.md Phase 4)

- **Price:** $500/month for 90 days
- **Payment:** Credit card on file BEFORE starting (use Stripe)
- **Deliverable:** Daily dispatch recommendations (email or simple dashboard)
- **Success metric:** Track actual fuel/labor savings monthly

**HubSpot action:**
- Move to **"Full Client"** stage (mark as "Closed Won") when they commit to pilot

---

## Metrics to Track (Weekly Review)

Every Friday, review these numbers in HubSpot:

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Emails sent this week | 10-50 (depending on ramp) | Hitting volume targets? |
| Reply rate | 10-20% | If <5%, messaging is broken |
| Calls scheduled | 1-2/week | Are you converting replies to calls? |
| Discovery calls completed | 1-2/week | Are you learning? |
| Paid audits sold | 1 in first month | Validates pain is real |
| Pilots started | 1 by Month 2-3 | Validates people will pay recurring |

**If reply rate is <5% after 30 emails:** Your messaging is broken. Try different subject lines or personalization.

**If calls aren't converting to audits:** The pain isn't acute enough or you're not asking for money confidently.

---

## Do's and Don'ts (YC Principles)

### DO

- **Talk to customers obsessively** — 10 discovery calls beats any amount of research
- **Ask for money early** — if they won't pay $500 for an audit, they won't pay $2,000/month for software
- **Personalize every email** — mention something specific about their company
- **Track everything in HubSpot** — you can't improve what you don't measure
- **Move fast** — respond to emails within 2 hours, schedule calls within 48 hours
- **Focus on regional operators first** — faster decisions, more acute pain (CONTEXT.md:148)

### DON'T

- **Don't pitch on the discovery call** — just listen and learn (CONTEXT.md:102)
- **Don't send decks or case studies** — get them on a call instead
- **Don't use bulk email tools** — manual is better at <50 prospects (TODO.md:31)
- **Don't let anyone stay at pilot pricing >90 days** — hold the line on full pricing (CONTEXT.md:242)
- **Don't chase non-responsive prospects** — 3 touches and move on
- **Don't build software until you've done 1+ manual audits** — learn the constraints first (CONTEXT.md:84)

---

## What Success Looks Like at Each Stage

### Week 1-2
- 20 emails sent
- 2-4 replies
- 1-2 discovery calls scheduled

### Week 3-4
- 50 emails sent (total)
- 5-10 replies (total)
- 3-5 discovery calls completed
- 1 paid audit sold

### Month 2
- 100+ emails sent (total)
- 1 manual audit delivered
- 1 pilot proposal sent

### Month 3
- 1 paying pilot active ($500/month)
- 2-3 more audits in pipeline
- Starting to build V1 software based on learnings

---

## Email Hygiene & Deliverability

### Before You Send 50+ Emails

From TODO.md, verify your email setup:

- [ ] SPF record: `v=spf1 include:_spf.google.com ~all`
- [ ] DKIM record from Gmail setup
- [ ] DMARC record: `v=dmarc1; p=quarantine; rua=mailto:joe@attribu.io`
- [ ] Verify at [mxtoolbox.com](https://mxtoolbox.com)

### Volume Ramp (from TODO.md:23)

- **Week 1-2:** Max 10 emails/day
- **Week 3-4:** Max 25 emails/day
- **Week 5+:** Max 50 emails/day

**Why ramp slowly:** Gmail/Google Workspace flags new senders who suddenly send 50+ emails/day. Warm up your domain reputation.

### Red Flags That Hurt Deliverability

- Sending from attribu.app@gmail.com instead of joe@attribu.io
- Using BCC for bulk sends
- Adding links or images in initial email
- Unsubscribe footers (looks like marketing, not personal outreach)

---

## When to Build Software

From CONTEXT.md Phase 3:

**DO NOT write a single line of code until:**

1. You've done 10+ customer discovery calls
2. You've sold and delivered at least 1 manual audit
3. You can clearly articulate the top 3 pain points in dollar terms
4. Someone has paid you money (even just $500) to solve this problem

**Why:** YC companies fail by building things nobody wants. Talk to users first. Build second.

---

## Tools Summary

| Tool | Purpose | Cost |
|------|---------|------|
| **Apollo.io** | Find prospects | Free (50 exports/month) |
| **Gmail (joe@attribu.io)** | Send emails | Free (via Google Workspace or send-as) |
| **HubSpot** | CRM, pipeline tracking | Free tier |
| **Google Calendar** | Schedule calls | Free |
| **Zoom** | Discovery calls | Free tier |
| **Stripe** | Collect payment for audits/pilots | 2.9% + $0.30/transaction |
| **Google Sheets** | Manual optimization work (pre-software) | Free |

---

## Final Note: Speed Wins

The difference between successful YC companies and failures at this stage is **speed of iteration**.

- Email 10 people → learn → adjust messaging → email 10 more
- Do 5 discovery calls → learn what pain is real → adjust questions → do 5 more
- Sell 1 audit → learn real data constraints → build V1 → sell pilot

**Don't batch.** Don't overthink. Send the emails. Get on the calls. Learn fast.

Your unfair advantage (CONTEXT.md:36) is the FedEx pedigree. Use it in every email. Operators trust credibility more than features.

Now go sell.

---

## Quick Reference: HubSpot Pipeline Stages

From TODO.md:13, your pipeline should be:

1. **Identified** — found in Apollo, researched
2. **Contacted** — initial email sent
3. **Replied** — they responded
4. **Call Scheduled** — discovery call on calendar
5. **Discovery Done** — call completed, pain validated
6. **Pilot Proposed** — audit or pilot offer sent
7. **Pilot Active** — paying for audit or pilot
8. **Full Client** — pilot converted to full pricing (mark as "Closed Won")
9. **Closed Lost** — no response or explicit pass

Move deals through these stages as you go. Review weekly.
