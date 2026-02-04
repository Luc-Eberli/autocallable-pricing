# Pricing Model: Gold linked BRC Autocallable
The model prices an Autocallable Barrier Reverse Convertible from UBS AG, linked to gold. 

Product ISIN: CH1522817944

# Product details:
Underlying: Gold spot

Product type: Autocallable Barrier Reverse Convertible

Coupon: 4.75% p.a., quarterly payments

Maturity: 1.5 years

Autocall: Quarterly observation from second quarter (100% of initial level required)

Barrier/Kick-in: 75% of initial level

# Structure of the code:

# 2. Simulate price paths:
Simulating future price paths in daily steps using Geometric Brownian Motion (GBM).

# 3. Payoff logic:
Payoff logic is according to the term sheet of the Product. In this case:

If autocall occurs:
Notional is repaid in full. All coupons until the date of the Autocall are paid. The product ends early, later coupons will not be received.

If no autocall occurred: 

The product continues until maturity. Coupons are paid for all scheduled payment dates. At maturity, repayment of notional is path-dependent. Full notional is repaid if the underlying was never equal to or below the kick-in level. If the barrier was breached, redemption depends on the expiration price of the underlying. Full repayment if the expiration price is above the strike level. Otherwise proportional loss between the expiration price and the strike level.

# 4. Monte Carlo Pricing:
The model evaluates the payoff across a large number of simulated price paths. The discounted payoffs are averaged to estimate the fair present value of the product. Additionally, the model tracks the count of barrier breaches. This is used later to calculate the probability of a barrier breach.

# 5. Results:
The program outputs the estimated Autocallable price and the percentage of simulation paths where a kick-in event occurred.
