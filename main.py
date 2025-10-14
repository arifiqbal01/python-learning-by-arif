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

