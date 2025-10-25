import json
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean,mode,median

with open("chess_games.json") as f:
    games = json.load(f)

with open("chess_games_alpha_beta_pruning.json") as f:
    alpha_beta_pruning = json.load(f)


moves = [g["moves"] for g in games]
durations = [g["duration"] for g in games]
endings = [g["ending"] for g in games]

moves2 = [g["moves"] for g in alpha_beta_pruning]
durations2 = [g["duration"] for g in alpha_beta_pruning]
endings2 = [g["ending"] for g in alpha_beta_pruning]


meanDuration = mean(durations)
medianDuration = median(durations)
modeDuration = mode(durations)

# https://www.geeksforgeeks.org/python/add-text-inside-the-plot-in-matplotlib/
perctange_of_insufficent_to_checkmate = (endings.count("checkmate")/ endings.count("insufficient_pieces")) * 100
plt.bar(("insufficient_pieces", "Checkmate"), (endings.count("insufficient_pieces"), endings.count("checkmate")))
plt.text(0.5, 540, f"{perctange_of_insufficent_to_checkmate}% \nof moves were checkmates", fontsize=10,bbox=dict(facecolor='red', alpha=0.5))
plt.ylabel("amount of games")
plt.show()



plt.scatter(moves, durations,s=10)
plt.axhline(meanDuration, color="black", linestyle="--", label="mean uration")
plt.axhline(medianDuration, color="green", linestyle="--", label="median duration")
plt.axhline(modeDuration, color="purple", linestyle="--", label="mode duration")

plt.xlabel("moves")
plt.ylabel("duration (seconds)")
plt.title("moves vs duration")
plt.legend()
plt.show()





# CPU heating up???
# if the amount of games increases, the time increases in aswell due to increase of heat in the CPU

# https://www.altcademy.com/blog/how-to-change-marker-size-in-scatter-plot-matplotlib/#:~:text=In%20Matplotlib%2C%20you%20can%20change,parameter%20in%20the%20scatter%20function.&text=In%20this%20example%2C%20each%20point,1%2F72%20of%20an%20inch.
# https://www.statology.org/line-of-best-fit-python/


uniform_size = 10
plt.scatter(range(len(alpha_beta_pruning)), durations2,s=uniform_size)
a, b = np.polyfit(range(len(alpha_beta_pruning)), durations2, 1)


plt.plot(range(len(alpha_beta_pruning)), a*range(len(alpha_beta_pruning))+b,linewidth=3,color='black',label="with alpha-beta tuning")  


plt.xlabel("game number")
plt.ylabel("duration (seconds)")
plt.legend()
plt.show()






# CPU heating up???
# if the amount of games increases, the time increases in aswell due to increase of heat in the CPU

# https://www.altcademy.com/blog/how-to-change-marker-size-in-scatter-plot-matplotlib/#:~:text=In%20Matplotlib%2C%20you%20can%20change,parameter%20in%20the%20scatter%20function.&text=In%20this%20example%2C%20each%20point,1%2F72%20of%20an%20inch.
# https://www.statology.org/line-of-best-fit-python/


uniform_size = 10

a, b = np.polyfit(range(len(games)), durations, 1)

a2,b2 = np.polyfit(range(len(games)), durations2, 1)


plt.plot(range(len(games)), a*range(len(games))+b,linewidth=3,color='red',label="without alpha beta pruning")  

plt.plot(range(len(alpha_beta_pruning)), a2*range(len(alpha_beta_pruning))+b2,linewidth=3,color='blue',label="alpha beta pruning")  

plt.xlabel("game number")
plt.ylabel("duration (seconds)")
plt.legend()
plt.show()









# https://stackoverflow.com/questions/50723319/how-do-i-determine-a-correlation-coefficient-in-python
# if a game has more moves it takes longer to compute
# x = np.random.random(20)
# y = np.random.random(20)
# x_bar = np.mean(x)
# y_bar = np.mean(y)

# top = np.sum((x - x_bar) * (y - y_bar))
# bot = np.sqrt(np.sum(np.power(x - x_bar, 2)) * np.sum(np.power(y - y_bar, 2)))



# if a game has more moves it takes longer to compute
moves = np.array(moves)
durations = np.array(durations)

moves_bar = mean(moves)
durations_bar = mean(durations)

top = np.sum((moves - moves_bar) * (durations - durations_bar))
bot = np.sqrt(np.sum((moves - moves_bar)**2) * np.sum((durations - durations_bar)**2))

correlation = top / bot
print("correlation between moves and duration:", correlation)





# draws are more common then wins
perctange_of_insufficent_to_checkmate = (endings.count("checkmate")/ endings.count("insufficient_pieces"))
print(f"{perctange_of_insufficent_to_checkmate}% of moves were checkmates")

