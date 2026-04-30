# 🎯 Key Design Decisions

## Overview

This document explains the major architectural and design decisions made during development, with rationale and trade-offs.

---

## 1. Mediator Pattern for Component Communication

### Decision
Use mediator pattern for all component communication instead of direct component-to-component calls.

### Rationale
- **Decoupling:** Components don't know about each other
- **Thread safety:** Mediator manages all synchronization
- **Testability:** Components can be tested in isolation
- **Flexibility:** Easy to add/remove components
- **Maintainability:** Clear communication paths

### Trade-offs
- **Indirection:** One extra hop for all communication
- **Complexity:** More code than direct calls
- **Learning curve:** Developers need to understand pattern

### Result
✅ Worth it - System is highly maintainable and testable

---

## 2. unique_ptr Only (No shared_ptr)

### Decision
Use `unique_ptr` for all ownership, never `shared_ptr`.

### Rationale
- **Clear ownership:** Always obvious who owns what
- **No cycles:** Impossible to create reference cycles
- **Performance:** No atomic reference counting
- **Simplicity:** Easier to reason about lifetimes
- **Safety:** Compiler enforces single ownership

### Trade-offs
- **Flexibility:** Can't share ownership easily
- **Refactoring:** Sometimes need to restructure code
- **Learning curve:** Developers used to shared_ptr

### Result
✅ Worth it - Code is clearer and safer

---

## 3. Result<T, E> Instead of Exceptions

### Decision
Use `Result<T, E>` type for error handling instead of exceptions.

### Rationale
- **Explicit:** Errors are part of function signature
- **Performance:** No exception unwinding overhead
- **Predictable:** No hidden control flow
- **Composable:** Easy to chain operations
- **Type-safe:** Compiler enforces error handling

### Trade-offs
- **Verbosity:** More code than exceptions
- **Propagation:** Need to manually propagate errors
- **Learning curve:** Different from standard C++

### Result
✅ Worth it - Errors are explicit and handled correctly

---

## 4. Dual Broker Support (Kafka + RabbitMQ)

### Decision
Support both Kafka and RabbitMQ instead of just one.

### Rationale
- **Flexibility:** Different use cases need different brokers
- **Demonstration:** Shows ability to work with multiple systems
- **Real-world:** Production systems often use multiple brokers
- **Learning:** Understand trade-offs between systems

### Trade-offs
- **Complexity:** More code to maintain
- **Testing:** Need to test both paths
- **Deployment:** More infrastructure to manage

### Result
✅ Worth it - Demonstrates flexibility and real-world thinking

---

## 5. Dual Serialization (Protobuf + JSON)

### Decision
Support both Protobuf and JSON serialization.

### Rationale
- **Performance:** Protobuf for hot paths
- **Debugging:** JSON for development
- **Web:** JSON for browser communication
- **Flexibility:** Different needs, different formats

### Trade-offs
- **Complexity:** More code to maintain
- **Testing:** Need to test both paths
- **Consistency:** Need to keep schemas in sync

### Result
✅ Worth it - Best of both worlds

---

## 6. Builder Pattern for Mediator Construction

### Decision
Use builder pattern with director for all mediator construction.

### Rationale
- **Type safety:** Compile-time validation
- **Flexibility:** Easy to add new configurations
- **Consistency:** All mediators built the same way
- **Testability:** Easy to create test mediators
- **Documentation:** Self-documenting code

### Trade-offs
- **Boilerplate:** More code than simple constructors
- **Learning curve:** Developers need to understand pattern

### Result
✅ Worth it - Construction is type-safe and consistent

---

## 7. RuntimeContext for Logging

### Decision
Pass `RuntimeContext` to all component methods for logging.

### Rationale
- **Context:** Always know where log came from
- **Thread-safe:** No global state
- **Testable:** Easy to capture logs in tests
- **Flexible:** Can add more context later
- **Performance:** Reference wrapper, no copying

### Trade-offs
- **Verbosity:** Extra parameter on every method
- **Boilerplate:** Need to pass context everywhere

### Result
✅ Worth it - Logging is contextual and thread-safe

---

## 8. No Mutexes in Components

### Decision
Components are single-threaded, mediator handles all synchronization.

### Rationale
- **Simplicity:** Components don't worry about threading
- **Performance:** No lock contention
- **Correctness:** Mediator ensures thread safety
- **Testability:** Components are deterministic

