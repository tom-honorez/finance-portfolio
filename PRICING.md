# Quantitative Pricing Component

This component is designed as a pricing layer within a trading and risk system, providing valuations and sensitivities that feed portfolio state, P&L and risk calculations.

---

## Capabilities

### Pricing Models
* Black-Scholes for European options valuation
* Support for calls and puts

### Risk Analytics
* Greeks calculation (Delta, Gamma, Vega, Theta, Rho)
* Position-level sensitivity analysis
* Portfolio risk aggregation

### Scenario Analysis
* Stress testing across market parameters
* What-if scenario evaluation
* Portfolio impact assessment

---

## Model Scope & Extensions

The current implementation focuses on Black-Scholes as a baseline model, with the design structured to support extension towards more advanced frameworks used in production environments:

* **Stochastic volatility models** (e.g. Heston)
* **Local volatility approaches** (Dupire-style)
* **Monte Carlo simulation** for path-dependent products
* **Multi-asset and cross-asset scenarios** (equity, FX, rates)

The goal is not isolated model implementation, but integration of pricing models within a consistent trading and risk system.

---

## System Integration

This pricing component integrates with the C++ trading platform to provide:

* **P&L calculations** - Mark-to-market valuations for positions
* **Risk monitoring** - Real-time exposure and sensitivity tracking
* **Portfolio analytics** - Scenario-based risk assessment

---

## Technical Implementation

* Pure Python implementation
* Vectorized calculations for performance
* Clean interfaces for system integration

---

> This component demonstrates quantitative modeling capabilities and system integration design.
