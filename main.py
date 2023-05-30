import argparse
from functions import (
    advance_time,
    inventory_check,
    def_buy_product,
    def_sell_product,
    def_revenue,
    def_profit,
    def_chart,
    expired_products,
)

# parser
parser = argparse.ArgumentParser()
# subparser
subparser = parser.add_subparsers(dest="command")

# subparser buy a product
buy_product = subparser.add_parser(
    "buy",
    help="Add product to inventory. Add product details using --product, --price and --expiration",
)
buy_product.add_argument("--product", type=str, metavar="", help="Product Name")
buy_product.add_argument(
    "--price", type=float, metavar="", help="Price with at least one decimal"
)
buy_product.add_argument(
    "--expiration", type=str, metavar="", help="Add a date with notation YYYY-MM-DD"
)

# advance time
parser.add_argument(
    "--advancetime", metavar="", help="Add a number of days to advance the current date"
)

# check the inventory
inventory = subparser.add_parser(
    "inventory",
    help="Check the inventory at a specified date by adding --now, --yesterday or --date (YYYY-MM-DD)",
)
inventory.add_argument("--now", help="Inventory at this moment", action="store_true")
inventory.add_argument("--yesterday", help="Inventory yesterday", action="store_true")
inventory.add_argument(
    "--date", type=str, metavar="", help="Inventory on a date to be chosen (YYYY-MM-DD"
)

# subparser sell a product
sell_product = subparser.add_parser(
    "sell", help="Sell a product from the inventory. Add --product and --price"
)
sell_product.add_argument("--product", type=str, metavar="", help="Product Name")
sell_product.add_argument(
    "--price", type=float, metavar="", help="Price with at least one decimal"
)

# listing expired products
parser.add_argument(
    "--expired",
    help="List all the expired products, when they expired, and how much money was wasted.",
    action="store_true",
)

# reporting the revenue
revenue = subparser.add_parser(
    "revenue",
    help="Report the revenue on a specified date by adding --today, --yesterday or --date (YYYY-MM or YYYY-MM-DD)",
)
revenue.add_argument("--today", help="Today's revenue so far", action="store_true")
revenue.add_argument("--yesterday", help="Yesterday's revenue", action="store_true")
revenue.add_argument(
    "--date", type=str, metavar="", help="Revenue on a date to be chosen"
)

# reporting the revenue
profit = subparser.add_parser(
    "profit",
    help="Report the profit on a specified date by adding --today, --yesterday or --date (YYYY-MM or YYYY-MM-DD)",
)
profit.add_argument("--today", help="Today's profit so far", action="store_true")
profit.add_argument("--yesterday", help="Yesterday's profit", action="store_true")
profit.add_argument("--date", type=str, metavar="", help="Profit on a chosen date")

# revenue/profit chart
parser.add_argument(
    "--chart",
    metavar="",
    help="Display a bar chart containing the revenue en profit per month for a given year",
)

# argparse arguments
args = parser.parse_args()

# functions based on arguments in commandline
if args.advancetime:
    try:
        advance_time(args.advancetime)
    except ValueError:
        print("Please enter a valid number of days, example: 3")
if args.command == "buy":
    def_buy_product(args.product, args.price, args.expiration)
if args.command == "inventory":
    if args.now:
        inventory_check("now")
    if args.yesterday:
        inventory_check("yesterday")
    if args.date:
        inventory_check(args.date)
if args.command == "sell":
    def_sell_product(args.product, args.price)
if args.command == "revenue":
    if args.today:
        def_revenue("today")
    if args.yesterday:
        def_revenue("yesterday")
    if args.date:
        def_revenue(args.date)
if args.command == "profit":
    if args.today:
        def_profit("today")
    if args.yesterday:
        def_profit("yesterday")
    if args.date:
        def_profit(args.date)
if args.chart:
    try:
        def_chart(args.chart)
    except TypeError:
        print("Please enter a valid year, example: 2022")
if args.expired:
    expired_products()
