# Pricing Model: Gold linked BRC Autocallable
The model prices an autocallable Barrier Reverse Convertible from UBS AG, linked to gold. 

Product ISIN: CH1522817944

# 1. Product details:
Underlying: Gold spot

Product type: Autocallable Barrier Reverse Convertible

Coupon: 4.75% p.a., quarterly payments

Maturity: 1.5 years

Autocall: Quarterly observation from second quarter (100% of Initial Level required)

Barrier/Kick-In: 75% of Initial Level

# Structure of the code:

# 2. Simulate price paths:
Simulating future price paths in daily steps using Geometric Brownian Motion (GBM).

# 3. Payoff logic:
Payoff logic is according to the term sheet of the Product. In this case:

If autocall occurs:
Notional is repaid in full. All coupons until the date of the autocall are paid. The product ends early, later coupons will not be received.

If no autocall occurred: 

The product continues until maturity. Coupons are paid for all scheduled payment dates. At maturity, repayment of notional is path-dependent. Full notional is repaid if the underlying was never equal to or below the Kick-In Level. If the barrier was breached, redemption depends on the Expiration Price of the underlying. Full repayment if the Expiration Price is above the Strike Level. Otherwise proportional loss between the Expiration Price and the Strike Level.

# 4. Monte Carlo Pricing:
The model evaluates the payoff across a large number of simulated price paths. The discounted payoffs are averaged to estimate the fair present value of the product. Additionally, the model tracks the count of barrier breaches. This is used later to calculate the probability of a barrier breach.

# 5. Results:
The program outputs the estimated autocallable price and the percentage of simulation paths where a Kick-In event occurred.
