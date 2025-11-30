import argparse
from math import sqrt
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