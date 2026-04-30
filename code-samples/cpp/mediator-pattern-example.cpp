/**
 * Mediator Pattern Example
 * 
 * Demonstrates how components communicate through a mediator
 * instead of directly with each other. This ensures:
 * - Decoupling between components
 * - Thread-safe communication
 * - Easy testing and maintenance
 */

#include <memory>
#include <vector>
#include <functional>

// Forward declarations
class RuntimeContext;
template<typename T, typename E> struct Result;

//=============================================================================
// Component Interface
//=============================================================================

/**
 * Base interface for all components.
 * Components are single-threaded and stateless (or manage their own state).
 * The mediator ensures thread-safe access.
 */
class IComponent {
public:
    virtual ~IComponent() = default;
    
    // Components must be movable but not copyable
    IComponent(const IComponent&) = delete;
    IComponent& operator=(const IComponent&) = delete;
    IComponent(IComponent&&) = default;
    IComponent& operator=(IComponent&&) = default;

protected:
    IComponent() = default;
};

//=============================================================================
// Example Component: Risk Calculator
//=============================================================================

struct RiskMetrics {
    double totalExposure;
    double concentrationRisk;
    double drawdownRisk;
};

struct RiskCalculationError {
    std::string message;
};

class RiskCalculator : public IComponent {
public:
    /**
     * Calculate risk metrics for a portfolio.
     * 
     * @param positions Current positions
     * @param ctx Runtime context for logging
     * @return Result with metrics or error
     */
    Result<RiskMetrics, RiskCalculationError> 
    calculateRisk(
        const std::vector<Position>& positions,
        const RuntimeContext& ctx
    ) {
        // Simplified example - real implementation would be more complex
        
        if (positions.empty()) {
            return Result<RiskMetrics, RiskCalculationError>::fail(
                RiskCalculationError{"No positions to calculate risk for"}
            );
        }
        
        RiskMetrics metrics;
        metrics.totalExposure = 0.0;
        
        for (const auto& pos : positions) {
            metrics.totalExposure += pos.value;
        }
        
        // Calculate concentration risk (simplified)
        metrics.concentrationRisk = calculateConcentration(positions);
        
        // Calculate drawdown risk (simplified)
        metrics.drawdownRisk = calculateDrawdown(positions);
        
        return Result<RiskMetrics, RiskCalculationError>::ok(metrics);
    }

private:
    double calculateConcentration(const std::vector<Position>& positions) {
        // Simplified - real implementation uses Herfindahl index
        return 0.0;
    }
    
    double calculateDrawdown(const std::vector<Position>& positions) {
        // Simplified - real implementation tracks historical max
        return 0.0;
    }
};

//=============================================================================
// Flow Action Interface
//=============================================================================

/**
 * Flow actions route data between components.
 * They contain NO business logic - only routing.
 */
class IFlowAction {
public:
    virtual ~IFlowAction() = default;
    
    /**
     * Execute the action.
     * 
     * @param ctx Runtime context
     * @return Result indicating success or failure
     */
    virtual Result<void, std::string> 
    execute(const RuntimeContext& ctx) = 0;
};

//=============================================================================
// Example Flow Action: Calculate Risk Action
//=============================================================================

class CalculateRiskAction : public IFlowAction {
public:
    /**
     * Constructor takes references to components (non-owning).
     * The mediator owns the components.
     */
    CalculateRiskAction(
        RiskCalculator& riskCalc,
        PortfolioAggregator& portfolio
    ) : riskCalc_(riskCalc), portfolio_(portfolio) {}
    
    Result<void, std::string> execute(const RuntimeContext& ctx) override {
        // Step 1: Get positions from portfolio component
        auto positionsResult = portfolio_.getPositions(ctx);
        if (!positionsResult.ok) {
            return Result<void, std::string>::fail(
                "Failed to get positions: " + positionsResult.error->message
            );
        }
        
        // Step 2: Calculate risk using risk calculator component
        auto riskResult = riskCalc_.calculateRisk(
            positionsResult.value.value(),
            ctx
        );
        if (!riskResult.ok) {
            return Result<void, std::string>::fail(
                "Failed to calculate risk: " + riskResult.error->message
            );
        }
        
        // Step 3: Update portfolio with risk metrics
        auto updateResult = portfolio_.updateRiskMetrics(
            riskResult.value.value(),
            ctx
        );
        if (!updateResult.ok) {
            return Result<void, std::string>::fail(
                "Failed to update risk metrics: " + updateResult.error->message
            );
        }
        
        return Result<void, std::string>::ok();
    }

private:
    RiskCalculator& riskCalc_;      // Non-owning reference
    PortfolioAggregator& portfolio_; // Non-owning reference
};

