# RevOps, pipeline, and GTM metrics

Use this module when diagnosing stage flow, lifecycle design, handoffs, pipeline coverage, conversion, speed, or revenue reporting.

## Define the operating model first

Before calculating or changing anything, establish the business's actual lifecycle, stage meanings, ownership rules, qualification criteria, win/loss states, revenue basis, and reporting period. Map lead-to-customer handoffs and feedback to marketing, sales, and post-sale teams. Treat unfamiliar frameworks (including MEDDIC or WbD) as optional lenses, not as required company methodology.

## Stage design

For each relevant stage, record:

1. entry evidence;
2. the outcome the stage is meant to represent;
3. owner and next action;
4. objective exit evidence for advancing or closing;
5. allowed time or aging interpretation, sourced from the organization;
6. reporting denominator and exclusions.

Stage names alone do not prove consistent usage. Sample current records, compare activity and field evidence, and document exception cases. Keep process cleanup separate from reclassification unless the user authorizes data edits.

## Metric contract

Each metric needs a name, explicit numerator and denominator, population, time window, timestamp definition, exclusions, source fields, freshness, and owner. Examples to define from local data include stage conversion, time between milestones, lead response latency, aging, win/loss mix, pipeline by expected close period, and forecast error. State missingness and sample size; avoid false precision.

## Forecast and coverage

Use the organization's own forecast categories and historical snapshots. If snapshots or calibration data do not exist, label a forecast as a current-data estimate and state that accuracy cannot be validated. Coverage needs a named target, window, denominator, and rules for open/qualified pipeline. Do not import a 3x/4x coverage target or any probability uplift from a source skill as a default.

## Prioritization

Locate the earliest constraint supported by evidence. Compare plausible causes such as demand quality, qualification, speed, stage definitions, owner capacity, follow-up, data completeness, or customer fit. Rank interventions by expected user value, evidence, effort, dependencies, reversibility, and risk. Do not assign numeric scores unless the scoring rubric is defined and calibrated for this business.
