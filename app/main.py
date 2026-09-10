from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, Field
from pathlib import Path
import json

app = FastAPI(title='Service Arbitrage Engine', version='0.2.0')

OFFER = {
    'id': 'business-flyer-design',
    'name': 'Business Flyer Design',
    'sale_price': 99.0,
    'fulfillment_ceiling': 35.0,
    'assumed_payment_fees': 4.0,
    'minimum_contribution': 40.0,
    'turnaround_business_days': 3,
    'revisions': 1,
    'scope': ['1 custom single-page business flyer','1 revision round','print-ready PDF','web-ready PNG or JPG','up to 3 business-day turnaround after complete intake'],
}

class MarginRequest(BaseModel):
    sale_price: float = Field(gt=0)
    fulfillment_cost: float = Field(ge=0)
    payment_fees: float = Field(default=0, ge=0)
    other_costs: float = Field(default=0, ge=0)
    minimum_contribution: float = Field(default=40, gt=0)

class Provider(BaseModel):
    provider_id: str
    name: str
    cost: float = Field(gt=0)
    quality_score: float = Field(ge=0, le=100)
    reliability_score: float = Field(ge=0, le=100)
    sla_hours: int = Field(gt=0)

class OrderPreflight(BaseModel):
    customer_email: EmailStr
    business_name: str = Field(min_length=1, max_length=120)
    headline: str = Field(min_length=1, max_length=160)
    body_copy: str = Field(min_length=1, max_length=2500)
    call_to_action: str = Field(min_length=1, max_length=180)
    brand_colors: str = ''
    website_or_phone: str = ''
    fulfillment_cost_estimate: float = Field(default=35.0, ge=0)

APPROVED_PROVIDER_STATUSES = {'approved', 'production_approved'}
MIN_APPROVED_PROVIDERS = 2

def provider_readiness():
    path = Path(__file__).resolve().parent.parent / 'config' / 'provider_candidates.json'
    try:
        roster = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {'approved_provider_count': 0, 'required_provider_count': MIN_APPROVED_PROVIDERS, 'payment_ready': False}
    approved = [p for p in roster.get('candidates', []) if p.get('status') in APPROVED_PROVIDER_STATUSES]
    return {'approved_provider_count': len(approved), 'required_provider_count': MIN_APPROVED_PROVIDERS, 'payment_ready': len(approved) >= MIN_APPROVED_PROVIDERS}

def margin_result(req: MarginRequest):
    contribution = req.sale_price - req.fulfillment_cost - req.payment_fees - req.other_costs
    margin_pct = contribution / req.sale_price * 100
    return {'sale_price': round(req.sale_price,2), 'fulfillment_cost': round(req.fulfillment_cost,2), 'contribution': round(contribution,2), 'contribution_margin_pct': round(margin_pct,1), 'accepted': contribution >= req.minimum_contribution}

@app.get('/health')
def health():
    return {'status':'ok','service':'service-arbitrage-engine','version':'0.2.0','offer':OFFER['id']}

@app.get('/offer')
def offer(): return OFFER

@app.post('/margin/check')
def margin_check(req: MarginRequest): return margin_result(req)

@app.post('/providers/rank')
def rank_providers(providers: list[Provider]):
    eligible=[p for p in providers if p.cost <= OFFER['fulfillment_ceiling']]
    ranked=sorted(eligible,key=lambda p:(((p.quality_score/100)*(p.reliability_score/100))/max(p.cost,1))*(1/max(p.sla_hours,1)),reverse=True)
    return {'eligible_count':len(ranked),'providers':ranked}

@app.get('/payment/readiness')
def payment_readiness():
    return provider_readiness()

@app.post('/orders/preflight')
def order_preflight(order: OrderPreflight):
    readiness = provider_readiness()
    if not readiness['payment_ready']:
        raise HTTPException(status_code=409, detail=f"Payment remains disabled until {MIN_APPROVED_PROVIDERS} providers are production-approved; currently {readiness['approved_provider_count']} approved.")
    if order.fulfillment_cost_estimate > OFFER['fulfillment_ceiling']:
        raise HTTPException(status_code=409, detail='Fulfillment estimate exceeds the $35 ceiling; reprice or reject before accepting payment.')
    result=margin_result(MarginRequest(sale_price=OFFER['sale_price'],fulfillment_cost=order.fulfillment_cost_estimate,payment_fees=OFFER['assumed_payment_fees'],minimum_contribution=OFFER['minimum_contribution']))
    if not result['accepted']:
        raise HTTPException(status_code=409, detail='Order does not meet the minimum contribution requirement.')
    return {'accepted':True,'state':'PAYMENT_READY','offer_id':OFFER['id'],'sale_price':OFFER['sale_price'],'projected_contribution':result['contribution'],'scope_locked':True,'intake':order.model_dump(exclude={'fulfillment_cost_estimate'})}

@app.get('/', response_class=HTMLResponse)
def landing():
    return HTMLResponse('''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Business Flyer Design — $99</title><style>body{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#f5f6f8;color:#13213a}.wrap{max-width:900px;margin:auto;padding:30px 20px}.hero{background:#13213a;color:white;border-radius:24px;padding:40px}.eyebrow{color:#e2bd62;font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:12px}h1{font-size:clamp(38px,7vw,64px);line-height:1;margin:12px 0 18px}.lead{font-size:19px;line-height:1.5;color:#e7ebf2}.grid{display:grid;grid-template-columns:1.2fr .8fr;gap:22px;margin-top:22px}.card{background:white;border-radius:20px;padding:26px;box-shadow:0 10px 30px #00000010}.price{font-size:46px;font-weight:850;margin:0}.check{list-style:none;padding:0}.check li{padding:8px 0;border-bottom:1px solid #eef1f4}.check li:before{content:'✓';margin-right:10px;font-weight:900;color:#18794e}.note{color:#667085;font-size:14px}.cta{display:block;background:#13213a;color:white;text-decoration:none;text-align:center;padding:15px;border-radius:10px;font-weight:800;margin-top:16px}@media(max-width:720px){.grid{grid-template-columns:1fr}.hero{padding:28px}}</style></head><body><div class="wrap"><section class="hero"><div class="eyebrow">Fixed scope • fixed price</div><h1>A polished business flyer without the agency price tag.</h1><p class="lead">Send your message, brand direction and call to action. Receive one custom flyer in print-ready and web-ready formats.</p></section><div class="grid"><section class="card"><h2>Included</h2><ul class="check"><li>1 custom single-page business flyer</li><li>1 revision round</li><li>Print-ready PDF</li><li>Web-ready PNG or JPG</li><li>Up to 3 business-day turnaround after complete intake</li></ul><p class="note">Additional concepts, pages, rush delivery, copywriting, or extra revisions are outside the $99 scope and require a separate quote.</p></section><aside class="card"><p class="price">$99</p><p>One-time fixed-price service.</p><p class="note">Ordering opens only after provider capacity and margin are confirmed.</p><a class="cta" href="/docs#/default/order_preflight_orders_preflight_post">Start order preflight</a></aside></div></div></body></html>''')
