# Dashboard Visualization Layer

## Overview

Visualization layer for a C++ quantitative trading platform. These screenshots show system state monitoring for portfolio aggregation, strategy execution, and risk tracking.

---

## Screenshots

### 1. Dashboard Overview
**File:** `dashboard-overview.png`

Aggregated portfolio state and strategy activity:
- **Portfolio Summary** - NAV, daily PnL, net/gross exposure aggregated from all strategies
- **Active Strategies** - Strategy-level PnL, exposure, and heartbeat status
- **Recent Trades** - Execution flow from strategy signals to filled orders

**System State:**
- Portfolio NAV: $1,250,000
- Daily PnL: +$12,500 (aggregated across strategies)
- 3 active strategies (momentum-strategy-1, mean-reversion-1, arbitrage-1)
- Trade execution history

### 2. Strategy Detail
**File:** `strategy-detail.png`

Strategy-level monitoring and position tracking:
- **PnL History** - Cumulative PnL computed from executed trades
- **Position Breakdown** - Current positions held by strategy
- **Strategy Metrics** - Total return, drawdown, trade count
- **Recent Trades** - Strategy-specific execution history

**Tracked Metrics:**
- Total PnL: +$82,500
- Position count: 3 long
- Max Drawdown: -5.2%
- Trades executed: 127

### 3. Risk Dashboard
**File:** `risk-dashboard.png`

Portfolio-level risk aggregation and monitoring:
- **Portfolio Risk Metrics** - NAV, exposure, drawdown aggregated from position tracker
- **Position Concentration** - Exposure breakdown by asset
- **Risk by Strategy** - Gross exposure per strategy
- **Drawdown History** - Portfolio-level drawdown tracking
- **Risk Limits** - Position size, leverage, concentration monitoring

**Risk State:**
- Gross Exposure: $193,280
- Max Drawdown: -8.2%
- Concentration (top 3): 86.4%
- Leverage: 1.25x

### 4. Portfolio Analytics
**File:** `portfolio-analytics.png`

Performance attribution and aggregation:
- **Portfolio PnL** - Aggregated PnL across all strategies
- **Strategy Contribution** - PnL breakdown by strategy
- **PnL Breakdown** - Realized vs unrealized PnL
- **Monthly Aggregation** - Monthly aggregation of daily PnL

**Aggregated Metrics:**
- Total Return: +33.0%
- Total PnL: +$125,000
- Active strategies: 3
- Current NAV: $1,542,380

---

## Notes

These screenshots represent system output from a C++ trading platform. The visualization layer receives portfolio state, strategy updates, and execution data via IPC from the backend engine. Data shown is for demonstration purposes.

---

**Last Updated:** May 1, 2026
