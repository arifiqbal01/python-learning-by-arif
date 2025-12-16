def form():
  return input("What's your first name? ")

first_name_a = form()
last_name_a = input("What's your last name? ")
form_a = first_name_a + last_name_a

first_name_b = form()
last_name_b = input("What's your last name? ")
form_b = first_name_b + last_name_b
print(form_a, form_b)

print("\n")
print("Task 1 completed")
print("**************")
print("\n")


# Create the answer_machine function here
def answer_machine():
    print("Please leave your message: ")


answer_machine()
answer1 = input()

answer_machine()
answer2 = input()

answer_machine()
answer3 = input()

print(answer1, answer2, answer3)

print("\n")
print("Task 2 completed")
print("**************")
print("\n")


# Create a function that has two input and one print functions
def print_name():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    print(first_name, last_name)

# Invoke the function
print_name()

print("\n")
print("Task 3 completed")
print("**************")
print("\n")

def address_form(city, postal_code):
  street = input("Enter your street: ")
  print("Your order will be shipped to", city, street, postal_code)

address_form("Taipei", 1234)

print("\n")
print("Task 4 completed")
print("**************")
print("\n")

# Create the data_form function
def data_form(current_year=2020, birth_year=2002, residence="Kerala"):
    full_name = input("What is your full name? ")
    birth_year = input("What is your birth year? ") or birth_year
    residence = input("Where is your city of residence? ") or residence
    age = current_year - int(birth_year)
    return full_name, age, residence
# Invoke the function with the current year value

input(data_form(current_year=2021))

print("\n")
print("Task 5 completed")
print("**************")
print("\n")

def leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                 return False
        else:
            return False
    else:
        return False


current_year = int(input("Enter current year: "))
is_leap = leap_year(current_year)
print(current_year, "is leap?", is_leap)

print("\n")
print("Task 6 completed")
print("**************")
print("\n")


test_years = [2000, 2016, 1979, 1999]
test_output = [True, True, False, False]

# Do the test here
for i in range(len(test_years)):
    year = test_years[i]
    output = leap_year(year)
    if output == test_output[i]:
        print("Test OK")
    else:
        print("Test Failed")

print("\n")
print("Task 7 completed")
print("**************")
print("\n")