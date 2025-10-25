import json
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean,mode,median

with open("chess_games.json") as f:
    games = json.load(f)

with open("alpha-beta-tuning-depth4.json") as f:
    prune_4 = json.load(f)

with open("alpha-beta-tuning-depth5.json") as f:
    prune_5 = json.load(f)

with open("alpha-beta-tuning-depth6.json") as f:
    prune_6 = json.load(f)


no_pruning_moves = [g["moves"] for g in games]
no_pruning_duration = [g["duration"] for g in games]
no_pruning_endings = [g["ending"] for g in games]


pruning_4_moves = [g["moves"] for g in prune_4]
pruning_4_durations = [g["duration"] for g in prune_4]
pruning_4_endings = [g["ending"] for g in prune_4]
pruning_4_temps = [g["core_temp"] for g in prune_4]

pruning_5_moves = [g["moves"] for g in prune_5]
pruning_5_durations = [g["duration"] for g in prune_5]
pruning_5_endings = [g["ending"] for g in prune_5]
pruning_5_temps = [g["core_temp"] for g in prune_5]

pruning_6_moves = [g["moves"] for g in prune_6]
pruning_6_durations = [g["duration"] for g in prune_6]
pruning_6_endings = [g["ending"] for g in prune_6]
pruning_6_temps = [g["core_temp"] for g in prune_6]



meanDuration = mean(no_pruning_duration)
medianDuration = median(no_pruning_duration)
modeDuration = mode(no_pruning_duration)



# https://www.geeksforgeeks.org/python/add-text-inside-the-plot-in-matplotlib/

# plt.figure(figsize=(10, 6))


# plt.bar("no pruning (4 ply)", no_pruning_endings.count("insufficient_pieces"),color="cyan")
# plt.bar("no pruning (4 ply)", no_pruning_endings.count("checkmate"), color="blue")
# plt.text(-0.4, no_pruning_endings.count("insufficient_pieces") + 100, f"{(no_pruning_endings.count("checkmate") / no_pruning_endings.count("insufficient_pieces")) * 100:.1f}%\nof moves were checkmates\nwith no pruning (4 ply)", fontsize=9, bbox=dict(facecolor='teal'))



# plt.bar("pruning (4 ply)", pruning_4_endings.count("insufficient_pieces"),color="cyan")
# plt.bar("pruning (4 ply)", pruning_4_endings.count("checkmate"), color="blue")
# plt.text(0.6, no_pruning_endings.count("insufficient_pieces") + 100, f"{(pruning_4_endings.count("checkmate") / pruning_4_endings.count("insufficient_pieces")) * 100:.1f}%\nof moves were checkmates\nwith pruning (4 ply)", fontsize=9, bbox=dict(facecolor='teal'))



# plt.bar("pruning (5 ply)", pruning_5_endings.count("insufficient_pieces"),color="cyan")
# plt.bar("pruning (5 ply)", pruning_5_endings.count("checkmate"), color="blue")
# plt.text(1.6, no_pruning_endings.count("insufficient_pieces") + 100, f"{(pruning_5_endings.count("checkmate") / pruning_5_endings.count("insufficient_pieces")) * 100:.1f}%\nof moves were checkmates\nwith pruning (5 ply)", fontsize=9, bbox=dict(facecolor='teaL'))



# plt.bar("pruning (6 ply)", pruning_6_endings.count("insufficient_pieces"),color="cyan")
# plt.bar("pruning (6 ply)", pruning_6_endings.count("checkmate"), color="blue")
# plt.text(2.6, no_pruning_endings.count("insufficient_pieces") + 100, f"{(pruning_6_endings.count("checkmate") / pruning_6_endings.count("insufficient_pieces")) * 100:.1f}%\nof moves were checkmates\nwith pruning (6 ply)",fontsize=9, bbox=dict(facecolor='TEAL'))

# plt.ylabel("Amount of games")
# plt.tight_layout()
# plt.show()














# uniform_size = 10
# plt.scatter(range(len(prune_4)), pruning_4_durations,s=uniform_size)
# a, b = np.polyfit(range(len(prune_4)), pruning_4_durations, 1)

# plt.plot(range(len(prune_4)), a*range(len(prune_4))+b,linewidth=3,color='black',label="with alpha-beta tuning")  
# plt.xlabel("game number")
# plt.ylabel("duration (seconds)")
# plt.legend()
# plt.show()







# uniform_size = 10

# a, b = np.polyfit(range(len(games)), no_pruning_duration, 1)
# a2,b2 = np.polyfit(range(len(games)), pruning_4_durations, 1)
# a3,b3 = np.polyfit(range(len(games)), pruning_5_durations, 1)
# a4,b4 = np.polyfit(range(len(games)), pruning_6_durations, 1)



# plt.plot(range(len(games)), a*range(len(games))+b,linewidth=3,color='red',label="without alpha beta pruning (4ply)")  
# plt.plot(range(len(prune_4)), a2*range(len(prune_4))+b2,linewidth=3,color='blue',label="alpha beta pruning (4ply)")  
# plt.plot(range(len(prune_5)), a3*range(len(prune_5))+b3,linewidth=3,color='green',label="alpha beta pruning (5ply)")  
# plt.plot(range(len(prune_6)), a4*range(len(prune_6))+b4,linewidth=3,color='cyan',label="alpha beta pruning (6ply)")  

# plt.xlabel("game number")
# plt.ylabel("duration (seconds)")
# plt.legend()
# plt.show()




uniform_size = 10

a2,b2 = np.polyfit(range(len(games)), pruning_4_temps, 1)
a3,b3 = np.polyfit(range(len(games)), pruning_5_temps, 1)
a4,b4 = np.polyfit(range(len(games)), pruning_6_temps, 1)


print(a2,a3,a4)
plt.plot(range(len(prune_4)), a2*range(len(prune_4))+b2,linewidth=3,color='blue',label="alpha beta pruning (4ply)")  
plt.plot(range(len(prune_5)), a3*range(len(prune_5))+b3,linewidth=3,color='green',label="alpha beta pruning (5ply)")  
plt.plot(range(len(prune_6)), a4*range(len(prune_6))+b4,linewidth=3,color='cyan',label="alpha beta pruning (6ply)")  

plt.xlabel("game number")
plt.ylabel("CPU temp (average over all the cores)")
plt.legend()
plt.show()












# no_pruning_moves = np.array(no_pruning_moves)
# no_pruning_duration = np.array(no_pruning_duration)

# moves_bar = mean(no_pruning_moves)
# durations_bar = mean(no_pruning_duration)

# top = np.sum((no_pruning_moves - moves_bar) * (no_pruning_duration - durations_bar))
# bot = np.sqrt(np.sum((no_pruning_moves - moves_bar)**2) * np.sum((no_pruning_duration - durations_bar)**2))

# correlation = top / bot
# print("correlation between moves and duration:", correlation)



# # draws are more common then wins
# perctange_of_insufficent_to_checkmate = (no_pruning_endings.count("checkmate")/ no_pruning_endings.count("insufficient_pieces"))
# print(f"{perctange_of_insufficent_to_checkmate}% of moves were checkmates")

