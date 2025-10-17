from enum import Enum
# variables
name = "Beau" # whole line is called statement
age = 25
Fruits = ["banana", "pine", "apple"]
print(type(age))

# data type 
age = 30 
print(isinstance(age, int))

age = str(2.5) 
print(isinstance(age, str))

name = True # Bolean 
age = False # Bolean 

# operators 
additon = 1 + 1
substraction = 2 - 1
multiplication = 3 * 5
division = 10 / 2 
remainder = 3 % 4 
exponent = 4 ** 2
floorDivision = 3 // 2 #round down to nearist whole number

age = 6
age **= 2
print(age)
print("sum-" + "up")

# comparative operators 
equal = 3 == 4 #false
notEqual = 5 != 7 #true
greaterThan = 8 > 9 #false
lessThan = 4 <= 5 #true

# boolean operators 
condition1 = True
condition2 = False

not condition1 #false
condition1 and condition2 #false
condition2 or condition1 #true

print(0 or 1) #1
print(False or "hey") #hey
print("hi" or False) #hi
print([] or "hi") #hi
print([] or ["hey"])

print("and prints")
print(0 and 1) #0
print(False and "hey") #False
print("hi" and "hi") #True
print([] and "hi") #[]
print([] and ["hey"]) #[]


# is # identity operator - use to compare two objects, return true if both are same objects
# in # membership operator - use to tell value is contain in list or in other sequence

# Ternary operators - quickly define conditioners 
def is_age(age):
  return True if age == 18 else False
print(is_age(19))

# strings #str
"Dog"
'Cat'
print("dog" + "-" + "cat")
f_name = "arif "
f_name += "Iqbal"
print(f_name)

age = str(12)

# multi-line strings
print(""" i'm 
26

years
 old
 .

""")

print("arif".upper())
print("aRiF".lower())
print("aRIf iQbaL".title())
print("arIf".islower())
print("ARIF".isupper())
# isalpha()
# isalnum()
# isdecimal()
# startswith()
# endswith()
# split()
# join()
# find()

# global functions
name = "Arif Iqbal"
print(name.lower())
print(name)
print(len(name))
print("Ar" in name)

# escaping characters
print("arif\"iqbal")
print("arif'iqbal")
print("arif\niqbal") #new line
print("arif\\iqbal") #escape backslash with another backslash

my_name = "arif iqbal"
print(my_name[1])
print(my_name[1:6])
print(my_name[-1])
print(my_name[:6])
print(my_name[7:])

# Bolean 
 # in number only 0 are false
 # only empty strings are false
 # dictioneries are false only when empty
done = ""
print(type(done) == bool)
if done:
  print("yes")
else:
  print("no")

ingrediants_present = True
meal_cooked = False
check_taste = all([ingrediants_present, meal_cooked])
print(check_taste)

# Number Data Types
  # int, float, complex
num1 = 2+3j
num2 = complex(2,3)
print(num1.real, num2.imag)

 # build in functions that help in numbers
print(abs(-5.5)) # provide absolute number value
print(round(3.45, 1)) # provide rounded number 

# enums = readable names that bound to constant value
class State(Enum):
  Inactive = 0
  Active = 1
print(State.Active.value)
print(State['Active'])
print(list(State))
print(len(State))

# user inputs
# age = input("what is your age ")
# print("your age is " + age)

# control statements
condition5 = False
if condition5 == True:
  print("conditon met")
  print("hurry")
else:
  print(" it was not true")


condition6 = True
name = "jonn"
if condition6:
  print("conditon6 met")
  print("hurry 6")
elif name == "roger":
  print("it has name roger")
elif name == "jon":
  print("it has name jon")
else:
  print("does not match any name")