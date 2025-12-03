"""
...
A animal class to represent
various animals
...
"""
class Animal:
  def walk(self):
    print("walking...")

class Dog(Animal):
  """a class representing dog"""
  def __init__(self, name, age):
    """Initialize a new dog"""
    self.name = name
    self.age = age

  def bark(self):
    """Let the dog bark"""
    print("Woof!")
print(Dog)

class DogNotFoundException(Exception):
  print("Inside")
  pass

try:
  raise DogNotFoundException()
except DogNotFoundException:
  print("dog not found")

filename = '/home/runner/workspace/module.py'
with open(filename, 'r') as file:
  content = file.read()
  print(content)