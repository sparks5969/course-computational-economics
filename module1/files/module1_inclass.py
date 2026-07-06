# Block 1: Simple if-elif-else with practical price comparison
# Shows how to use multiple conditions and string formatting
current_price = 45
competitor_price = 40
our_cost = 35

# We compare our price to both competitor price and our costs
if current_price < competitor_price:
    print(f"Our price (${current_price}) is lower than competitor (${competitor_price})")
    if current_price <= our_cost:
        print("Warning: We are selling at or below cost!")
elif current_price == competitor_price:
    print("We are matching competitor's price")
else:
    difference = current_price - competitor_price
    print(f"Our price is ${difference} higher than competitor")


# Block 2: While loop with a practical inventory example
# Shows how to use while loops with compound conditions
inventory = 100
daily_sales = 15
days = 0
reorder_point = 30

print("\nInventory Tracking:")
while inventory > reorder_point and days < 10:
    inventory -= daily_sales
    days += 1
    print(f"Day {days}: Inventory level is {inventory} units")
    if inventory <= reorder_point:
        print("Time to reorder!")


# Block 3: For loop with list manipulation
# Shows how to work with lists and use range()
prices = [10, 20, 15, 25, 30, 15]
print("\nPrice Analysis:")

total = 0
for price in prices:
    total += price
    print(f"Added ${price}, running total: ${total}")

average = total / len(prices)
print(f"Average price is: ${average}")


# Block 4: Combining loops with conditionals
# Shows how to filter and count items
temperatures = [68, 75, 82, 91, 95, 85, 76, 80]
hot_days = 0
pleasant_days = 0

print("\nWeather Analysis:")
for temp in temperatures:
    if temp >= 85:
        hot_days += 1
        print(f"{temp}°F - Hot day!")
    elif 70 <= temp < 85:
        pleasant_days += 1
        print(f"{temp}°F - Pleasant day")
    else:
        print(f"{temp}°F - Cool day")

print(f"We had {hot_days} hot days and {pleasant_days} pleasant days")


# Block 5: String manipulation with a simple input validation
# Shows how to work with strings and use multiple conditions
product_code = "ABC-123-xyz"

print("\nProduct Code Validation:")
if product_code.count('-') == 2 and len(product_code) >= 8:
    parts = product_code.split('-')
    if parts[0].isalpha() and parts[1].isnumeric():
        print("Valid product code format")
        print(f"Product family: {parts[0]}")
        print(f"Product number: {parts[1]}")
    else:
        print("Invalid format: First part should be letters, second part numbers")