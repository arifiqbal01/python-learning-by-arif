## Task 1

# Complete the code so that the input numbers get sorted in descending order.
input_numbers = []

num = int(input("How many numbers do you want to sort: "))

for i in range(num):
    number = input("put your number: ")
    input_numbers += number

input_numbers.sort()
input_numbers.reverse()
print("Sorted:")
print(input_numbers)

print("\n")
print("Task 1 completed")
print("**************")
print("\n")

## Task 2

# Create a list for the prices 18.0, 12.0, 14.0, 9.0 
prices = [18.0, 12.0, 14.0, 9.0]

for p in range(len(prices)):
    prices[p] += prices[p] * 0.20
print("Prices including tax:", prices)

print("\n")
print("Task 2 completed")
print("**************")
print("\n")
## Task 3

fruits = ["apples", "bananas", "oranges"]

for fruit in fruits:
    if fruit == "bananas":
        print("Bananas are yummy!")
    elif fruit == "apples":
        print("Apples are delicious!")
    else:
        print("Oranges are juicy!")

print("\n")
print("Task 3 completed")
print("**************")
print("\n")
## Task 4

fruits = ["apples", "bananas", "oranges"]
print("Original list content:", fruits) 

fruits[1], fruits[2] = "pear", "peaches"
print("New list content:", fruits) 

print("\n")
print("Task 4 completed")
print("**************")
print("\n")
## Task 5

lottery = [1, 2, 3, 4, 5]  
prompt = "Enter a number to replace the middle number of the list: " + str(lottery) + " "
number = int(input(prompt))
lottery[2] = number
del lottery[-1]
print(lottery, len(lottery))

print("\n")
print("Task 5 completed")
print("**************")
print("\n")