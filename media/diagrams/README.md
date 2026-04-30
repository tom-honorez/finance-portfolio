# 📐 Architecture Diagrams

## Overview

This directory contains PlantUML diagrams that visualize the architecture and design patterns used in the trading platform and pricing library.

---

## Available Diagrams

### 1. System Architecture
**File:** `system-architecture.puml`

Shows the complete system architecture including:
- 3 mediators (Strategy, Reporting, Dashboard)
- Message infrastructure (Kafka, RabbitMQ)
- Data layer (PostgreSQL, TimescaleDB)
- Desktop UI (Electron + React)

**Key concepts:**
- Component organization
- Message flows
- Data persistence
- UI integration

### 2. Mediator Pattern
**File:** `mediator-pattern.puml`

Demonstrates the mediator pattern implementation:
- Component ownership (unique_ptr)
- Action creation and execution
- Component borrowing (references)
- Flow execution

**Key concepts:**
- Decoupled components
- Thread-safe communication
- Actions only route data
- Clear ownership model

### 3. Message Flow
**File:** `message-flow.puml`

Shows a complete message flow example (strategy registration):
- Strategy → Kafka (Protobuf)
- Kafka → Reporting
- Reporting → RabbitMQ (JSON)
- RabbitMQ → Dashboard
- Dashboard → UI (IPC)

**Key concepts:**
- End-to-end flow
- Broker selection
- Serialization choices
- IPC communication

### 4. Builder Pattern
**File:** `builder-pattern.puml`

Illustrates the builder pattern hierarchy:
- Base builder class
- 16 concrete builders (4 types × 2 brokers × 2 serializers)
- Director pattern
- Type-safe construction

**Key concepts:**
- Template method pattern
- Compile-time type safety
- Flexible configuration
- Complete matrix implementation

### 5. Pricing Library
**File:** `pricing-library.puml`

Shows the visitor pattern for quantitative pricing:
- Valuation nodes (Asset, Option, Greek)
- Visitors (Price, Scenario, Description)
- Node-visitor interaction
- Extensible calculations

**Key concepts:**
- Visitor pattern
- Separation of concerns
- Extensibility
- Type-safe traversal

---

## Viewing the Diagrams

### Online Viewers

**PlantUML Online:**
1. Go to http://www.plantuml.com/plantuml/uml/
2. Copy the `.puml` file content
3. Paste and view

**VS Code:**
1. Install "PlantUML" extension
2. Open `.puml` file
3. Press `Alt+D` to preview

**IntelliJ/CLion:**
1. Install "PlantUML integration" plugin
2. Right-click `.puml` file
3. Select "Show PlantUML Diagram"

### Generating PNG/SVG

**Using PlantUML CLI:**
```bash
# Install PlantUML
sudo apt-get install plantuml

# Generate PNG
plantuml system-architecture.puml

# Generate SVG
plantuml -tsvg system-architecture.puml
```

**Using Docker:**
```bash
# Generate all diagrams
docker run --rm -v $(pwd):/data plantuml/plantuml *.puml
```

---

## Diagram Style

All diagrams use:
- **Plain theme** - Clean, professional look
- **White background** - Print-friendly
- **Clear labels** - Easy to understand
- **Consistent notation** - UML standard
- **Annotations** - Explain key concepts

---

## Adding New Diagrams

When adding new diagrams:

1. **Use PlantUML** - Consistent with existing diagrams
2. **Follow naming** - `kebab-case.puml`
3. **Add annotations** - Explain key concepts
4. **Update this README** - Document the new diagram
5. **Keep it simple** - Focus on key concepts

---

## Diagram Sources

These diagrams were created to visualize:
- Architecture decisions from [DESIGN-DECISIONS.md](../../docs/DESIGN-DECISIONS.md)
- System architecture from [TRADING-PLATFORM.md](../../docs/TRADING-PLATFORM.md)
- Pricing library from [PRICING-LIBRARY.md](../../docs/PRICING-LIBRARY.md)

---

## License

These diagrams are part of the portfolio showcase and are subject to the same license as the rest of the repository. See [LICENSE](../../LICENSE) for details.

---

**Last Updated:** April 30, 2026
