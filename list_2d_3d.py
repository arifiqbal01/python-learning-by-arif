matrix = [['SQUARE' for i in range(8)] for j in range(8)]

print(matrix)

print("\n")
print("Task 1 completed")
print("**************")
print("\n")


countries = [
   ['Egypt', 'USA', 'India'],
   ['Dubai', 'America', 'Spain'], 
   ['London', 'England', 'France']
]
countries2  = [country for row in countries for country in 
                   row if len(country) < 6]
print(countries2)

print("\n")
print("Task 2 completed")
print("**************")
print("\n")

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
chessboard = [[(i + str(j) ) for j in range(1, 9)] for i in letters]
print(chessboard)

print("\n")
print("Task 3 completed")
print("**************")
print("\n")


matrix = [[[k for k in range(3)] for j in range(3)] for i in range(3)]
print(matrix)

print("\n")
print("Task 4 completed")
print("**************")
print("\n")

navbar_links = ["about", "blog", "contact"]                                 
pages = ["index.html", "entry.html"] 

array_3d = [[navbar_links for page in pages] for n in range(1, 5)]
total_links = 0

# Iterate over the 3D array

for a in array_3d:
   for b in a:
      total_links += len(b)

print("total number of links:", total_links)

print("\n")
print("Task 5 completed")
print("**************")
print("\n")

matrix = [
    [[0, 1, 2], [0, 1, 2], [0, 1, 2]], 
    [[0, 1, 2], [0, 1, 2], [0, 1, 2]], 
    [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
]
matrix2 = []

for submatrix in matrix:
  for val in submatrix:
    matrix2.append(val)

print(matrix2[2])

print("\n")
print("Task 6 completed")
print("**************")
print("\n")