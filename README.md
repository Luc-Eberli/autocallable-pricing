# Pricing Model: Gold linked BRC Autocallable
The model prices an Autocallable Barrier Reverse Convertible issued by UBS AG, linked to gold.

# Product Details:
Underlying: Gold spot

Product type: Autocallable Barrier Reverse Convertible

Coupon: 4.75% p.a., quarterly payments

Maturity: 1.5 years

Autocall: Quarterly observation at 100% of initial level

Barrier/Kick-in: 75% of initial level

# Structure of the code:

# 1. Simulate Pricepaths:
Simulated price paths in daily steps using Geometric Brownian Motion (GBM).

# 2. Payoff logic:
If autocall occurs, discounted coupon payments and notional repaid at autocall date. The product is terminated, later coupons won't be paid.

If no autocall, all coupons are paid and final payoff depends on barrier breach:

No breach: full notional returned

Barrier breached: final payoff proportional to underlying performance at maturity.

