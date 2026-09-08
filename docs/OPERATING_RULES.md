# Operating Rules

## Economic gate
A job is accepted only when:

`sale price - provider cost - payment fees - other direct costs >= minimum contribution`

The system must calculate this before committing to fulfillment.

## Provider routing
Rank qualified providers using expected economics, quality, reliability, SLA, revision history, refund history, and recent performance.

A cheap provider with poor reliability is not preferred over a slightly more expensive provider with materially better expected completion.

## Failure handling
- Provider misses SLA → reassign when feasible.
- QA failure → request correction or reassign.
- Repeated provider failures → lower score and suspend when thresholds are crossed.
- Margin becomes negative before fulfillment → stop and escalate rather than silently absorbing the loss.

## Compliance
Do not automate prohibited actions on third-party marketplaces. Do not scrape protected data, create deceptive accounts, spam proposals, fabricate reviews, or misrepresent subcontracting. Use approved APIs and direct relationships where possible.
