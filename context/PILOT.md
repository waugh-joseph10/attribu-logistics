# Pilot Evaluation & Build Framework

> **Purpose:** Validate pain, quantify ROI, and deliver value BEFORE building software
> **Timeline:** 2-3 weeks from first conversation to paid pilot
> **Outcome:** Either a paying customer with proven ROI or a clean "no" with lessons learned

---

## Phase 1: Qualification (First 48 Hours)

### Minimum Requirements Checklist

Use this to filter prospects in the first conversation:

- [ ] **Fleet size:** 15-100 technicians (sweet spot: 20-50)
- [ ] **Geography:** Service area is regional, not hyper-local (>50 mile radius)
- [ ] **Current dispatch:** Manual process (whiteboard, spreadsheet, or basic FSM software)
- [ ] **Decision maker:** You're talking to owner, ops manager, or someone who can sign a $500-1K check
- [ ] **Data access:** They can export job history (CSV, API, or manual extraction)
- [ ] **Pain language:** They use dollar figures when describing routing problems ("we waste X hours/week")

### Red Flags (Walk Away)

- Fleet is <10 techs (too small, can't prove ROI)
- Fleet is >200 techs (too complex for manual MVP, sales cycle too long)
- Service area is <20 mile radius (routing delta is negligible)
- "It would be nice to optimize" language (vitamin, not painkiller)
- No one can export job data (you'll spend weeks on data extraction)
- Decision maker is 3+ levels removed from operations

### Qualification Questions

Ask these in the first call:

1. **"Walk me through how you dispatch technicians today."**
   - Listen for: manual steps, pain points, time spent

2. **"How many jobs does an average tech complete per day?"**
   - Baseline metric for improvement calculation

3. **"What does a bad dispatch day cost you?"**
   - If they can't answer in dollars, the pain isn't acute enough

4. **"Have you tried to solve this before? What happened?"**
   - Learn what didn't work, surface objections early

5. **"Can you export the last 30 days of job data?"**
   - If yes → proceed. If no → ask what systems they use and if API access exists

6. **"If I can show you exactly where you're losing money and how to fix it, would you pay $500-1K for that analysis?"**
   - This is the filter. If no → thank them and move on.

---

## Phase 2: Data Collection (Week 1)

### Required Data Fields

You need this to run any meaningful analysis:

| Field | Required? | Format | Example |
|---|---|---|---|
| Job ID | Yes | Text/Number | `JOB-12345` |
| Job Date | Yes | Date | `2026-04-15` |
| Job Start Time | Yes | Time | `09:30` |
| Job End Time | Yes | Time | `11:15` |
| Service Address | Yes | Full address | `123 Main St, Austin TX 78701` |
| Assigned Technician | Yes | Tech ID/Name | `TECH-042` or `John Smith` |
| Job Type | Preferred | Category | `HVAC Repair`, `Install`, `Maintenance` |
| Skill Required | Preferred | Text | `HVAC Level 2`, `Electrical` |
| Time Window | Preferred | Time range | `8am-12pm` or `anytime` |
| Priority | Optional | High/Med/Low | `High` |
| Parts Needed | Optional | Boolean | `Yes/No` |

### Data Collection Email Template

```
Subject: Data request for route optimization analysis

Hi [Name],

To run the analysis we discussed, I need the last 30 days of completed jobs. Specifically:

- Job ID
- Date and time (start + end)
- Service address
- Which tech was assigned
- Job type (if tracked)

A CSV export from [ServiceTitan/Housecall Pro/their system] works great. If you need help pulling this, let me know and I can walk you through it.

Once I have this, I'll deliver the analysis within 5 business days.

— Joe
joe@attribu.io
```

### Data Quality Checks

When you receive the data, validate immediately:

```python
import pandas as pd

# Load data
df = pd.read_csv('customer_jobs.csv')

# Check required fields
required = ['job_id', 'date', 'start_time', 'end_time', 'address', 'tech_id']
missing = [col for col in required if col not in df.columns]
if missing:
    print(f"❌ Missing required columns: {missing}")

# Check for nulls
null_counts = df[required].isnull().sum()
if null_counts.any():
    print(f"⚠️  Null values found:\n{null_counts[null_counts > 0]}")

# Check date range
print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
print(f"📊 Total jobs: {len(df)}")
print(f"👷 Unique techs: {df['tech_id'].nunique()}")

# Flag duplicates
dupes = df[df.duplicated(subset=['job_id'], keep=False)]
if len(dupes) > 0:
    print(f"⚠️  {len(dupes)} duplicate job IDs found")
```

If data quality is poor (>20% nulls, inconsistent addresses, missing techs), **stop here** and request a cleaner extract. Bad data = bad analysis = lost credibility.

---

## Phase 3: Manual Optimization Analysis (Week 1-2)

### Step 1: Geocode All Addresses

Use a simple geocoding script to convert addresses to lat/long:

```python
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Initialize geocoder (free, no API key needed for small datasets)
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

# Save geocoded data
df.to_csv('customer_jobs_geocoded.csv', index=False)
```

For production or larger datasets, use Google Maps Geocoding API (requires billing but more accurate).

### Step 2: Calculate Baseline Metrics

Before optimization, measure what they're currently achieving:

```python
import numpy as np

# Group by technician and date
daily_tech = df.groupby(['tech_id', 'date']).agg({
    'job_id': 'count',  # jobs per day
    'start_time': 'min',  # first job start
    'end_time': 'max',  # last job end
}).rename(columns={'job_id': 'jobs_per_day'})

# Calculate working hours
daily_tech['hours_worked'] = (
    pd.to_datetime(daily_tech['end_time']) -
    pd.to_datetime(daily_tech['start_time'])
).dt.total_seconds() / 3600

# Average metrics
baseline_jobs_per_day = daily_tech['jobs_per_day'].mean()
baseline_hours = daily_tech['hours_worked'].mean()

print(f"📊 BASELINE METRICS")
print(f"Avg jobs/tech/day: {baseline_jobs_per_day:.1f}")
print(f"Avg working hours: {baseline_hours:.1f}")
```

Calculate drive time and distance (this is what you're optimizing):

```python
from geopy.distance import geodesic

def calculate_route_distance(tech_jobs):
    """Calculate total distance for a tech's daily route"""
    if len(tech_jobs) < 2:
        return 0

    total_distance = 0
    for i in range(len(tech_jobs) - 1):
        start = (tech_jobs.iloc[i]['lat'], tech_jobs.iloc[i]['lon'])
        end = (tech_jobs.iloc[i+1]['lat'], tech_jobs.iloc[i+1]['lon'])
        total_distance += geodesic(start, end).miles

    return total_distance

# Calculate daily drive distance per tech
df_sorted = df.sort_values(['tech_id', 'date', 'start_time'])
daily_distance = df_sorted.groupby(['tech_id', 'date']).apply(
    calculate_route_distance
).reset_index(name='total_miles')

baseline_miles_per_day = daily_distance['total_miles'].mean()
print(f"Avg miles/tech/day: {baseline_miles_per_day:.1f}")
```

### Step 3: Run Optimization (OR-Tools)

This is where your FedEx experience shines. Use Google OR-Tools to compute optimized routes:

```python
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np

def create_distance_matrix(locations):
    """Create distance matrix from lat/lon coordinates"""
    n = len(locations)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = geodesic(locations[i], locations[j]).miles

    return matrix

def solve_vrp(distance_matrix, num_vehicles, depot=0):
    """Solve Vehicle Routing Problem with OR-Tools"""

    # Create routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix),
        num_vehicles,
        depot
    )

    # Create routing model
    routing = pywrapcp.RoutingModel(manager)

    # Create distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node] * 100)  # scale for int

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = 30

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    return manager, routing, solution

# Example: Optimize one day for one tech
sample_day = df[
    (df['tech_id'] == 'TECH-001') &
    (df['date'] == '2026-04-15')
].copy()

locations = list(zip(sample_day['lat'], sample_day['lon']))
distance_matrix = create_distance_matrix(locations)

manager, routing, solution = solve_vrp(
    distance_matrix,
    num_vehicles=1,
    depot=0  # assume first job is depot/home base
)

# Extract optimized route
if solution:
    index = routing.Start(0)
    optimized_route = []
    total_distance = 0

    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        optimized_route.append(node)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        total_distance += routing.GetArcCostForVehicle(
            previous_index, index, 0
        )

    optimized_miles = total_distance / 100  # unscale
    original_miles = calculate_route_distance(sample_day)

    print(f"Original route: {original_miles:.1f} miles")
    print(f"Optimized route: {optimized_miles:.1f} miles")
    print(f"Savings: {original_miles - optimized_miles:.1f} miles ({(1 - optimized_miles/original_miles)*100:.1f}%)")
```

### Step 4: Scale to Full Dataset

Run optimization across all techs and all days in the dataset:

```python
results = []

for (tech, date), group in df.groupby(['tech_id', 'date']):
    if len(group) < 2:
        continue  # skip single-job days

    locations = list(zip(group['lat'], group['lon']))
    distance_matrix = create_distance_matrix(locations)

    manager, routing, solution = solve_vrp(distance_matrix, num_vehicles=1)

    if solution:
        # Calculate optimized distance
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

### Fuel Savings

```python
# Assumptions (adjust based on customer's actual costs)
FUEL_COST_PER_GALLON = 3.50  # national avg
MPG = 15  # typical service vehicle

# Calculate monthly fuel savings
avg_daily_savings_miles = results_df['savings_miles'].mean()
num_techs = df['tech_id'].nunique()
work_days_per_month = 22

monthly_miles_saved = avg_daily_savings_miles * num_techs * work_days_per_month
monthly_gallons_saved = monthly_miles_saved / MPG
monthly_fuel_savings = monthly_gallons_saved * FUEL_COST_PER_GALLON

annual_fuel_savings = monthly_fuel_savings * 12

print(f"💰 FUEL SAVINGS")
print(f"Avg miles saved per tech per day: {avg_daily_savings_miles:.1f}")
print(f"Monthly fuel savings: ${monthly_fuel_savings:,.0f}")
print(f"Annual fuel savings: ${annual_fuel_savings:,.0f}")
```

### Labor Time Savings

```python
# Assumptions
AVG_SPEED_MPH = 25  # urban/suburban service area
HOURLY_LABOR_COST = 35  # loaded cost (wage + benefits)

# Calculate time savings
avg_daily_time_saved_hours = avg_daily_savings_miles / AVG_SPEED_MPH
monthly_hours_saved = avg_daily_time_saved_hours * num_techs * work_days_per_month
monthly_labor_savings = monthly_hours_saved * HOURLY_LABOR_COST

annual_labor_savings = monthly_labor_savings * 12

print(f"⏱️  LABOR TIME SAVINGS")
print(f"Avg time saved per tech per day: {avg_daily_time_saved_hours * 60:.0f} min")
print(f"Monthly labor savings: ${monthly_labor_savings:,.0f}")
print(f"Annual labor savings: ${annual_labor_savings:,.0f}")
```

### Capacity Increase (Jobs Per Tech)

```python
# Calculate how many additional jobs could fit in saved time
AVG_JOB_DURATION_HOURS = df.groupby('job_id').apply(
    lambda x: (
        pd.to_datetime(x['end_time'].iloc[0]) -
        pd.to_datetime(x['start_time'].iloc[0])
    ).total_seconds() / 3600
).mean()

additional_jobs_per_day = avg_daily_time_saved_hours / AVG_JOB_DURATION_HOURS
monthly_additional_jobs = additional_jobs_per_day * num_techs * work_days_per_month

# Assume 60% of freed capacity converts to actual jobs (conservative)
realized_additional_jobs = monthly_additional_jobs * 0.6

# Revenue impact (customer-specific)
AVG_JOB_REVENUE = 250  # typical service call - UPDATE THIS
monthly_revenue_increase = realized_additional_jobs * AVG_JOB_REVENUE
annual_revenue_increase = monthly_revenue_increase * 12

print(f"📈 CAPACITY INCREASE")
print(f"Additional jobs per tech per day (potential): {additional_jobs_per_day:.2f}")
print(f"Realized additional jobs per month: {realized_additional_jobs:.0f}")
print(f"Monthly revenue increase: ${monthly_revenue_increase:,.0f}")
print(f"Annual revenue increase: ${annual_revenue_increase:,.0f}")
```

### Total ROI Summary

```python
total_annual_savings = annual_fuel_savings + annual_labor_savings
total_annual_impact = total_annual_savings + annual_revenue_increase

print(f"\n💎 TOTAL ANNUAL IMPACT")
print(f"Fuel savings: ${annual_fuel_savings:,.0f}")
print(f"Labor savings: ${annual_labor_savings:,.0f}")
print(f"Revenue increase: ${annual_revenue_increase:,.0f}")
print(f"—" * 40)
print(f"TOTAL: ${total_annual_impact:,.0f}")
print(f"\nROI at $3,000/month software cost:")
print(f"Annual cost: $36,000")
print(f"Annual benefit: ${total_annual_impact:,.0f}")
print(f"Net benefit: ${total_annual_impact - 36000:,.0f}")
print(f"ROI: {(total_annual_impact / 36000 - 1) * 100:.0f}%")
```

---

## Phase 5: Deliverables

### What You Deliver to the Customer

Create a simple PDF report (use a Jupyter notebook + nbconvert, or a Google Doc):

**1. Executive Summary (1 page)**
- Current state: X jobs/day, Y miles/tech, Z hrs driving
- Optimized state: +A jobs/day, -B% miles, -C hrs wasted
- Dollar impact: $D/month, $E/year
- Recommended next step: 90-day pilot at $500/month

**2. Detailed Findings (2-3 pages)**
- Baseline metrics with charts
- Optimization methodology (high-level, not code)
- Day-by-day comparison for sample week
- Map visualization (before/after routes for 1-2 techs)

**3. Implementation Plan (1 page)**
- What a software solution would look like
- Timeline: 4-6 weeks to V1
- Pilot terms: $500/month for 90 days, then $2,500/month
- Success criteria: achieve 75%+ of projected savings

### Visual: Before/After Route Map

Use `folium` to create interactive maps:

```python
import folium

# Pick one representative day
sample_tech = results_df.sort_values('savings_pct', ascending=False).iloc[0]['tech_id']
sample_date = results_df.sort_values('savings_pct', ascending=False).iloc[0]['date']

sample_jobs = df[(df['tech_id'] == sample_tech) & (df['date'] == sample_date)].copy()

# Create map centered on jobs
center_lat = sample_jobs['lat'].mean()
center_lon = sample_jobs['lon'].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

# Plot original route (red)
original_coords = list(zip(sample_jobs['lat'], sample_jobs['lon']))
folium.PolyLine(original_coords, color='red', weight=3, opacity=0.7, popup='Original Route').add_to(m)

# Plot optimized route (green) - would need to store optimized order
# optimized_coords = [original_coords[i] for i in optimized_route_order]
# folium.PolyLine(optimized_coords, color='green', weight=3, opacity=0.7, popup='Optimized Route').add_to(m)

# Add markers for each job
for idx, row in sample_jobs.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=6,
        popup=f"Job {row['job_id']}",
        color='blue',
        fill=True
    ).add_to(m)

m.save('route_comparison.html')
```

Send them this HTML file or embed screenshot in the PDF.

---

## Phase 6: Pilot Pricing & Contract

### Pricing Tiers

| Fleet Size | Pilot (90 days) | Full Price | Annual Savings (est) |
|---|---|---|---|
| 15-20 techs | $500/month | $1,500/month | $90K-$120K |
| 21-40 techs | $750/month | $2,500/month | $150K-$220K |
| 41-80 techs | $1,000/month | $4,000/month | $250K-$400K |

### Pilot Terms (Send This via Email)

```
Subject: Pilot Agreement — Route Optimization for [Company Name]

Hi [Name],

Based on our analysis, I'm confident we can save you $[X]/year in fuel and labor costs through intelligent dispatch optimization.

Here's what I'm proposing:

90-Day Pilot: $[500-1000]/month
- Daily optimized dispatch recommendations delivered by 6am
- Weekly performance reports (miles saved, time saved, jobs per tech)
- Direct access to me for adjustments and questions
- Cancel anytime if you don't see at least 5x ROI

After Pilot: $[1500-4000]/month based on fleet size
- Only convert if you're seeing real savings
- Month-to-month, no long-term contract

Next Steps:
1. Reply "yes" to this email to start
2. I'll send a simple service agreement and invoice
3. We'll do a kickoff call to integrate with your dispatch process
4. First optimized routes delivered within 5 business days

Sound good?

— Joe
joe@attribu.io
```

### Simple Service Agreement

Keep it to 1 page. Key terms:
- Services: Daily route optimization recommendations
- Term: 90 days, auto-renews month-to-month
- Payment: Due on 1st of month, net 15
- Termination: Either party, 30 days notice
- Liability: Limited to fees paid in prior 3 months
- No SLA (this is a pilot, manage expectations)

Use Docusign or PandaDoc for electronic signature.

---

## Phase 7: Pilot Delivery (Manual → Software Transition)

### Weeks 1-2: Manual Delivery

- Export their jobs each evening (API integration if possible, otherwise CSV)
- Run optimization script overnight
- Email optimized dispatch schedule by 6am
- Include: tech assignments, recommended order, map view
- Weekly check-in: "Here's what we saved you this week"

### Weeks 3-4: Semi-Automated

- Build a Django management command that runs the optimization script
- Set up Celery Beat to run it nightly at midnight
- Auto-send email with results
- Still manually review output before it goes out (catch edge cases)

### Weeks 5-8: Full V1 Software

- Build simple Django admin interface to:
  - Import jobs (CSV upload or API sync)
  - View optimization results
  - Override/adjust routes manually
  - See historical performance
- Migrate customer to self-service dashboard
- Reduce hands-on involvement to weekly check-ins

### Success Metrics to Track Weekly

| Metric | Target |
|---|---|
| Miles per tech per day | -15% to -25% |
| Jobs per tech per day | +10% to +15% |
| Customer satisfaction | Weekly check-in, NPS-style |
| Data quality | <5% jobs missing required fields |

If you're not hitting at least -10% miles or +5% jobs by week 4, diagnose why:
- Are they following the optimized routes?
- Are there constraints you missed (customer time windows, tech skills)?
- Is the data quality poor?

---

## Red Flags During Pilot (When to Walk Away)

- Customer won't provide data after multiple requests (not serious)
- Techs refuse to follow optimized routes and owner won't enforce (culture problem)
- Savings are <5% (market is too small or too efficient already)
- Owner ghosts you after week 2 (not engaged)
- They ask for custom features before paying pilot fee (scope creep)

**Do not discount. Do not extend the pilot beyond 90 days. Either convert to full price or part ways.**

---

## Key Scripts to Build

Create these as Django management commands:

1. `python manage.py geocode_jobs --file=jobs.csv`
2. `python manage.py calculate_baseline --customer=acme_hvac`
3. `python manage.py optimize_routes --customer=acme_hvac --date=2026-04-15`
4. `python manage.py generate_report --customer=acme_hvac --week=2026-W16`

Store in `apps/dispatch/management/commands/`.

---

## Next Steps for You

1. **Build the optimization script first** (before you have a customer). Test it on synthetic data or public datasets.
2. **Create report templates** (Jupyter notebook or Google Doc template with placeholders).
3. **Write the qualification email** and start sending it to 20 prospects.
4. **When someone says yes to the $500-1K audit:** Use this framework to deliver in 5 business days.
5. **Iterate based on feedback.** If 3 customers all ask for the same constraint (e.g., "my techs can't work past 5pm"), add it to the model.

---

## Final Notes

- **Do not over-engineer.** The first pilot can be entirely manual with Python scripts and email. That's fine.
- **Charge for the audit.** If they won't pay $500 for analysis, they won't pay $2,500/month for software.
- **Use your FedEx pedigree.** Every email, every call, every deliverable should reinforce "I've done this at scale."
- **Be honest about limitations.** If you can't handle a constraint (e.g., real-time rerouting), say so. Credibility > overpromising.

You don't need perfect software to prove value. You need clean data, solid math, and a customer who feels the pain.
