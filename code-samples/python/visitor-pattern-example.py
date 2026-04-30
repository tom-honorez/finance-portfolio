"""
Visitor Pattern Example for Quantitative Pricing

Demonstrates how the visitor pattern enables extensible calculations
on a valuation tree without modifying the tree structure.

Key benefits:
- Easy to add new calculations (new visitors)
- Separation of concerns (structure vs calculation)
- Type-safe traversal
- Composable operations
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
import math

#=============================================================================
# Visitor Interface
#=============================================================================

class ValuationVisitor(Protocol):
    """
    Visitor interface for valuation tree traversal.
    Each visit method handles a specific node type.
    """
    
    def visit_spot(self, node: 'SpotNode') -> float:
        """Visit a spot price node"""
        ...
    
    def visit_european_call(self, node: 'EuropeanCallNode') -> float:
        """Visit a European call option node"""
        ...
    
    def visit_delta(self, node: 'DeltaNode') -> float:
        """Visit a delta (Greek) node"""
        ...

#=============================================================================
# Node Base Class
#=============================================================================

class ValuationNode(ABC):
    """
    Base class for all valuation nodes.
    Nodes represent elements in the valuation tree.
    """
    
    @abstractmethod
    def accept(self, visitor: ValuationVisitor) -> float:
        """
        Accept a visitor and delegate to the appropriate visit method.
        This is the key to the visitor pattern.
        """
        pass

#=============================================================================
# Asset Nodes
#=============================================================================

@dataclass
class SpotNode(ValuationNode):
    """
    Represents the current spot price of an asset.
    """
    spot: float
    
    def accept(self, visitor: ValuationVisitor) -> float:
        return visitor.visit_spot(self)

#=============================================================================
# Option Nodes
#=============================================================================

@dataclass
class EuropeanCallNode(ValuationNode):
    """
    Represents a European call option.
    Contains all parameters needed for valuation.
    """
    spot: float
    strike: float
    time_to_maturity: float
    rate: float
    volatility: float
    
    def accept(self, visitor: ValuationVisitor) -> float:
        return visitor.visit_european_call(self)

#=============================================================================
# Greek Nodes
#=============================================================================

@dataclass
class DeltaNode(ValuationNode):
    """
    Represents the delta (spot sensitivity) of an option.
    Wraps an option node.
    """
    option: EuropeanCallNode
    
    def accept(self, visitor: ValuationVisitor) -> float:
        return visitor.visit_delta(self)

#=============================================================================
# Concrete Visitor: Price Calculator
#=============================================================================

class PriceCalculatorVisitor:
    """
    Visitor that calculates prices using Black-Scholes model.
    """
    
    def visit_spot(self, node: SpotNode) -> float:
        """Spot price is just the value"""
        return node.spot
    
    def visit_european_call(self, node: EuropeanCallNode) -> float:
        """Calculate European call price using Black-Scholes"""
        S = node.spot
        K = node.strike
        T = node.time_to_maturity
        r = node.rate
        sigma = node.volatility
        
        # Black-Scholes formula
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        # Standard normal CDF (simplified - real implementation uses scipy)
        N_d1 = self._norm_cdf(d1)
        N_d2 = self._norm_cdf(d2)
        
        price = S * N_d1 - K * math.exp(-r * T) * N_d2
        return price
    
    def visit_delta(self, node: DeltaNode) -> float:
        """Calculate delta (spot sensitivity)"""
        option = node.option
        S = option.spot
        K = option.strike
        T = option.time_to_maturity
        r = option.rate
        sigma = option.volatility
        
        # Delta for European call
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        delta = self._norm_cdf(d1)
        return delta
    
    @staticmethod
    def _norm_cdf(x: float) -> float:
        """
        Approximation of standard normal CDF.
        Real implementation would use scipy.stats.norm.cdf
        """
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

#=============================================================================
# Concrete Visitor: Scenario Analysis
#=============================================================================

class SpotShiftScenarioVisitor:
    """
    Visitor that calculates prices under different spot scenarios.
    Demonstrates how easy it is to add new calculations.
    """
    
    def __init__(self, spot_shifts: list[float]):
        """
        Args:
            spot_shifts: List of relative spot shifts (e.g., [-0.10, 0.0, 0.10])
        """
        self.spot_shifts = spot_shifts
        self.price_calculator = PriceCalculatorVisitor()
    
    def visit_spot(self, node: SpotNode) -> dict[float, float]:
        """Return spot under different scenarios"""
        return {
            shift: node.spot * (1 + shift)
            for shift in self.spot_shifts
        }
    
    def visit_european_call(self, node: EuropeanCallNode) -> dict[float, float]:
        """Calculate option price under different spot scenarios"""
        results = {}
        
        for shift in self.spot_shifts:
            # Create new node with shifted spot
            shifted_node = EuropeanCallNode(
                spot=node.spot * (1 + shift),
                strike=node.strike,
                time_to_maturity=node.time_to_maturity,
                rate=node.rate,
                volatility=node.volatility
            )
            
            # Calculate price with shifted spot
            price = shifted_node.accept(self.price_calculator)
            results[shift] = price
        
        return results
    
    def visit_delta(self, node: DeltaNode) -> dict[float, float]:
        """Calculate delta under different spot scenarios"""
        results = {}
        
        for shift in self.spot_shifts:
            # Create new option node with shifted spot
            shifted_option = EuropeanCallNode(
                spot=node.option.spot * (1 + shift),
                strike=node.option.strike,
                time_to_maturity=node.option.time_to_maturity,
                rate=node.option.rate,
                volatility=node.option.volatility
            )
            
            # Create new delta node
            shifted_delta = DeltaNode(option=shifted_option)
            
            # Calculate delta with shifted spot
            delta = shifted_delta.accept(self.price_calculator)
            results[shift] = delta
        
        return results

#=============================================================================
# Usage Example
#=============================================================================

def example_basic_pricing():
    """Example: Calculate option price and delta"""
    
    # Create option node
    option = EuropeanCallNode(
        spot=100.0,
        strike=100.0,
        time_to_maturity=1.0,
        rate=0.05,
        volatility=0.20
    )
    
    # Create price calculator visitor
    price_visitor = PriceCalculatorVisitor()
    
    # Calculate price
    price = option.accept(price_visitor)
    print(f"Call Price: ${price:.2f}")
    
    # Create delta node
    delta_node = DeltaNode(option=option)
    
    # Calculate delta
    delta = delta_node.accept(price_visitor)
    print(f"Delta: {delta:.4f}")


def example_scenario_analysis():
    """Example: Scenario analysis with spot shifts"""
    
    # Create option node
    option = EuropeanCallNode(
        spot=100.0,
        strike=100.0,
        time_to_maturity=1.0,
        rate=0.05,
        volatility=0.20
    )
    
    # Create scenario visitor with spot shifts
    scenario_visitor = SpotShiftScenarioVisitor(
        spot_shifts=[-0.10, -0.05, 0.00, 0.05, 0.10]
    )
    
    # Calculate prices under different scenarios
    scenario_prices = option.accept(scenario_visitor)
    
    print("\nSpot Scenario Analysis:")
    print("-" * 40)
    for shift, price in scenario_prices.items():
        spot = 100.0 * (1 + shift)
        print(f"Spot: ${spot:6.2f} ({shift:+.1%}) → Price: ${price:.2f}")


def example_adding_new_calculation():
    """
    Example: How easy it is to add a new calculation.
    
    To add a new Greek (e.g., Gamma), you would:
    1. Create a GammaNode class
    2. Add visit_gamma method to visitors
    3. Implement the calculation
    
    No need to modify existing nodes or visitors!
    """
    
    # This is the power of the visitor pattern:
    # - Easy to add new calculations (new visitors)
    # - Easy to add new Greeks (new nodes + visitor methods)
    # - No modification of existing code
    # - Type-safe and composable
    
    pass

#=============================================================================
# Key Takeaways
#=============================================================================

"""
Visitor Pattern Benefits for Quantitative Pricing:

1. **Extensibility**: Easy to add new calculations without modifying nodes
   - New Greek? Add a visitor method
   - New scenario? Create a new visitor
   - New model? Implement visitor interface

2. **Separation of Concerns**: 
   - Nodes represent structure (what is being valued)
   - Visitors represent calculations (how to value it)

3. **Type Safety**:
   - Compiler ensures all node types are handled
   - No runtime type checking needed

4. **Composability**:
   - Visitors can use other visitors
   - Build complex calculations from simple ones

5. **Testability**:
   - Test nodes and visitors independently
   - Easy to mock visitors for testing

Real-world applications:
- Pricing different instruments
- Calculating Greeks (Delta, Gamma, Vega, etc.)
- Scenario analysis (spot, vol, rate shifts)
- Risk calculations
- P&L attribution
- Sensitivity analysis

This pattern is perfect for quantitative finance where:
- You have a fixed structure (instruments, Greeks)
- You need many different calculations
- Calculations change more often than structure
"""

if __name__ == "__main__":
    example_basic_pricing()
    example_scenario_analysis()
