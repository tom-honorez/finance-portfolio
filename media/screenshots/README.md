# 📸 Dashboard Screenshots

## Overview

Screenshots of the trading dashboard desktop application built with React, TypeScript, and Electron.

---

## Screenshots

### Dashboard Overview
**File:** `dashboard-overview.png`

Main dashboard view showing:
- **Portfolio Summary** - Total value, daily P&L, and performance metrics
- **Active Strategies** - List of running trading strategies with status and metrics
- **Recent Trades** - Real-time trade execution history

**Key Features Visible:**
- Portfolio value: $1,250,000.50
- Daily P&L: +$12,500.75 (+1.01%)
- 3 active strategies (Momentum, Mean Reversion, Arbitrage)
- Real-time trade blotter with symbols, quantities, prices, and P&L
- Strategy health monitoring (RUNNING, PAUSED, HEALTHY, WARNING)
- Performance metrics (Sharpe ratio, positions, trades)

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
