from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, TakeProfitRequest, StopLossRequest, TrailingStopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

    import alpaca_trade_api as tradeapi
# ... other imports (databases, models, etc.) ...

# Initialize Alpaca API client
api = tradeapi.REST(YOUR_API_KEY, YOUR_SECRET_KEY, YOUR_PAPER_TRADING_URL)  # Use paper trading first!

while True:  # Main trading loop
    # 1. Data Acquisition
    options_data = api.get_options(symbol="AAPL", expiration_date='2024-01-19') # Example - replace with your logic

    # 2. Option Trading Strategy
    #   - Option pricing model calculations
    #   - Predictive model predictions
    #   - Generate trade signals (buy/sell options)

    # 3. Execute Option Trades (using api.submit_order())  - Only in live trading!

    # Weekly (or defined interval):
    # 4. Stock Portfolio Review
    #   - Data acquisition (fundamental data)
    #   - Screening and selection
    #   - Rebalancing (using api.submit_order()) - Only in live trading!

    time.sleep(60)  # Pause for a minute (adjust as needed)
    
trading_client = TradingClient('api-key', 'secret-key')

# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

# Check our current balance vs. our balance at the last market close
balance_change = float(account.equity) - float(account.last_equity)
print(f'Today\'s portfolio balance change: ${balance_change}')

# search for US equities
search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)

assets = trading_client.get_all_assets(search_params)

# search for AAPL
qqq_asset = trading_client.get_asset('QQQ')

if qqq_asset.tradable:
    print('We can trade QQQ.')

    # preparing market order
market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=0.023,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )

# preparing limit order
limit_order_data = LimitOrderRequest(
                    symbol="BTC/USD",
                    limit_price=17000,
                    notional=4000,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.FOK
                   )

# Limit order
limit_order = trading_client.submit_order(
                order_data=limit_order_data
              )

# preparing short orders
market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )

# preparing orders
market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=0.023,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY,
                    client_order_id='my_first_order',
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )

# Get our order using its Client Order ID.
my_order = trading_client.get_order_by_client_id('my_first_order')
print('Got order #{}'.format(my_order.id))


# preparing bracket order with both stop loss and take profit
bracket__order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=5,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY,
                    order_class=OrderClass.BRACKET,
                    take_profit=TakeProfitRequest(limit_price=400),
                    stop_loss=StopLossRequest(stop_price=300)
                    )

bracket_order = trading_client.submit_order(
                order_data=bracket__order_data
               )

# preparing oto order with stop loss
oto_order_data = LimitOrderRequest(
                    symbol="SPY",
                    qty=5,
                    limit_price=350,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY,
                    order_class=OrderClass.OTO,
                    stop_loss=StopLossRequest(stop_price=300)
                    )

# Market order
oto_order = trading_client.submit_order(
                order_data=oto_order_data
               )

trailing_percent_data = TrailingStopOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC,
                    trail_percent=1.00 # hwm * 0.99
                    )

trailing_percent_order = trading_client.submit_order(
                order_data=trailing_percent_data
               )


trailing_price_data = TrailingStopOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC,
                    trail_price=1.00 # hwm - $1.00
                    )

trailing_price_order = trading_client.submit_order(
                order_data=trailing_price_data
               )

# Get the last 100 closed orders
get_orders_data = GetOrdersRequest(
    status=QueryOrderStatus.CLOSED,
    limit=100,
    nested=True  # show nested multi-leg orders
)

trading_client.get_orders(filter=get_orders_data)

# websocket order updates
@conn.on(client_order_id)
async def on_msg(data):
    # Print the update to the console.
    print("Update for {}. Event: {}.".format(data.event))

stream.subscribe_trade_updates(on_msg)
# Start listening for updates.
stream.run()

# Get our position in AAPL.
aapl_position = trading_client.get_open_position('AAPL')

# Get a list of all of our positions.
portfolio = trading_client.get_all_positions()

# Print the quantity of shares for each position.
for position in portfolio:
    print("{} shares of {}".format(position.qty, position.symbol))