//=============================================================================
// Mediator Core Interface
//=============================================================================

/**
 * Mediator manages components and executes flows.
 * It ensures thread-safe access to components.
 */
class IMediatorCore {
public:
    virtual ~IMediatorCore() = default;
    
    /**
     * Execute a flow (sequence of actions).
     * 
     * @param actions Actions to execute
     * @param ctx Runtime context
     * @return Result indicating success or failure
     */
    virtual Result<void, std::string> 
    executeFlow(
        const std::vector<std::unique_ptr<IFlowAction>>& actions,
        const RuntimeContext& ctx
    ) = 0;
};

//=============================================================================
// Example Mediator: Simple Sequential Mediator
//=============================================================================

class SimpleMediatorCore : public IMediatorCore {
public:
    Result<void, std::string> executeFlow(
        const std::vector<std::unique_ptr<IFlowAction>>& actions,
        const RuntimeContext& ctx
    ) override {
        // Execute actions sequentially
        for (const auto& action : actions) {
            auto result = action->execute(ctx);
            if (!result.ok) {
                return result; // Propagate error
            }
        }
        
        return Result<void, std::string>::ok();
    }
};

//=============================================================================
// Component Container
//=============================================================================

/**
 * Container holds all components with type-safe access.
 * Uses unique_ptr for clear ownership.
 */
class ComponentContainer {
public:
    /**
     * Add a component to the container.
     * Container takes ownership via unique_ptr.
     */
    template<typename T>
    void addComponent(std::unique_ptr<T> component) {
        components_.push_back(std::move(component));
    }
    
    /**
     * Get a component by type.
     * Returns non-owning reference.
     */
    template<typename T>
    T& getComponent() {
        for (auto& comp : components_) {
            if (auto* typed = dynamic_cast<T*>(comp.get())) {
                return *typed;
            }
        }
        throw std::runtime_error("Component not found");
    }

private:
    std::vector<std::unique_ptr<IComponent>> components_;
};

//=============================================================================
// Usage Example
//=============================================================================

void example() {
    // Create component container
    ComponentContainer components;
    
    // Add components (mediator owns them via unique_ptr)
    components.addComponent(std::make_unique<RiskCalculator>());
    components.addComponent(std::make_unique<PortfolioAggregator>());
    
    // Get non-owning references to components
    auto& riskCalc = components.getComponent<RiskCalculator>();
    auto& portfolio = components.getComponent<PortfolioAggregator>();
    
    // Create flow actions (they borrow components via references)
    std::vector<std::unique_ptr<IFlowAction>> actions;
    actions.push_back(
        std::make_unique<CalculateRiskAction>(riskCalc, portfolio)
    );
    
    // Create mediator
    SimpleMediatorCore mediator;
    
    // Execute flow
    RuntimeContext ctx;
    auto result = mediator.executeFlow(actions, ctx);
    
    if (result.ok) {
        // Success - risk calculated and portfolio updated
    } else {
        // Error - handle it
        std::cerr << "Flow failed: " << result.error.value() << std::endl;
    }
}

//=============================================================================
// Key Takeaways
//=============================================================================

/*
 * 1. Components are decoupled - they don't know about each other
 * 2. Mediator manages all communication and thread safety
 * 3. Actions only route data - no business logic
 * 4. unique_ptr for ownership, references for borrowing
 * 5. Result<T, E> for explicit error handling
 * 6. RuntimeContext for logging and tracing
 * 
 * This pattern makes the system:
 * - Easy to test (components in isolation)
 * - Easy to maintain (clear boundaries)
 * - Thread-safe (mediator manages concurrency)
 * - Flexible (easy to add/remove components)
 */
