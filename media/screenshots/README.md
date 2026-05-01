# 📸 Dashboard Screenshots

## Overview

Screenshots of the trading dashboard desktop application built with React, TypeScript, and Electron.

---

## Screenshots

### 1. Dashboard Overview
**File:** `dashboard-overview.png`

Main dashboard view showing:
- **Portfolio Summary** - Total value, daily P&L, and performance metrics
- **Active Strategies** - List of running trading strategies with status and metrics
- **Recent Trades** - Real-time trade execution history

**Key Features:**
- Portfolio value: $1,250,000.50
- Daily P&L: +$12,500.75 (+1.01%)
- 3 active strategies (Momentum, Mean Reversion, Arbitrage)
- Real-time trade blotter
- Strategy health monitoring

### 2. Strategy Detail
**File:** `strategy-detail.png`

Detailed strategy analysis with visualizations:
- **Equity Curve** - Strategy performance over time
- **Daily P&L Chart** - Bar chart showing daily profits/losses
- **Position Breakdown** - Pie chart of current positions
- **Performance Metrics** - Sharpe ratio, Sortino ratio, win rate, profit factor
- **Current Positions Table** - Live positions with P&L

**Key Metrics:**
- Total P&L: +$125,450.75
- Sharpe Ratio: 2.15
- Win Rate: 62.3% (1,247 trades)
- Max Drawdown: -8.5%

### 3. Risk Dashboard
**File:** `risk-dashboard.png`

Real-time risk monitoring and analysis:
- **Exposure by Asset** - Bar chart showing position sizes
- **Drawdown History** - Historical drawdown tracking
- **Sector Exposure** - Pie chart of sector allocation
- **Risk Limits** - Progress bars for various risk metrics
- **Position Risk Table** - VaR, Beta, Volatility per position

**Risk Metrics:**
- Portfolio VaR (95%): $45,250
- Max Drawdown: -12.3%
- Concentration Risk: Medium
- Leverage: 1.25x

---

## Technical Stack

**Frontend:**
- React 19+ with TypeScript
- TailwindCSS for styling
- Electron for desktop application
- Real-time data updates via IPC

**Design:**
- Clean, professional interface
- Color-coded status indicators
- Responsive grid layouts
- Hover effects and interactive elements

---

## Notes

These screenshots show the dashboard with sample data for demonstration purposes. The actual application connects to the C++ trading platform backend via inter-process communication (IPC) for real-time market data, strategy updates, and trade execution.

---

**Last Updated:** May 1, 2026
