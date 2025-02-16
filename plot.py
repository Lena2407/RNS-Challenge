import numpy as np
import matplotlib.pyplot as plt

# Beispiel-Daten
labels = ['No Provider', 'No Tier-1 ISP', 'No Tier-2 ISP', 'All together']
n_groups = len(labels)

# Drei Werte 
values = np.array([50, 55, 60])  

# Farben für jede Säule (Basisfarben für vorderste Werte)
base_color = 'green'
fig, ax = plt.subplots(figsize=(12, 6))
fig.subplots_adjust(bottom=0.2)
bar_width = 0.6
opacity = 0.6


ax.bar(0, values[2], color=base_color, alpha=0.2, width=bar_width) # links klein
ax.bar(1, values[1], color=base_color, alpha=0.5, width=bar_width) # mitte mitte
ax.bar(2, values[0], color=base_color, alpha=1.0, width=bar_width) # rechts groß
ax.bar(3, values[2], color=base_color, alpha=0.2, width=bar_width) # alle 3 übereinander
ax.bar(3, values[1], color=base_color, alpha=0.5, width=bar_width)
ax.bar(3, values[0], color=base_color, alpha=1.0, width=bar_width)


# Achsenbeschriftungen
#ax.set_xlabel("Network reachablility")
ax.set_ylabel("Number of ASes reachable")
ax.set_title("Network Reachability Example")
ax.set_xticks(np.arange(n_groups))
ax.set_xticklabels(labels, rotation=90)

plt.show()


# cloud = [8075, 15169, 16509, 36351]
# tier1 = [174, 209, 286, 701, 1239, 1299, 2828, 2914, 3257, 3320, 3356, 3491, 5511, 6453, 6461, 6762, 6830, 7018, 12956]
# tier2 = [6939, 7713, 3491, 4826, 9002, 1221, 7922, 4134, 4766, 1257, 3292, 22652, 8001, 1273, 2497, 6830, 2856, 1257, 2516, 7713, 2711, 12182, 4589, 38930]

# as_to_name = {8075:"Microsoft", 15169:"Google", 16509:"Amazon", 36351:"IBM", 
#               174:"Cogent", 209:"Centurylink", 286:"KPN", 701:"VZ Business", 1239:"Sprint", 1299:"Telia", 2828:"VZ", 2914:"NTT", 
#               3257:"GTT", 3320:"D Telekom", 3356:"Level 3", 3491:"PCCW", 5511:"Orange", 6453:"Tata", 6461:"Zayo", 6762:"IT SParkle", 
#               6830:"Liberty Global", 7018:"AT&T", 12956:"Telefonica", 6939:"HE", 7713:"TELIN PT", 3491:"PCCW", 4826:"Vocus", 
#               9002:"RETN", 1221:"Telstra", 7922:"Comcast", 4134:"CN Net", 
#               4766:"Korea Tele", 1257:"KCOM", 3292:"TDC", 22652:"Fibrenoire", 8001:"Stealth", 1273:"Vodafone", 
#               2497:"IIJapan", 6830:"Lib. Glob.", 2856:"Brit. Tele", 1257:"Tele2", 2516:"KDDI", 
#               7713:"PT", 2711:"Spirit", 12182:"Internap", 4589:"Easynet", 38930:"FibreRing"}