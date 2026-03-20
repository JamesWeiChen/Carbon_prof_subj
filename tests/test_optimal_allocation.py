import json
import unittest

from Stage_CarbonTrading import calculate_optimal_allowance_allocation
from configs.config import config
from utils.shared_utils import calculate_player_production_benchmarks


class DummyPlayer:
    def __init__(self, market_price, marginal_cost, emission_per_unit, max_production):
        self.market_price = market_price
        self.marginal_cost_coefficient = marginal_cost
        self.carbon_emission_per_unit = emission_per_unit
        self.max_production = max_production
        self.disturbance_values = json.dumps([0.0] * max_production)


class DummyGrandfatheringPlayer(DummyPlayer):
    def __init__(self, market_price, marginal_cost, emission_per_unit, max_production, is_dominant):
        super().__init__(market_price, marginal_cost, emission_per_unit, max_production)
        self.is_dominant = is_dominant


class OptimalAllowanceAllocationTests(unittest.TestCase):
    def test_cap_matches_tax_benchmark_emissions(self):
        market_price = 35
        carbon_multiplier = 1.0
        players = [
            DummyPlayer(market_price, marginal_cost=3, emission_per_unit=2, max_production=10),
            DummyPlayer(market_price, marginal_cost=5, emission_per_unit=3, max_production=10),
        ]

        social_cost = config.carbon_trading_social_cost_per_unit_carbon
        tax_rate = carbon_multiplier * social_cost

        allocation = calculate_optimal_allowance_allocation(
            players,
            market_price=market_price,
            tax_rate=tax_rate,
            carbon_multiplier=carbon_multiplier,
            allocation_method="equal",
        )

        expected_totals = 0
        for player, firm_details in zip(players, allocation["firm_details"]):
            benchmarks = calculate_player_production_benchmarks(
                player,
                social_cost_per_unit_carbon=social_cost,
                tax_rate=tax_rate,
            )
            self.assertEqual(firm_details["q_subopt"], benchmarks["q_tax"])
            self.assertEqual(firm_details["TE_subopt"], benchmarks["e_tax"])
            self.assertGreaterEqual(firm_details["q_subopt"], 0)
            self.assertLessEqual(firm_details["q_subopt"], player.max_production)
            self.assertGreaterEqual(firm_details["TE_subopt"], 0)
            self.assertLessEqual(
                firm_details["TE_subopt"],
                int(round(player.carbon_emission_per_unit * player.max_production)),
            )
            expected_totals += benchmarks["e_tax"]

        self.assertEqual(allocation["TE_tax_total"], expected_totals)
        self.assertEqual(allocation["cap_total"], allocation["TE_tax_total"])

    def test_grandfathering_uses_configured_40_percent_share_for_dominant_firms(self):
        market_price = 35
        carbon_multiplier = 1.0
        social_cost = config.carbon_trading_social_cost_per_unit_carbon
        tax_rate = carbon_multiplier * social_cost

        self.assertEqual(config.grandfathering_rule.get("dominant_share_of_cap"), 0.4)

        players = [
            DummyGrandfatheringPlayer(market_price, marginal_cost=3, emission_per_unit=2, max_production=10, is_dominant=1),
            DummyGrandfatheringPlayer(market_price, marginal_cost=3, emission_per_unit=2, max_production=10, is_dominant=1),
            DummyGrandfatheringPlayer(market_price, marginal_cost=3, emission_per_unit=2, max_production=10, is_dominant=1),
        ]
        players.extend(
            DummyGrandfatheringPlayer(market_price, marginal_cost=5, emission_per_unit=1, max_production=8, is_dominant=0)
            for _ in range(12)
        )

        allocation = calculate_optimal_allowance_allocation(
            players,
            market_price=market_price,
            tax_rate=tax_rate,
            carbon_multiplier=carbon_multiplier,
            allocation_method="grandfathering",
        )

        dominant_total = sum(
            permits
            for permits, player in zip(allocation["allocations"], players)
            if player.is_dominant
        )
        expected_dominant_total = int(round(allocation["cap_total"] * 0.4))

        self.assertEqual(dominant_total, expected_dominant_total)
        self.assertEqual(sum(allocation["allocations"]), allocation["cap_total"])


if __name__ == "__main__":
    unittest.main()
