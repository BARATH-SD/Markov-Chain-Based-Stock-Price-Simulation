# 📈 Markov Chain-Based Stock Price Simulation

A project that models and simulates future stock prices using a **discrete-state Markov Chain**, based on historical return patterns. Simulations are used to estimate future trajectories and compare with actual price movements.

---

## 🔍 Objective

To simulate the next *N* days of a stock's price (e.g., AAPL) using historical returns converted into **discrete states** (`-1`, `0`, `1`) and generate multiple simulation paths using a **transition probability matrix**.

---

## 🛠️ Tools & Technologies

- **Python**
- `pandas`, `numpy`, `matplotlib`
- `yfinance` (for historical stock data)

---

## 🧠 Methodology

1. **Data Acquisition**  
   Downloaded historical stock prices (AAPL, 2020–2023) using `yfinance`.

2. **Return Calculation**  
   Computed daily returns as percentage changes of closing prices.

3. **State Discretization**  
   Assigned states:  
   - `1` if return > +0.2%  
   - `0` if return ∈ [−0.2%, +0.2%]  
   - `-1` if return < −0.2%

4. **Transition Matrix Construction**  
   Built a `3x3` state transition probability matrix from historical state sequences.

5. **Future Simulation**  
   Simulated **100 future paths** over **30 days** using Markov transitions.

6. **Evaluation & Visualization**  
   - Calculated the mean of all simulations.  
   - Compared simulated averages to actual price trajectory (if available).  
   - Plotted simulations and real prices.

---

## 📊 Results

- Simulation trajectories broadly follow the short-term trend but diverge significantly over longer horizons.
- The discrete-state assumption limits precision but offers interpretability.
- Project highlights limitations of Markovian memoryless assumptions in financial modeling.

---

## 📁 Folder Structure

