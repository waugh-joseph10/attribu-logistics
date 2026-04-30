# Email Setup & Client Outreach TODO

## 1. Verify Email Infrastructure (Do First)
- [ ] Confirm Cloudflare MX records point to `route1.mx.cloudflare.net`
- [ ] Add SPF record: `TXT @ "v=spf1 include:_spf.google.com ~all"`
- [ ] Add DKIM record: `TXT google._domainkey <value from Gmail DKIM setup>`
- [ ] Add DMARC record: `TXT @ "v=dmarc1; p=quarantine; rua=mailto:joe@attribu.io"`
- [ ] Verify at [mxtoolbox.com](https://mxtoolbox.com)
- [ ] In Gmail Settings → Accounts → "Send mail as" → set `joe@attribu.io` as default

## 2. Set Up Client Tracking (CRM)
- [ ] Create free HubSpot account, connect Gmail
- [ ] Create pipeline with stages: `Identified → Contacted → Replied → Call Scheduled → Discovery Done → Pilot Proposed → Pilot Active → Full Client → Closed Lost`

## 3. Find Clients
- [ ] Sign up for Apollo.io free tier (50 exports/month)
- [ ] Search: Title = Owner OR Operations Manager, Industry = HVAC/Plumbing/Electrical, Size = 10–200 employees
- [ ] Supplement with Google Maps: "HVAC company [city]" → find owner → look up via Apollo

## 4. Outreach Rules
- [ ] Send plain-text only — no HTML, no logos, no unsubscribe footer
- [ ] Personalize line 1 with something specific to their company
- [ ] Ramp sending volume: max 10/day week 1–2, 25/day week 3–4, 50/day week 5+
- [ ] Use 3-touch sequence: Day 0 (initial), Day 4 (one-line bump), Day 10 (close-out)
- [ ] Log every sent email in HubSpot immediately

## 5. Do Not Do Yet
- [ ] ~~Bulk email tools (Mailchimp, Brevo) for cold outreach~~
- [ ] ~~Google Workspace paid plan — free setup is sufficient~~
- [ ] ~~Automated sequences — manual is better at <50 prospects~~
- [ ] ~~OAuth / Gmail API inbox integration — not needed until V2+~~
