# Service Arbitrage Engine

Automated system for selling fixed-scope digital services at a price above the fully loaded fulfillment cost, while routing each job to qualified providers.

## Initial operating model
Example launch offer: **Business Flyer Design — $99**.

Default fulfillment ceiling: **$35**.

The engine must reject or reprice jobs when expected contribution margin, delivery time, or provider reliability falls below configured thresholds.

## Core flow
Customer → Offer → Payment → Intake → Margin Gate → Provider Selection → Fulfillment → QA → Delivery → Review/Retention.

## Provider scorecard
Each provider is scored on:
- price
- quality
- speed/SLA
- revision rate
- customer satisfaction
- refund rate
- reliability

Provider selection optimizes expected contribution × reliability, not simply lowest cost.

## Rules
- Never sell work outside advertised scope.
- Never misrepresent fulfillment or ownership.
- Never fabricate reviews or testimonials.
- Never use unauthorized marketplace bots, scraping, fake accounts, or proposal spam.
- Prefer APIs and direct provider relationships where available.
- Remove providers that repeatedly miss quality or SLA thresholds.
- Keep every routing and margin decision auditable.
