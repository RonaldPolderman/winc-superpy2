import csv
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta, date
import os


# This is a class that defines an object for a purchased product.
# The object has attributes such as the ID, name, date of purchase, purchase price, and expiration date.
class BoughtProduct:
    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.bought_date = row[2]
        self.bought_price = row[3]
        self.expiration_date = row[4]


# This is a class that defines an object for a sold product.
# The object has attributes such as the ID, ID of the bought product, date of sale, and sale price.
class SoldProduct:
    def __init__(self, row):
        self.id = row[0]
        self.bought_id = row[1]
        self.sold_date = row[2]
        self.sold_price = row[3]


# This is a class that defines an object for the current date.
# The object has methods for getting the current date, yesterday's date, and advancing the date by a certain number of days.
class Date:
    def __init__(self, date):
        self.date = date

    def today():
        with open("current_date.txt", "r") as date_file:
            return date_file.read().strip()

    def yesterday():
        with open("current_date.txt", "r") as date_file:
            return datetime.strftime(
                (
                    (datetime.strptime(date_file.read().strip(), "%Y-%m-%d"))
                    - timedelta(days=1)
                ),
                "%Y-%m-%d",
            )

    def advance_date(delta_time):
        with open("current_date.txt", "r") as date_file:
            old_date = datetime.strptime(date_file.read().strip(), "%Y-%m-%d")
            new_date = datetime.strftime(
                old_date + timedelta(days=int(delta_time)), "%Y-%m-%d"
            )
        with open("current_date.txt", "w") as date_file:
            date_file.write(new_date)
        print(f"Date advanced with {delta_time} days and is now {new_date}")


# This function adds a new product to the inventory by writing its information to a CSV file called bought.csv.
# The information includes a unique ID, the product name, the date of purchase (obtained from the Date.today() method),
# the purchase price, and the expiration date.


def def_buy_product(product_name, buy_price, expiration_date):
    # Check if current_date.txt is empty
    if os.path.getsize("current_date.txt") == 0:
        # Write the current date to current_date.txt
        with open("current_date.txt", "w") as file:
            file.write(str(date.today()))

    with open("bought.csv", "r") as bought_file:
        csv_reader = csv.reader(bought_file)
        id = len(list(csv_reader)) + 1

    with open("bought.csv", "a", newline="") as bought_file:
        csv_writer = csv.writer(bought_file)
        csv_writer.writerow(
            [id, product_name, date.today(), buy_price, expiration_date]
        )

    print(f"One {product_name} has been added to the inventory.")


# This function advances the date by a specified number of days, and then checks for any products that have expired.
# Any expired products are removed from the bought.csv file and added to the sold.csv file with a sale price of 0.0.
def advance_time(delta_time):
    Date.advance_date(delta_time)

    new_date = datetime.strptime(Date.today(), "%Y-%m-%d")
    with open("bought.csv", "r") as bought_file, open("sold.csv", "r") as sold_file:
        bought_list = list(map(BoughtProduct, list(csv.reader(bought_file))))
        sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
        bought_list_copy = bought_list.copy()
        for bought_item in bought_list:
            for sold_item in sold_list:
                if bought_item.id == sold_item.bought_id:
                    bought_list_copy.remove(bought_item)

        expired_products = []
        for bought_item in bought_list_copy:
            if datetime.strptime(bought_item.expiration_date, "%Y-%m-%d") < new_date:
                expired_products.append(bought_item)

        with open("sold.csv", "a", newline="") as sold_file:
            csv_writer = csv.writer(sold_file)
            for expired_item in expired_products:
                id = (len(sold_list)) + 1
                csv_writer.writerow([id, expired_item.id, Date.today(), 0.0])
        if expired_products != []:
            print(f"In the meantime, {len(expired_products)} product(s) expired.")


# This function creates a table using the rich library, with columns for the product name, count, purchase price, and expiration date.
# The function takes in a list of products and their information, and outputs the table.
def make_table(inventory_list, product_list):
    table = Table(title=inventory_list)

    table.add_column("Product Name", justify="center")
    table.add_column("Count", justify="center")
    table.add_column("Buy Price", justify="center")
    table.add_column("Expiration date", justify="center")

    for row in product_list:
        column_1 = str(row[0])
        column_2 = str(row[1])
        column_3 = str(row[2])
        column_4 = str(row[3])
        table.add_row(column_1, column_2, column_3, column_4)

    console = Console()
    console.print(table)


