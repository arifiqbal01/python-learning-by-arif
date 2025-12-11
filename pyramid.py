# In the file pyramid.py create a program with the following principle:

# Each row contains one block more than the row before. Based on the input number, calculate the overall amount of rows of the pyramid. Follow the comments for detailed instructions..

# Note: If there is no sufficient number of blocks to complete the future row, then the loop breaks.


total_blocks = int(input("Enter the number of blocks: "))

used_blocks = 0
current_row_blocks = 0
rows = 0

# A while loop running for used_blocks up to total_blocks
while used_blocks < total_blocks:
    # Set blocks per row to 0 to start building new row
    blocks_per_row = 0
    # A while loop for building each row
    while current_row_blocks >= blocks_per_row: 
        # Increment the blocks per row by 1
        blocks_per_row += 1
        # Print an asterisk to visualise the code
        print("*", end="")
    # Increment the rows and print a newline to visualise next row
    rows += 1
    print()
    # Set current_row_blocks to the blocks used inside the nested loop
    current_row_blocks = blocks_per_row
    # Increment used_blocks by the amount of blocks in the current row
    used_blocks += current_row_blocks

    future_row = current_row_blocks + 1
    # Break if the future row needs more blocks than the total


print("The rows of the pyramid:", rows)
