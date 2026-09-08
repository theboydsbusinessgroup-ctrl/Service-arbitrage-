from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Service Arbitrage Engine", version="0.1.0")

class MarginRequest(BaseModel):
    sale_price: float = Field(gt=0)
    fulfillment_cost: float = Field(ge=0)
    payment_fees: float = Field(default=0, ge=0)
    other_costs: float = Field(default=0, ge=0)
    minimum_contribution: float = Field(default=40, ge=0)

class Provider(BaseModel):
    provider_id: str
    name: str
    cost: float = Field(ge=0)
    quality_score: float = Field(ge=0, le=100)
    reliability_score: float = Field(ge=0, le=100)
    sla_hours: int = Field(gt=0)

@app.get("/health")
def health():
    return {"status": "ok", "service": "service-arbitrage-engine", "version": "0.1.0"}

@app.post("/margin/check")
def margin_check(req: MarginRequest):
    contribution = req.sale_price - req.fulfillment_cost - req.payment_fees - req.other_costs
    return {
        "sale_price": req.sale_price,
        "contribution": round(contribution, 2),
        "accepted": contribution >= req.minimum_contribution,
    }

@app.post("/providers/rank")
def rank_providers(providers: list[Provider]):
    ranked = sorted(
        providers,
        key=lambda p: ((p.quality_score / 100) * (p.reliability_score / 100)) / max(p.cost, 1),
        reverse=True,
    )
    return ranked
