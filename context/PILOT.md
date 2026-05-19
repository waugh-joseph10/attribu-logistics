# Pilot Evaluation & Build Framework

> **Purpose:** Validate pain, quantify ROI, and deliver value BEFORE building software
> **Sequence:** Free audit (first 2-3) → case study → paid audit → 90-day pilot → full price
> **Outcome:** Either a paying customer with proven ROI, or a clean "no" with lessons learned

---

## Audit Strategy: Free First, Then Paid

### Why Free for the First 2-3

You have zero case studies. Asking for $500–$1,000 before you can show results is a tougher close with no social proof. The first 2-3 audits are an investment:

1. **You get real data** — constraints, data quality, what operators actually track
2. **You build the case study** — "We saved [Company] $22K in one month"
3. **The case study sells the next audit** — once you have numbers, $500 is easy to justify

### Transition to Paid

After your first delivered case study with verified dollar savings:

| Fleet Size | Audit Price |
|-----------|------------|
| < 30 techs | $500 |
| 30–50 techs | $750 |
| 50+ techs | $1,000 |

**Get paid upfront.** Stripe invoice or Venmo — no payment, no start.

**The filter:** If they won't pay $500 for an analysis after seeing your case study, they won't pay $2,500/month for software. Move on.

---

## Phase 1: Qualification (First 48 Hours After Call)

### Minimum Requirements

- [ ] **Fleet size:** 15–100 technicians (sweet spot: 20–50)
- [ ] **Geography:** Regional service area, not hyper-local (>50 mile radius)
- [ ] **Current dispatch:** Manual or basic FSM (whiteboard, spreadsheet, ServiceTitan, Housecall Pro)
- [ ] **Decision maker:** Talking to owner, ops manager, or someone who can authorize $500+
- [ ] **Data access:** Can export job history (CSV is fine)
- [ ] **Pain language:** Uses dollar figures — "we waste X hours/week" not "it would be nice"

### Red Flags (Walk Away)

- Fleet < 10 techs (too small, can't prove ROI)
- Fleet > 200 techs (too complex for manual MVP, wrong sales cycle)
- Service area < 20 mile radius (routing delta is negligible)
- "It would be nice" language (vitamin, not painkiller)
- No one can export job data
- Decision maker is 3+ levels removed from operations

### Qualification Questions (Discovery Call)

1. **"Walk me through how you dispatch technicians today."**
2. **"How many jobs does an average tech complete per day?"** — baseline metric
3. **"What does a bad dispatch day cost you?"** — if they can't answer in dollars, pain isn't acute
4. **"Have you tried to solve this before? What happened?"**
5. **"Can you export the last 30 days of job data?"** — yes = proceed, no = ask about API access
6. **"If I can show you exactly where you're losing money, would you want to see it?"** — this is the filter for free audit

---

## Phase 2: Data Collection (Week 1)

### Required Data Fields

| Field | Required? | Format | Example |
|---|---|---|---|
| Job ID | Yes | Text/Number | `JOB-12345` |
| Job Date | Yes | Date | `2026-04-15` |
| Job Start Time | Yes | Time | `09:30` |
| Job End Time | Yes | Time | `11:15` |
| Service Address | Yes | Full address | `123 Main St, Phoenix AZ 85001` |
| Assigned Technician | Yes | Tech ID/Name | `John Smith` |
| Job Type | Preferred | Category | `HVAC Repair`, `Maintenance` |
| Skill Required | Preferred | Text | `HVAC Level 2` |
| Time Window | Preferred | Time range | `8am-12pm` |

### Data Request Email

```
Subject: Data request for routing analysis

Hi [Name],

To run the analysis we discussed, I need the last 30 days of completed jobs:

- Job ID
- Date and time (start + end)
- Service address
- Which tech was assigned
- Job type (if tracked)

A CSV export from [ServiceTitan/their system] works great. If you need help pulling it, let me know — I can walk you through it.

Once I have this, I'll deliver the analysis within 5 business days.

— Joe
joe@attribu.io
```

### Data Quality Check

When you receive the data, validate immediately:

```python
import pandas as pd

df = pd.read_csv('customer_jobs.csv')

required = ['job_id', 'date', 'start_time', 'end_time', 'address', 'tech_id']
missing = [col for col in required if col not in df.columns]
if missing:
    print(f"Missing required columns: {missing}")

null_counts = df[required].isnull().sum()
if null_counts.any():
    print(f"Null values:\n{null_counts[null_counts > 0]}")

print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Total jobs: {len(df)}")
print(f"Unique techs: {df['tech_id'].nunique()}")

dupes = df[df.duplicated(subset=['job_id'], keep=False)]
if len(dupes) > 0:
    print(f"{len(dupes)} duplicate job IDs")
```

If data quality is poor (>20% nulls, inconsistent addresses, missing techs), **stop and request a cleaner extract.** Bad data = bad analysis = lost credibility.

---

## Phase 3: Manual Optimization Analysis (Week 1-2)

### Step 1: Geocode Addresses

```python
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="attribu_analysis")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def geocode_address(address):
    try:
        location = geocode(address)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None, None

df[['lat', 'lon']] = df['address'].apply(
    lambda x: pd.Series(geocode_address(x))
)
df.to_csv('customer_jobs_geocoded.csv', index=False)
```

For larger datasets, use Google Maps Geocoding API (more accurate, requires billing).

### Step 2: Baseline Metrics

```python
import numpy as np

daily_tech = df.groupby(['tech_id', 'date']).agg({
    'job_id': 'count',
    'start_time': 'min',
    'end_time': 'max',
}).rename(columns={'job_id': 'jobs_per_day'})

daily_tech['hours_worked'] = (
    pd.to_datetime(daily_tech['end_time']) -
    pd.to_datetime(daily_tech['start_time'])
).dt.total_seconds() / 3600

baseline_jobs_per_day = daily_tech['jobs_per_day'].mean()
baseline_hours = daily_tech['hours_worked'].mean()

print(f"Avg jobs/tech/day: {baseline_jobs_per_day:.1f}")
print(f"Avg working hours: {baseline_hours:.1f}")
```

```python
from geopy.distance import geodesic

def calculate_route_distance(tech_jobs):
    if len(tech_jobs) < 2:
        return 0
    total = 0
    for i in range(len(tech_jobs) - 1):
        start = (tech_jobs.iloc[i]['lat'], tech_jobs.iloc[i]['lon'])
        end = (tech_jobs.iloc[i+1]['lat'], tech_jobs.iloc[i+1]['lon'])
        total += geodesic(start, end).miles
    return total

df_sorted = df.sort_values(['tech_id', 'date', 'start_time'])
daily_distance = df_sorted.groupby(['tech_id', 'date']).apply(
    calculate_route_distance
).reset_index(name='total_miles')

print(f"Avg miles/tech/day: {daily_distance['total_miles'].mean():.1f}")
```

### Step 3: OR-Tools Optimization

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_distance_matrix(locations):
    n = len(locations)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = geodesic(locations[i], locations[j]).miles
    return matrix

def solve_vrp(distance_matrix, num_vehicles, depot=0):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return int(distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)] * 100)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.seconds = 30

    return manager, routing, routing.SolveWithParameters(search_parameters)