# This function takes a requested date as input, and then checks the inventory on that date.
# It checks which products were purchased before that date and not yet sold,
# and then creates a dictionary with the product name as key and the total count and value as values.
# The function then calls the make_table() function to output the inventory as a table.
def inventory_check(requested_date):
    curr_date = ""

    def day():
        with open("bought.csv", "r") as bought_file, open("sold.csv", "r") as sold_file:
            bought_list = list(map(BoughtProduct, list(csv.reader(bought_file))))
            sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
            bought_list_copy = bought_list.copy()
            for bought_item in bought_list:
                for sold_item in sold_list:
                    if (bought_item.id == sold_item.bought_id) and (
                        datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                        <= datetime.strptime(curr_date, "%Y-%m-%d")
                    ):
                        bought_list_copy.remove(bought_item)
            bought_list_copy2 = bought_list_copy.copy()
            for bought_item in bought_list_copy:
                if datetime.strptime(
                    bought_item.bought_date, "%Y-%m-%d"
                ) > datetime.strptime(curr_date, "%Y-%m-%d"):
                    bought_list_copy2.remove(bought_item)

            count_dict = {}
            for product in bought_list_copy2:
                if (
                    product.name,
                    product.bought_price,
                    product.expiration_date,
                ) in count_dict:
                    count_dict[
                        (product.name, product.bought_price, product.expiration_date)
                    ] += 1
                else:
                    count_dict[
                        (product.name, product.bought_price, product.expiration_date)
                    ] = 1
            inventory_list = []
            for key in count_dict:
                inventory_list.append([key[0], count_dict[key], key[1], key[2]])

        make_table(f"Inventory on {curr_date}", inventory_list)

    if requested_date == "now":
        curr_date += Date.today()
        day()
    elif requested_date == "yesterday":
        curr_date += Date.yesterday()
        day()
    else:
        try:
            curr_date += datetime.strftime(
                datetime.strptime(requested_date, "%Y-%m-%d"), "%Y-%m-%d"
            )
            day()
        except ValueError:
            print(
                'Please specify a day to show the inventory: "--now", "--yesterday" or "--date YYYY-MM-DD"'
            )


# This function takes in a list of products, the name of a product and the selling price.
# It then updates the sold product in the products list and returns the updated list.
def def_sell_product(product_name, sell_price):
    with open("bought.csv", "r") as bought_file, open("sold.csv", "r") as sold_file:
        bought_list = list(map(BoughtProduct, list(csv.reader(bought_file))))
        sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
        id = (len(sold_list)) + 1
        bought_list_copy = bought_list.copy()
        for bought_item in bought_list:
            for sold_item in sold_list:
                if bought_item.id == sold_item.bought_id:
                    bought_list_copy.remove(bought_item)

    curr_date_str = Date.today()

    product_to_sell = []
    for product in bought_list_copy:
        if product.name == product_name:
            product_to_sell.append(product)
            break

    if product_to_sell == []:
        print(f"Error: {product_name} not in stock!")
    else:
        with open("sold.csv", "a", newline="") as sold_file:
            csv_writer = csv.writer(sold_file)
            csv_writer.writerow([id, product_to_sell[0].id, curr_date_str, sell_price])
        print(f"One {product_name} sold for {sell_price}!")


# This function takes in a list of products and returns a new list of products that have expired.
# It checks the expiry date of each product in the list and adds it to the new list if it has already expired.
def expired_products():
    product_list = []
    with open("sold.csv", "r") as sold_file, open("bought.csv", "r") as bought_file:
        bought_list = list(map(BoughtProduct, list(csv.reader(bought_file))))
        sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
        for sold_item in sold_list:
            if sold_item.sold_price == "0.0":
                product_list.append(sold_item)
    expired_product_list = []
    for expired_product in product_list:
        for bought_item in bought_list:
            if expired_product.bought_id == bought_item.id:
                expired_product_list.append(
                    [bought_item.name, bought_item.bought_price, sold_item.sold_date]
                )

    table = Table(title="Expired Products")

    table.add_column("Product Name", justify="center")
    table.add_column("Money Wasted", justify="center")
    table.add_column("Date Expired", justify="center")

    for row in expired_product_list:
        column_1 = str(row[0])
        column_2 = str(row[1])
        column_3 = str(row[2])
        table.add_row(column_1, column_2, column_3)

    console = Console()
    console.print(table)


# This function takes in a list of sales, where each sale is a dictionary containing the product name, quantity, and price.
# It calculates the total revenue from all the sales in the list and returns the total revenue.
def def_revenue(requested_date):
    curr_date = ""

    def month():
        revenue = 0
        requested_date_obj = datetime.strptime(requested_date, "%Y-%m")
        with open("sold.csv", "r") as sold_file:
            sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
            for sold_item in sold_list:
                if (
                    datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                ).month == requested_date_obj.month and (
                    datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                ).year == requested_date_obj.year:
                    revenue += float(sold_item.sold_price)

        print(f"The revenue in {requested_date_obj.strftime('%B %Y')} was: {revenue}")

    def day():
        revenue = 0
        requested_date_obj = datetime.strptime(curr_date, "%Y-%m-%d")
        with open("sold.csv", "r") as sold_file:
            sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
            for sold_item in sold_list:
                if (
                    datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                ) == requested_date_obj:
                    revenue += float(sold_item.sold_price)

        print(
            f"The revenue on {requested_date_obj.strftime('%Y-%m-%d')} was: {revenue}"
        )

    if requested_date == "today":
        curr_date += Date.today()
        day()
    elif requested_date == "yesterday":
        curr_date += Date.yesterday()
        day()
    else:
        try:
            curr_date += datetime.strftime(
                datetime.strptime(requested_date, "%Y-%m"), "%Y-%m"
            )
            month()
        except ValueError:
            try:
                curr_date += datetime.strftime(
                    datetime.strptime(requested_date, "%Y-%m-%d"), "%Y-%m-%d"
                )
                day()
            except ValueError:
                print(
                    "Enter a month (format: YYYY-MM) or day (format: YYYY-MM-DD) to view the revenue"
                )


