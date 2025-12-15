import argparse
from math import sqrt
from os import name
from re import error
from typing import Self
from lib import dog
from functools import reduce
import time

dog.bark()

# Libraries
print(sqrt(4))

# accept arguments 
# name = sys.argv[2]
# print("hello " + name)

parser = argparse.ArgumentParser(
  description='this program prints the name of my dogs'
)

parser.add_argument('-c', '--color', metavar='color', choices={'red', "yellow"}, help='the color to search for')

args = parser.parse_args()
print(args.color)

# Lambda Functions
lambda num : num * 2

multiply = lambda a, b: a * b
print(multiply(2, 3))

# map(), filter(), reduce()
numbers = [1, 2, 3]
result = map(lambda a: a * 2, numbers)
print(list(result))

mix_numbers = [1, 2, 4, 5, 3, 7, 8, 4]
even = filter(lambda a: a % 2 == 0, mix_numbers)
print(list(even))

expanses = [
  ('Dinner', 80),
  ('Car repair', 12)
]
sum = reduce(lambda a, b: a[1] + b[1], expanses)
print(sum)

# recursion
def factorial(n):
  if n == 1: return 1
  return n * factorial(n-1)
print(factorial(3))
print(factorial(4))

# decorators
def decor(func):
  def wrapper():
    print("before")
    func()
    print("after")
  return wrapper
@decor
def greet():
   print("hello")
greet()

def timer(func):
  def wrapper():
    start = time.time()
    func()
    end = time.time()
    print("execution time is", end - start)
  return wrapper

@timer
def total_sum():
  time.sleep(1)
  return 12000 + 328475628734 + 34285672
total_sum()


# Docstrings
"""
this module is for for dog function.
"""
# Annotation
def increment(n: int) -> int:
  return n +1

count: int = 0

# exceptions
try: 
  result = 2/0
except ZeroDivisionError:
  print("cannot devide by zero!")
finally:
  result = 1
print(result)

try: 
  raise Exception("An error")
except Exception as error:
  print(error)

# Third Party Packages
# pip

# List Compression
numbers_normal = [1, 2, 3, 4, 5, 6]
numbers_power_2 = [n**2 for n in numbers_normal]
print(numbers_power_2)

numbers_power_2 = []
for n in numbers_normal:
  numbers_power_2.append(n**2)

# Polymorphism 

class Dog0:
  def eat(self):
    return "Dog eating"

class Cat:
  def eat(self):
    return "Cat eating"

roger = Dog0()
meao = Cat()
print(roger.eat())
print(meao.eat())

# Operator overlading
class Dog:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def __gt__(self, other):
    return True if self.age > other.age else False

roger = Dog("Roger", 8)
syd = Dog("Syd", 7)

"""
Different Operators 

__add__() respond to the + operator
__sub__() respond to the - operator
__mul__() respond to the * operator
__truediv__() respond to the / operator
__floordiv__() respond to the // operator
__mod__() respond to the % operator
__pow__() respond to the ** operator
__rshift__() respond to the >> operator
__lshift__() respond to the << operator
__and__() respond to the & operator
__or__() respond to the | operator
__xor__() respond to the ^ operator

"""

num1 = 2+3j
num2 = complex(2,3)
print(num1.real, num2.imag)

age = 22
while age > 20:
  print("Adult", age)
  age -= 1
print("age does not satisfy condition")

boys = ["sohail", "shanu", "sikandar"]
for boy in boys:
  your_boy = boys[1]
print(your_boy)

list = [1, 2, 3, 4, 5]
sums_up = 0
for i in list:
  sums_up += i
print(sums_up)

numbers = [1, 2, 3, 4, 5]
max_up = 0
for i in numbers:
  max_up += i * i
print(max_up)

random_list = [1, 3, 45, 23, 7]
def numberSquare():
  squareList = []
  for a in random_list:
    single_item = a ** 2
    squareList.append(single_item)
  print(squareList)
numberSquare()

fruits = ['mango', ' banana', 'apple']
for f in fruits:
  if f == 'banana':
    continue
  print("fruits: " + f + " banana skiped")

class Animal:
  def walking(self):
    print("walking...")
    return self
    
  def eat(self):
    print("eating...")
    return self

class Dog(Animal):
  def __init__(self, name, age):
    self.name = name
    self.age = age
    
  def bark(self):
    print("Woof, Woff..")
    return self
  
  def sound(self):
    print("Woof, Woff..")

  def introduce(self):
    print(f"My name is {self.name} and my age is {self.age}")
    return self
  
  def human_age(self):
    print(self.age * 7)

class Cat(Animal):
  def __init__(self, name, color):
    self.name = name
    self.color = color
  
  def meow(self):
    print("Meow meow..")
    return self
  
  def sound(self):
    print("Meow meow..")

def make_sound(Animal):
  Animal.sound()

d1 = Dog("Buddy", 8)
c1 = Cat("Mimi", "White")
d1.introduce()
d1.walking()
d1.bark()
c1.walking().meow()
d1.eat()
c1.eat()
d1.human_age()
make_sound(d1)
make_sound(c1)