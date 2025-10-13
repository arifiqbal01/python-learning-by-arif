import random

def get_choices():
  player_choice = input("Enter a choice (rock, paper, scissors: ")
  options = ["rock", "paper", "scissors"]
  computer_choice = random.choice(options)
  choices = {"player": player_choice, "computer": computer_choice}
  return choices

def check_win(player, computer):
  print(f"player chosed {player} computer chosed {computer}")
  if player == computer:
    return ("it's a tie!")
  elif player == "rock": 
    if computer == "scissors":
      return ("rock smashes scissors. You win")
    else:
      return ("Paper cover rock. you lose")
  elif player == "paper":
    if computer == "rock":
      return ("paper covers rock. You win")
    else:
      return ("Scissors cut paper. you lose")
  elif player == "scissors":
    if computer == "paper":
      return ("Scissors cut paper. You lose")
    else:
      return ("Rock smashes scissors. You win")
    
choices = get_choices()
result = check_win(choices["player"], choices["computer"])
print(result)