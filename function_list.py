def average(list1):
  total = 0
  for i in list1:
      total += i
  return total / len(list1)

av = average([5, 2, 2, 4])
print(av)

def my_function(numbers):
    for i in numbers:
        print(i+1, end=' ')

numbers = [1, 2, 3] 
my_function(numbers)

def double_list(numbers):
    return 2 * numbers

numbers = [1, 2, 3]
print(double_list(numbers))


# Open the file prime_numbers.py, and write a function that checks whether an integer is prime* or not. Use a list for the function's argument, and create that list with a for loop for numbers 1 to 20.


# Fun Fact: Prime numbers are used in generating secret keys, e.g in Diffie-Hellman encryption.


# * A number is prime if it is greater than 1 and is divided exactly only by 1 and itself. E.g 4 isn't a prime number, as we can divide it by 1 and 2; 7, however, is a prime number, since we can't divide it exactly with other numbers than 1 and itself.
print("********")

def prime_numbers(num_list):
    prime_numbers = []
    # Write your code here.
    for i in num_list:
        if i > 1:
            is_prime = True
            for j in range(2, int(i ** 0.5 + 1)):
                    if i % j == 0:
                        is_prime = False
                        break
            if is_prime:
                prime_numbers.append(i)
   
    return prime_numbers

numbers = []
# Update the list for numbers 2 to 20
for n in range(2, 21):
      numbers.append(n)

print("Prime numbers list", prime_numbers(numbers))

def prime_numbers(num_list):
      prime_numbers = []
      for num in num_list:
            if num <= 1:
                  return num, "is not greater than 1"
            else:
                  for i in range(2, num):
                        if num % i != 0:
                              prime_numbers.append(num)
                        break
      return prime_numbers

numbers = []
# Update the list for numbers 2 to 20
for i in range(2, 21):
      numbers.append(i)

print("Prime numbers list", prime_numbers(numbers))


def date2list(date):
    d = ""
    for char in date:
        if char != "-":
            d += char
    return [d[0:4], d[4:6], d[6:8]]

# date = input("Enter a date in the format of YYYY-MM-DD: ")
# my_list = date2list(date)
# print(my_list)



month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

for i in range(1, len(month_days)):
    cm_index = i
    pm_index = i -1
    month_days[cm_index] += month_days[pm_index]
print(month_days)