### Trade-offs
- **Flexibility:** Can't have multi-threaded components
- **Performance:** Mediator might be bottleneck

### Result
✅ Worth it - Components are simple and correct

---

## 9. Actions Only Route Data (No Business Logic)

### Decision
Flow actions only route data to components, no business logic.

### Rationale
- **Separation:** Clear boundary between routing and logic
- **Testability:** Logic is in testable components
- **Reusability:** Components can be used in different flows
- **Maintainability:** Easy to find where logic lives

### Trade-offs
- **Verbosity:** More code than putting logic in actions
- **Indirection:** Extra hop to get to logic

### Result
✅ Worth it - System is well-structured and testable

---

## 10. Visitor Pattern for Pricing Library

### Decision
Use visitor pattern for valuation tree traversal.

### Rationale
- **Extensibility:** Easy to add new calculations
- **Separation:** Calculation logic separate from tree structure
- **Type safety:** Compiler ensures all nodes handled
- **Flexibility:** Different visitors for different purposes

### Trade-offs
- **Complexity:** More code than simple methods
- **Learning curve:** Developers need to understand pattern

### Result
✅ Worth it - Easy to add new Greeks and scenarios

---

## 11. Python for Pricing, C++ for Trading

### Decision
Use Python for pricing library, C++ for trading platform.

### Rationale
- **Right tool:** Python for models, C++ for performance
- **Productivity:** Faster to develop models in Python
- **Ecosystem:** NumPy/SciPy are best for numerical computing
- **Integration:** Can bridge with pybind11 later

### Trade-offs
- **Performance:** Python slower than C++
- **Deployment:** Two languages to manage
- **Integration:** Need bridge code

### Result
✅ Worth it - Productivity gains outweigh costs

---

## 12. IPC via stdin/stdout (Not Network)

### Decision
Use stdin/stdout for C++/JavaScript IPC instead of network sockets.

### Rationale
- **Simplicity:** No network stack needed
- **Performance:** No network overhead
- **Portability:** Works everywhere
- **Debugging:** Easy to inspect
- **Security:** No network exposure

### Trade-offs
- **Flexibility:** Can't communicate across machines
- **Scalability:** Limited to single machine

### Result
✅ Worth it - Perfect for desktop application

---

## 13. TimescaleDB for Time-Series Data

### Decision
Use TimescaleDB extension for PostgreSQL instead of separate time-series database.

### Rationale
- **Integration:** Same database as relational data
- **SQL:** Familiar query language
- **Performance:** Optimized for time-series
- **Compression:** Automatic space savings
- **Simplicity:** One database to manage

### Trade-offs
- **Specialization:** Not as optimized as pure time-series DB
- **Scaling:** Limited compared to distributed systems

### Result
✅ Worth it - Good balance of features and simplicity

---

## 14. Electron for Desktop UI

### Decision
Use Electron instead of native UI frameworks.

### Rationale
- **Cross-platform:** One codebase for all platforms
- **Web tech:** Leverage React ecosystem
- **Productivity:** Faster development than native
- **Modern:** Good developer experience

### Trade-offs
- **Size:** Larger application size
- **Performance:** Slower than native
- **Resources:** More memory usage

### Result
✅ Worth it - Productivity gains outweigh costs

---

## 15. No Technical Debt Policy

### Decision
Never merge code with TODOs, shortcuts, or known issues.

### Rationale
- **Quality:** Production-ready from day one
- **Maintainability:** No cleanup needed later
- **Velocity:** No slowdown from debt
- **Pride:** High-quality codebase

### Trade-offs
- **Speed:** Slower initial development
- **Flexibility:** Can't "just ship it"

### Result
✅ Worth it - Codebase is clean and maintainable

---

## Summary

### Patterns Used
- Mediator (component communication)
- Builder (object construction)
- Visitor (tree traversal)
- RAII (resource management)
- Result<T, E> (error handling)

### Principles Followed
- Single Responsibility
- Dependency Inversion
- Interface Segregation
- Don't Repeat Yourself
- Keep It Simple

### Anti-Patterns Avoided
- God objects
- Spaghetti code
- Premature optimization
- Over-engineering
- Technical debt

### Result
A well-designed system that is:
- ✅ Maintainable
- ✅ Testable
- ✅ Performant
- ✅ Extensible
- ✅ Production-ready
