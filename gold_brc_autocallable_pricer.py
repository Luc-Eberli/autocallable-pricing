#The model prices an Autocallable Barrier Reverse Convertible from UBS AG,
#linked to gold.

import math
import numpy as np
import numpy.random as npr

# 1. Parameters

#Market Parameters
S0 = 4611.05 # Reference Level
r = 0.0365 # Risk-free rate (USD overnight, SOFR-based)
volatility = 0.20 # Annualized gold volatility (historically between 15%-20%)

#Autocallable Parameters
calculation_amount = 1000
coupon = 0.0475 # coupon p.a.
cpn_payments_per_year = 4
days_per_year = 360
T = 1.5 # Maturity in years
early_redemption_level = 1.0 * S0 # Autocall level (100% of reference level)
kick_in_level = 0.75 * S0 # Level of kick-in (75% of reference level)

#Observation Dates 
coupon_payment_dates = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
autocall_dates = [0.5, 0.75, 1.0, 1.25]

#Simulation Parameters
I = int(50000) # Number of monte carlo paths 
breach_count = 0 # Counter for kick-in breaches
M = int(T * days_per_year) # Total number of time steps to have daily steps over 18 months
dt = 1 / days_per_year # Interval length / time steps once a day

# 2. GBM Random Price Path Simulation

# Create table for each timestep and path S[time step, number of path]. "+1" includes S0
S = np.zeros((M + 1, I)) 

# Set initial value to S0 for all paths
S[0] = S0 

for t in range(1, M + 1):
    # Recursive definition of next price step based on Geometric Brownian Motion (GBM)
    S[t] = S[t - 1] * np.exp((r - 0.5 * volatility ** 2) * dt + volatility * math.sqrt(dt) * npr.standard_normal(I))

# 3. Payoff of one path

def payoff_single_path(path):
    pv = 0.0  # present value accumulator

    # Calculate payoff, if autocall occurs
    for autocall_date in autocall_dates:
        day_of_autocall = int(autocall_date * days_per_year)
        if S[day_of_autocall, path] >= early_redemption_level:

            # Count together discounted coupon payments up to autocall
            for cpn_date in coupon_payment_dates:
                if cpn_date <= autocall_date:
                    coupon_payment = calculation_amount * (coupon / cpn_payments_per_year)
                    # Add discounted coupon payment to path payout
                    pv = pv + coupon_payment * math.exp(-r * cpn_date)

            # Repay discounted calculation amount at autocall
            pv = pv + calculation_amount * math.exp(-r * autocall_date)
            return pv

    # If no Autocall, check final payoff at maturity
    # Discounted coupon payments until maturity
    for cpn_date in coupon_payment_dates:
        coupon_payment = calculation_amount * (coupon / cpn_payments_per_year)
        pv = pv + coupon_payment * math.exp(-r * cpn_date)


    # Check if a kick-in has occurred and calculate payoff accordingly
    path_min = np.min(S[:, path])
    final_price = S[-1, path]
    if path_min > kick_in_level:
        # Kick-in event hasn't occurred
        pv = pv + calculation_amount * math.exp(-r * T)
    else:
        # Kick-in event occurred
        if final_price >= S0:
            pv = pv + calculation_amount * math.exp(-r * T)
        else:
            pv = pv + calculation_amount * (final_price / S0) * math.exp(-r * T)

    return pv

        
# 4. Monte Carlo Pricing

def monte_carlo_pricing():
    global breach_count
    breach_count = int(0) # Counter for kick-in breaches
    all_payoffs = []
    for i in range(I):
        payoff = payoff_single_path(i)
        all_payoffs.append(payoff)
        final_price = S[-1, i]
        if min(S[:, i]) < kick_in_level:
            breach_count = breach_count + 1

    return np.mean(all_payoffs)

# 5. Run Pricing

autocallable_price = monte_carlo_pricing()

print(f"Autocallable price: {autocallable_price:.2f}$")
print(f"Percentage of kick-in events: {breach_count / I * 100:.2f}%")
