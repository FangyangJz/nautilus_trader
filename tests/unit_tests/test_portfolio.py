#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
# <copyright file="portfolio.pyx" company="Invariance Pte">
#  Copyright (C) 2018-2019 Invariance Pte. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  http://www.invariance.com
# </copyright>
# -------------------------------------------------------------------------------------------------

import unittest
import uuid
import datetime
import time

from datetime import datetime, timezone, timedelta

from inv_trader.common.clock import TestClock
from inv_trader.model.enums import Venue, Resolution, QuoteType, OrderSide, TimeInForce, OrderStatus
from inv_trader.model.enums import MarketPosition
from inv_trader.model.objects import Symbol, Price, Tick, BarType, Bar
from inv_trader.model.order import OrderFactory
from inv_trader.model.events import OrderSubmitted, OrderAccepted, OrderRejected, OrderWorking
from inv_trader.model.events import OrderExpired, OrderModified, OrderCancelled, OrderCancelReject
from inv_trader.model.events import TimeEvent
from inv_trader.model.identifiers import GUID, Label, OrderId, PositionId
from inv_trader.model.position import Position
from inv_trader.data import LiveDataClient
from inv_trader.strategy import TradeStrategy
from inv_trader.tools import IndicatorUpdater
from inv_trader.portfolio.portfolio import Portfolio
from inv_indicators.average.ema import ExponentialMovingAverage
from inv_indicators.intrinsic_network import IntrinsicNetwork
from test_kit.stubs import TestStubs
from test_kit.mocks import MockExecClient
from test_kit.strategies import TestStrategy1

UNIX_EPOCH = TestStubs.unix_epoch()
AUDUSD_FXCM = Symbol('audusd', Venue.FXCM)
GBPUSD_FXCM = Symbol('gbpusd', Venue.FXCM)


class PortfolioTestsTests(unittest.TestCase):

    def setUp(self):
        # Fixture Setup
        self.order_factory = OrderFactory(clock=TestClock())
        self.portfolio = Portfolio()
        print('\n')

    def test_can_register_strategy(self):
        # Arrange
        strategy = TradeStrategy()

        # Act
        self.portfolio._register_strategy(strategy.id)

        # Assert
        self.assertTrue(strategy.id in self.portfolio.registered_strategies())

    def test_can_register_order(self):
        # Arrange
        order = self.order_factory.market(
            AUDUSD_FXCM,
            OrderId('AUDUSD-1-123456'),
            Label('S1'),
            OrderSide.BUY,
            100000)

        position_id = PositionId('AUDUSD-1-123456')

        # Act
        self.portfolio._register_order(order.id, position_id)

        # Assert
        self.assertTrue(order.id in self.portfolio.registered_order_ids())
        self.assertTrue(position_id in self.portfolio.registered_position_ids())