```

### Step 4: Scale Across Full Dataset

```python
results = []

for (tech, date), group in df.groupby(['tech_id', 'date']):
    if len(group) < 2:
        continue

    locations = list(zip(group['lat'], group['lon']))
    distance_matrix = create_distance_matrix(locations)
    manager, routing, solution = solve_vrp(distance_matrix, num_vehicles=1)

    if solution:
        index = routing.Start(0)
        total_distance = 0
        while not routing.IsEnd(index):
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

        optimized_miles = total_distance / 100
        original_miles = calculate_route_distance(group)

        results.append({
            'tech_id': tech,
            'date': date,
            'original_miles': original_miles,
            'optimized_miles': optimized_miles,
            'savings_miles': original_miles - optimized_miles,
            'savings_pct': (1 - optimized_miles / original_miles) * 100
        })

results_df = pd.DataFrame(results)
```

---

## Phase 4: ROI Calculation

```python
FUEL_COST_PER_GALLON = 3.50
MPG = 15
AVG_SPEED_MPH = 25
HOURLY_LABOR_COST = 35
WORK_DAYS_PER_MONTH = 22

avg_daily_savings_miles = results_df['savings_miles'].mean()
num_techs = df['tech_id'].nunique()

# Fuel savings
monthly_miles_saved = avg_daily_savings_miles * num_techs * WORK_DAYS_PER_MONTH
monthly_fuel_savings = (monthly_miles_saved / MPG) * FUEL_COST_PER_GALLON
annual_fuel_savings = monthly_fuel_savings * 12

# Labor savings
avg_daily_time_saved_hours = avg_daily_savings_miles / AVG_SPEED_MPH
monthly_labor_savings = avg_daily_time_saved_hours * num_techs * WORK_DAYS_PER_MONTH * HOURLY_LABOR_COST
annual_labor_savings = monthly_labor_savings * 12

total_annual_savings = annual_fuel_savings + annual_labor_savings

print(f"Avg miles saved/tech/day: {avg_daily_savings_miles:.1f}")
print(f"Annual fuel savings: ${annual_fuel_savings:,.0f}")
print(f"Annual labor savings: ${annual_labor_savings:,.0f}")
print(f"TOTAL annual savings: ${total_annual_savings:,.0f}")
```

Update `HOURLY_LABOR_COST` and `AVG_JOB_REVENUE` based on what the customer tells you during the discovery call. Don't use defaults in the final deliverable.

---

## Phase 5: Deliverable

### What You Deliver

A clean 2-4 page PDF or Google Doc:

**1. Executive Summary (1 page)**
- Current state: X jobs/day, Y miles/tech, Z hrs driving
- Optimized state: +A jobs/day, -B% miles, -C hrs wasted
- Dollar impact: $D/month, $E/year
- Recommended next step: 90-day pilot at $[500-1K]/month

**2. Detailed Findings (1-2 pages)**
- Baseline metrics with simple charts
- Day-by-day comparison for 1 sample week
- Before/after route map for 1-2 techs (see below)

**3. Next Step (half page)**
- What a software solution looks like
- Pilot terms

### Route Visualization

```python
import folium

