
book1 = input("Have you read Alice in Wonderland, yes or no? ") 
book2 = input("Have you read Aladdin and the Magic Lamp, yes or no? ")

# Conditional statements block

if not(book1 or book2) == "yes":
    print("You have not read either of the books!")
elif not(book1 and book2) == "yes":
    print("You have read one of the books.")
else:
    print("You have read both of the books.")