inventory = ["dining table", "desk", "coffee table", "stool", "bench"]
user_input = input('Type of tabe: "dining table", "desk", "coffee table", "stool", "bench" ')
# Save user input

# Check if input exists in the inventory
if user_input in inventory:
    print(user_input, "is in stock!")
else:
    print(user_input, "is not available!")

print("\n")
print("Task 1 completed")
print("**************")
print("\n")

numbers = [1, 2, 3, 4, 5]
while numbers:
    num = int(input("Enter a number from 1 to 10: "))
    for i in range(len(numbers)):
        if numbers[i] == num:
            print(num, "Bingo")
            del numbers[i]
            break
print("You found all numbers!")

print("\n")
print("Task 2 completed")
print("**************")
print("\n")

my_list = [1, 3, 5, 7, 9]
del my_list[:]
print(my_list)

num_list = [1, 3, 5, 7, 9]
print(num_list[2:-1])

sliced_list = num_list[::3]
print(sliced_list)

reversed_list = num_list[::-1]
print(reversed_list)

num_list[2:-1] = [24, 26]


print("\n")
print("Task 3 completed")
print("**************")
print("\n")

my_list = [30, 20, 10, 50, 60, 70, 80, 90]
largest = my_list[-1]
my_list.append(100)
largest = my_list[-1:]


print(largest)


print("\n")
print("Task 4 completed")
print("**************")
print("\n")


wedding_guests = ["Mary", "David", "Harry", "Nick", "Alice"]


# Write your code here
dinner_guests = wedding_guests[:]
del dinner_guests[3]
print(wedding_guests)
print(dinner_guests)

print("\n")
print("Task 5 completed")
print("**************")
print("\n")


stock = ['desk', 'chairs', 'computer']
to_order = ['printer', 'scanner']
# Create assets list
assets = stock[:]
# Append printer and scanner to assets
assets[3:] = to_order[:]

desk_price = 100
chairs_price = 300
computer_price = 1200
printer_price = 250
scanner_price = 120

prices = []
# Append each item's price to prices list
for asset in assets:
    if asset == "desk":
        prices.append(desk_price)
    elif asset == "chairs":
        prices.append(chairs_price)
    elif asset == "computer":
        prices.append(computer_price)
    elif asset == "printer":
        prices.append(printer_price)
    else: 
        prices.append(scanner_price)

total_assets = 0
# Calculate the total amount of prices
for p in prices:
    total_assets += p
# Print the final message with the help of a for loop
print('Total stock:', end=" ")
for i in assets:
    print(i, end=", ")
print('total assets:', str(total_assets) + "$")

print("\n")
print("Task 6 completed")
print("**************")
print("\n")

mixed = [1, 2, 4, 4, 1, 4, 2, 6, 2, 9]
unique_list = []
# Write your code here.
for i in mixed:
    if i not in unique_list:
        unique_list.append(i)
print("The list with unique numbers:")
print(unique_list)

print("\n")
print("Task 7 completed")
print("**************")
print("\n")