sample_tech = results_df.sort_values('savings_pct', ascending=False).iloc[0]['tech_id']
sample_date = results_df.sort_values('savings_pct', ascending=False).iloc[0]['date']
sample_jobs = df[(df['tech_id'] == sample_tech) & (df['date'] == sample_date)].copy()

m = folium.Map(
    location=[sample_jobs['lat'].mean(), sample_jobs['lon'].mean()],
    zoom_start=11
)
folium.PolyLine(
    list(zip(sample_jobs['lat'], sample_jobs['lon'])),
    color='red', weight=3, opacity=0.7, popup='Original Route'
).add_to(m)

for _, row in sample_jobs.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=6, popup=f"Job {row['job_id']}",
        color='blue', fill=True
    ).add_to(m)

m.save('route_comparison.html')
```

Export the map as a screenshot for the PDF.

---

## Phase 6: Pilot Offer

After a successful free audit showing real savings:

```
Subject: Next step — pilot for [Company Name]

Hi [Name],

Based on the analysis, you're leaving roughly $[X]/year on the table in fuel and drive time.

I'm building software to automate this — it'll give you optimized dispatch recommendations every morning at 6am.

Here's what I'm proposing:

90-Day Pilot: $[500-750-1000]/month based on fleet size
- Daily optimized routes delivered by 6am
- Weekly savings reports (miles, time, jobs per tech)
- Direct access to me for adjustments
- Cancel anytime if you don't see at least 5x ROI

After the pilot: $[1,500-4,000]/month based on fleet size. Only convert if you're seeing real results.

Want to move forward? Reply "yes" and I'll send a simple agreement and Stripe invoice.

— Joe
joe@attribu.io
```

### Pilot Pricing Tiers

| Fleet Size | Pilot (90 days) | Full Price |
|---|---|---|
| 15–20 techs | $500/month | $1,500/month |
| 21–40 techs | $750/month | $2,500/month |
| 41–80 techs | $1,000/month | $4,000/month |

**Credit card on file before starting.** Use Stripe. No payment = no start.

**HubSpot:** Move to "Pilot Proposed" when you send the offer, "Pilot Active" when they pay.

---

## Phase 7: Pilot Delivery

### Weeks 1-2: Manual

- Export their jobs each evening (CSV or API)
- Run optimization script overnight
- Email optimized dispatch schedule by 6am
- Weekly check-in: "Here's what we saved you this week"

### Weeks 3-4: Semi-Automated

- Django management command for nightly optimization
- Celery Beat to run at midnight
- Auto-send email with results
- You still review output before send (catch edge cases)

### Weeks 5-8: V1 Software

- Simple Django admin to import jobs, view results, override routes
- Migrate customer to dashboard
- Reduce hands-on to weekly check-ins

### Success Metrics (Track Weekly)

| Metric | Target |
|---|---|
| Miles per tech per day | -15% to -25% |
| Jobs per tech per day | +10% to +15% |
| Data quality | <5% jobs missing required fields |

If not hitting -10% miles by week 4, diagnose:
- Are they following the optimized routes?
- Are there constraints you missed (time windows, tech skills)?
- Is the data quality poor?

---

## Red Flags During Pilot (When to Walk Away)

- Won't provide data after multiple requests — not serious
- Techs ignore optimized routes and owner won't enforce — culture problem
- Savings are <5% — market too small or already efficient
- Owner ghosts you after week 2 — not engaged
- Asks for custom features before paying pilot fee — scope creep

**Do not discount. Do not extend beyond 90 days. Either convert to full price or part ways cleanly.**

---

## Management Commands to Build

```
python manage.py geocode_jobs --file=jobs.csv
python manage.py calculate_baseline --customer=acme_hvac
python manage.py optimize_routes --customer=acme_hvac --date=2026-04-15
python manage.py generate_report --customer=acme_hvac --week=2026-W16
```

Store in `apps/dispatch/management/commands/`.

---

## Final Notes

- **Do not over-engineer.** The first pilot can be entirely manual Python scripts and email.
- **Free audits are an investment, not charity.** Scope them tightly. The goal is a case study with dollar numbers.
- **Use your ML pedigree.** Every call, every deliverable should reinforce: "I've done this at production scale."
- **Be honest about limitations.** If you can't handle real-time rerouting yet, say so. Credibility beats overpromising.
- **Charge after the first case study.** If they won't pay $500 for analysis after seeing real results, move on.