# This function takes in a list of sales and a list of products.
# It calculates the total profit from all the sales in the list by subtracting the cost price of each sold product from its selling price, and then summing up the profits.
# The cost price of each product is obtained from the products list.
def def_profit(requested_date):
    curr_date = ""

    def month():
        profit = 0
        requested_date_obj = datetime.strptime(curr_date, "%Y-%m")

        with open("bought.csv", "r") as bought_file, open("sold.csv", "r") as sold_file:
            bought_list = list(map(BoughtProduct, list(csv.reader(bought_file))))
            sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
            sold_date_list = []
            for sold_item in sold_list:
                if (
                    datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                ).month == requested_date_obj.month and (
                    datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                ).year == requested_date_obj.year:
                    sold_date_list.append(sold_item)
            for sold_item in sold_date_list:
                for bought_item in bought_list:
                    if sold_item.bought_id == bought_item.id:
                        profit += float(sold_item.sold_price) - float(
                            bought_item.bought_price
                        )

        print(
            f"The total profit in {requested_date_obj.strftime('%B %Y')} was: {profit}"
        )

    def day():
        profit = 0
        requested_date_obj = datetime.strptime(curr_date, "%Y-%m-%d")

        with open("bought.csv", "r") as bought_file, open("sold.csv", "r") as sold_file:
            bought_list = list(map(BoughtProduct, list(csv.reader(bought_file))))
            sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
            sold_date_list = []
            for sold_item in sold_list:
                if (
                    datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                ) == requested_date_obj:
                    sold_date_list.append(sold_item)
            for sold_item in sold_date_list:
                for bought_item in bought_list:
                    if sold_item.bought_id == bought_item.id:
                        profit += float(sold_item.sold_price) - float(
                            bought_item.bought_price
                        )

            print(
                f"The total profit on {requested_date_obj.strftime('%Y-%m-%d')} was: {profit}"
            )

    if requested_date == "today":
        curr_date += Date.today()
        day()
    elif requested_date == "yesterday":
        curr_date += Date.yesterday()
        day()
    else:
        try:
            curr_date += datetime.strftime(
                datetime.strptime(requested_date, "%Y-%m"), "%Y-%m"
            )
            month()
        except ValueError:
            try:
                curr_date += datetime.strftime(
                    datetime.strptime(requested_date, "%Y-%m-%d"), "%Y-%m-%d"
                )
                day()
            except ValueError:
                print(
                    "Please enter a month (format: YYYY-MM) or day (format: YYYY-MM-DD) to view the profit"
                )


# This function takes in a list of sales, where each sale is a dictionary containing the product name, quantity, and price.
# It creates a bar chart showing the total revenue for each product in the sales list.
# The x-axis of the chart represents the product names, and the y-axis represents the total revenue.
def def_chart(year):
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    revenue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    profit = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    with open("sold.csv", "r") as sold_file, open("bought.csv", "r") as bought_file:
        sold_list = list(map(SoldProduct, list(csv.reader(sold_file))))
        requested_year_obj = datetime.strptime(year, "%Y")
        sold_date_list = []
        for sold_item in sold_list:
            count = 0
            for month1 in months:
                if (
                    datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                ).month == datetime.strptime(month1, "%b").month and (
                    datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                ).year == requested_year_obj.year:
                    sold_date_list.append(sold_item)
                    revenue[count] += float(sold_item.sold_price)
                count += 1
        bought_list = list(map(BoughtProduct, list(csv.reader(bought_file))))
        for sold_item in sold_date_list:
            for bought_item in bought_list:
                if sold_item.bought_id == bought_item.id:
                    count = 0
                    for month1 in months:
                        if (
                            datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                        ).month == datetime.strptime(month1, "%b").month and (
                            datetime.strptime(sold_item.sold_date, "%Y-%m-%d")
                        ).year == requested_year_obj.year:
                            profit[count] += float(sold_item.sold_price) - float(
                                bought_item.bought_price
                            )
                        count += 1

    xpos = np.arange(len(months))

    plt.xticks(xpos, months)
    plt.xlabel("Profit/Revenue(Month)")
    plt.title(f"Profit and revenue in {year}")
    plt.bar(xpos - 0.2, revenue, width=0.4, label="Revenue")
    plt.bar(xpos + 0.2, profit, width=0.4, label="Profit")
    plt.legend()
    plt.show()
