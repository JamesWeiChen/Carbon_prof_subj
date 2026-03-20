import json
import unittest
from contextlib import nullcontext
from unittest.mock import patch

from utils import trading_utils


class DummySubsession:
    def __init__(self):
        self.start_time = None
        self.executed_trades = '[]'

    def save(self):
        pass


class DummyGroup:
    def __init__(self):
        self.buy_orders = '[]'
        self.sell_orders = '[]'
        self.subsession = DummySubsession()
        self._players = {}

    def add_players(self, *players):
        for player in players:
            player.group = self
            self._players[player.id_in_group] = player

    def get_player_by_id(self, player_id):
        return self._players[player_id]

    def save(self):
        pass


class DummyPlayer:
    def __init__(self, player_id, cash=0, items=0):
        self.id_in_group = player_id
        self.current_cash = cash
        self.current_items = items
        self.group = None
        self.submitted_offers = '[]'
        self.total_bought = 0
        self.total_spent = 0
        self.total_sold = 0
        self.total_earned = 0

    def save(self):
        pass


class TradingUtilsTests(unittest.TestCase):
    def setUp(self):
        lock_ctx_patcher = patch.object(
            trading_utils,
            '_group_order_book_lock',
            side_effect=lambda group: nullcontext(),
        )
        reload_pair_patcher = patch.object(
            trading_utils,
            '_reload_group_and_player',
            side_effect=lambda player, group: (player, group),
        )
        reload_by_id_patcher = patch.object(
            trading_utils,
            '_reload_player_by_id',
            side_effect=lambda _model, group, player_id: group.get_player_by_id(player_id),
        )
        commit_patcher = patch.object(trading_utils, '_commit_trading_state', return_value=None)

        self.addCleanup(lock_ctx_patcher.stop)
        self.addCleanup(reload_pair_patcher.stop)
        self.addCleanup(reload_by_id_patcher.stop)
        self.addCleanup(commit_patcher.stop)

        lock_ctx_patcher.start()
        reload_pair_patcher.start()
        reload_by_id_patcher.start()
        commit_patcher.start()

    def test_process_new_order_sell_consumes_matching_buy_order(self):
        group = DummyGroup()
        buyer = DummyPlayer(1, cash=500, items=0)
        seller_a = DummyPlayer(2, cash=100, items=5)
        seller_b = DummyPlayer(3, cash=100, items=5)
        group.add_players(buyer, seller_a, seller_b)
        group.buy_orders = json.dumps([[1, 54, 2, '00:01']])

        result_a = trading_utils.process_new_order(
            seller_a, group, 'sell', 54, 2, item_name='測試商品', item_field='current_items'
        )

        self.assertEqual(result_a['type'], 'trade_executed')
        self.assertEqual(buyer.current_cash, 392)
        self.assertEqual(seller_a.current_cash, 208)
        self.assertEqual(buyer.current_items, 2)
        self.assertEqual(seller_a.current_items, 3)
        self.assertEqual(json.loads(group.buy_orders), [])
        self.assertEqual(len(json.loads(group.subsession.executed_trades)), 1)

        result_b = trading_utils.process_new_order(
            seller_b, group, 'sell', 54, 2, item_name='測試商品', item_field='current_items'
        )

        self.assertEqual(result_b['type'], 'order_added')
        self.assertEqual(json.loads(group.sell_orders), [[3, 54, 2, '00:00']])
        self.assertEqual(len(json.loads(group.subsession.executed_trades)), 1)

    def test_process_accept_offer_rejects_missing_order(self):
        group = DummyGroup()
        buyer = DummyPlayer(1, cash=500, items=0)
        seller = DummyPlayer(2, cash=100, items=5)
        group.add_players(buyer, seller)

        result = trading_utils.process_accept_offer(
            seller, group, 'buy', 1, 54, 2, item_name='測試商品', item_field='current_items'
        )

        self.assertEqual(result['type'], 'fail')
        self.assertIn('已不存在', result['notifications'][2])
        self.assertEqual(json.loads(group.subsession.executed_trades), [])


if __name__ == '__main__':
    unittest.main()
