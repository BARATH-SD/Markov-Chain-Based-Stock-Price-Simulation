# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 19:23:53 2025

@author: Barath

Project title: Stock Price Simulation using Markov Chains
Goal: Predicting price trends based on historical state transitions

"""
#**************************************
# Import Libraries
#**************************************

import yfinance as yf
import numpy as nm
import pandas as pd
import matplotlib.pyplot as plt
import random


#**************************************
# Download Stock Data
#**************************************

ticker='AAPL'                
start_date='2020-01-01'
end_date='2022-12-31'

data=yf.download(ticker,start_date,end_date)
closing_prices=data["Close"][ticker]      # Extract just the closing prices for analysis


#**************************************
# Convert Returns to Discrete States
#**************************************

returns=closing_prices.pct_change().dropna() #Calculates the percentage change
# +1 for up, -1 for down, 0 for neutral

def get_state(change, threshold=0.002):
    if change > threshold:
        return 1
    elif change < -threshold:
        return -1
    else:
        return 0

states = returns.apply(get_state)


#**************************************
# Build Transition Matrix
#**************************************

# Initialize a dictionary to count transitions between states
# Rows: current state, Columns: next state
transitions={
    -1:{-1:0,0:0,1:0},
    0:{-1:0,0:0,1:0},
    1:{-1:0,0:0,1:0}
}

for i in range(len(states)-1):
    current_st=states.iloc[i]
    next_st=states.iloc[i+1]
    transitions[current_st][next_st]+=1

#Normalize to create Probabilities
for current_st in transitions:
    total=sum(transitions[current_st].values())
    for next_st in transitions[current_st]:
        if total>0:
            transitions[current_st][next_st] /= total


#**************************************
# Run Multiple Simulations
#**************************************

n_days=30                              #No. of future days to simulate
simulations=100                         #No. of simulations

simulated_prices_matrix=[]

for i in range(simulations):
    initial_price=closing_prices.iloc[-1]   #Start with latest real price
    current_st=states.iloc[-1]              #Start with the last known state
    simulated_prices=[initial_price]        #each simulation generates a list of prices for n_days + 1 day (starting from the last real price)
    
    for j in range(n_days):
        probabs=list(transitions[current_st].values())  # probab of next possible state
        next_possible_states=[-1,0,1]
        next_st=random.choices(next_possible_states,weights=probabs)[0]  # Randomly choose the next state based on these probabilities
        current_st=next_st
        
        # Estimate next price based on assumed movement per state
        if next_st==1:
            next_price=simulated_prices[-1]*(1 + 0.1)    # 1% up
        elif next_st == -1:
            next_price=simulated_prices[-1]*(1 - 0.1)    # 1% down
        else:
            next_price=simulated_prices[-1]               # No change
    
        simulated_prices.append(next_price)
    simulated_prices_matrix.append(simulated_prices)

# now the simulation matrix contains 100 rows(simulations) wtih each having 31 days' prices
simul_df=pd.DataFrame(simulated_prices_matrix).T
simul_df.index.name='Day'
# Transpose makes columns as simulations and each row denoting the each day
# Hence the avg. price can be found be taking the mean of each row

#**************************************
# Compare with the future stock data
#**************************************
future_start='2022-12-30'
future_end='2023-02-20'    

future_data=yf.download(ticker,future_start,future_end)
future_prices=future_data['Close'].values[:n_days+1]

plt.figure(figsize=(10,6))

# Plot all simulations faintly
for i in range(simulations):                    
    plt.plot(simul_df[i],color='grey',alpha=0.1)

# Plot mean of simulations
plt.plot(simul_df.mean(axis=1),color='blue',label="Simulated Mean",linewidth=2)

# Plot actual prices
plt.plot(future_prices,color='green',label="Actual Prices",linewidth=2)

plt.title(f"{ticker}: Simulated vs Actual Prices ({n_days} Days)")
plt.xlabel("Day")
plt.ylabel("Price ($)")
plt.ylim(closing_prices.iloc[-1]-50,closing_prices.iloc[-1]+50)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()





