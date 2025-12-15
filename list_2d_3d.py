matrix = [['SQUARE' for i in range(8)] for j in range(8)]

print(matrix)


countries = [
   ['Egypt', 'USA', 'India'],
   ['Dubai', 'America', 'Spain'], 
   ['London', 'England', 'France']
]
countries2  = [country for row in countries for country in 
                   row if len(country) < 6]
print(countries2)


letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
chessboard = []
# Write your code here
for i in range(1, 9):
  row = []
  for j in letters:
    row.append(j + str(i))
  chessboard.append(row)
  
print(chessboard)