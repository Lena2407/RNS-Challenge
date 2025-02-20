
import matplotlib.pyplot as plt
import matplotlib.lines as Line2D
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd





# ixp = set()

as_to_name = {8075:"Microsoft", 15169:"Google", 16509:"Amazon", 36351:"IBM", 
              174:"Cogent", 209:"Centurylink", 286:"KPN", 701:"VZ Business", 1239:"Sprint", 1299:"Telia", 2828:"VZ", 2914:"NTT", 
              3257:"GTT", 3320:"D Telekom", 3356:"Level 3", 3491:"PCCW", 5511:"Orange", 6453:"Tata", 6461:"Zayo", 6762:"IT SParkle", 
              6830:"Liberty Global", 7018:"AT&T", 12956:"Telefonica", 6939:"HE", 7713:"TELIN PT", 3491:"PCCW", 4826:"Vocus", 
              9002:"RETN", 1221:"Telstra", 7922:"Comcast", 4134:"CN Net", 
              4766:"Korea Tele", 1257:"KCOM", 3292:"TDC", 22652:"Fibrenoire", 8001:"Stealth", 1273:"Vodafone", 
              2497:"IIJapan", 6830:"Lib. Glob.", 2856:"Brit. Tele", 1257:"Tele2", 2516:"KDDI", 
              7713:"PT", 2711:"Spirit", 12182:"Internap", 4589:"Easynet", 38930:"FibreRing"}



# predefined ASNs
cloud = [8075, 15169, 16509, 36351]
# same for 2020 and 2024 (3491 and 6453 are ne)
#tier1 =      [174, 209, 286, 701, 1239, 1299, 2828, 2914, 3257, 3320, 3356, 3491, 5511, 6453, 6461, 6762, 6830, 7018, 12956]
#tier1_2015 = [174, 209, 286, 701, 1239, 1299, 2828, 2914, 3257, 3320, 3356,       5511,       6461, 6762, 6830, 7018, 12956]
tier2 = [6939, 7713, 3491, 4826, 9002, 1221, 7922, 4134, 4766, 1257, 3292, 22652, 8001, 1273, 2497, 6830, 2856, 1257, 2516, 7713, 2711, 12182, 4589, 38930]


# pt 3243(viel zu niedrig), 7713(etwas zu hoch)
# spirit 2711 (zu niedrig)

def read_as_relationship(filename):
    types = {8075:0, 15169:0, 16509:0, 36351:0} # 0 = cloud, 1 = tier-1, 2 = tier-2, 3 = was customer if tier-1, 4 = was provider
    p2c = {}
    p2p = {}
    all_ases = set()  
    with open(filename) as f:
        raw = f.readlines()
        for line in raw:
            words = line.split()
            if (words[0] == "#"): # get all comments at the beginning
                if (len(words) > 2 and words[2] == "clique:"): # get input clique (all Tier-1 ISPs)
                    for i in range(3, len(words)):
                        types[int(words[i])] = 1
                # if (words[1] == "IXP"):
                #     for i in range(3, len(words)):
                #         ixp.add(words[i])
            else:
                connection = line.split("|")
                all_ases.add(connection[0])
                all_ases.add(connection[1])
                if (connection[2] == "0"): # peer connections (p2p) are indicated by connection type number 0
                    for i in range(2):
                        peer_1 = int(connection[i])
                        peer_2 = int(connection[(i+1)%2])
                        # add connection to p2p dict
                        if (peer_1 in p2p): 
                            p2p[peer_1].add(peer_2)
                        else:
                            p2p[peer_1] = {peer_2}
                elif (connection[2] == "-1"): # provider to customer connections (p2c) are indicated by connection number -1
                    provider = int(connection[0])
                    customer= int(connection[1])
                    # add connection to p2c dict
                    if (provider in p2c): 
                        p2c[provider].add(customer)
                    else:
                        p2c[provider] = {customer}
                    # add AS type to types dict
                    # if (not provider in types):
                    #     types[provider] = 4 # AS is provider (4)
                    # else:
                    #     if (types[provider] == 3):
                    #         types[provider] = 2 # set Tier-2 type if now provider and has been customer to Tier-1 ISP (3)
                    #     elif (types[provider] == 1):    
                    #         if (not customer in types): 
                    #             types[customer] = 3 # AS is customer to Tier-1 ISP (3)
                    #         elif (types[customer] == 4):
                    #             types[customer] = 2 # set Tier-2 type if now customer to Tier-1 ISP and has been provider (4)
    # deletable = []
    # for a in types:
    #     if (types[a] >= 3):
    #         deletable.append(a)
    #     elif (types[a] == 2):
    #         flag = False
    #         count_peers = 0
    #         count_customers = len(p2c[a])
    #         if (a in p2p):
    #             for n in p2p[a]:
    #                 if (n in types and types[n] == 2):
    #                     count_peers += 1
            
    #         if (count_peers < 200 or count_customers < 20):
    #             deletable.append(a)
    #         else:
    #             print(a)
    # for a in deletable:
    #     types.pop(a)
    # for a in all_vodafone_ases_tier2:
    #     types[a] = 2

    for a in tier2:
        if (not a in types):
            types[a] = 2

    return types, p2c, p2p, all_ases

def reachability(types, p2c, p2p, bypass=[]):
    # 'moving down' (p2c) and 'moving on same layer' (p2p) reachability amount
    reachable = {}
    for a in types:
        # Tier-2 ISPs
        # if (types[a] == 2):
            visited = set()
            stack = [a]
            if a in p2p:
                for n in p2p[a]:
                    if (not (n in types and types[n] in bypass)):
                        stack.append(n)
            while stack:
                elem = stack.pop()  
                if elem in visited:
                    continue
                if (a not in reachable):
                    reachable[a] = {elem}
                else:
                    reachable[a].add(elem)
                visited.add(elem)
                if (elem in p2c):
                    for n in p2c[elem]:
                        if (not (n in types and types[n] in bypass)):
                            stack.append(n)
    return reachable

def calculate_and_plot(filename, sort_by_type, replot):
    types = {8075:0, 15169:0, 16509:0, 36351:0} # 0 = cloud, 1 = tier-1, 2 = tier-2, 3 = was customer if tier-1, 4 = was provider
    p2c = {}
    p2p = {}
    all_ases = set()                  
    types, p2c, p2p, all_ases = read_as_relationship(filename)
    provider_free = reachability(types, p2c, p2p)
    tier_1_free = reachability(types, p2c, p2p, [1])
    hierarchy_free = reachability(types, p2c, p2p, [1,2])
    print(filename, len(all_ases))

    # pandas
    # idx = []
    # provider_free_list = []
    # tier_1_free_list = []
    # hierarchy_free_list = []
    # as_type_list =[]


    plotable_ases = []
    for a in types:
        ases_reachable = [a]
        ases_reachable.append(len(provider_free[a]))
        ases_reachable.append(len(tier_1_free[a]))
        ases_reachable.append(len(hierarchy_free[a]))
        plotable_ases.append(ases_reachable)
        # pandas
        # idx.append(as_to_name[a])
        # provider_free_list.append(len(provider_free[a]))
        # tier_1_free_list.append(len(tier_1_free[a]))
        # hierarchy_free_list.append(len(hierarchy_free[a]))
        # as_type_list.append(types[a])
    plotable_ases.sort(key=lambda x: x[3], reverse=True)
    if (sort_by_type):
        type_sorted_ases = []
        for i in range(3):
            for a in plotable_ases:
                if (types[a[0]] == (i+1)%3):
                    type_sorted_ases.append(a)
        plotable_ases = type_sorted_ases


    # pandas
    sorted_data = { 
        "provider-free":[a[1] for a in plotable_ases],
        "tier-1-free":[a[2] for a in plotable_ases],
        "hierarchy-free":[a[3] for a in plotable_ases],
        "reachability":[a[3]/len(all_ases) for a in plotable_ases],
        "as-type":[types[a[0]] for a in plotable_ases]
    }



    df = pd.DataFrame(sorted_data, index=[as_to_name[a[0]] for a in plotable_ases])

    if (replot):
        # df.plot(kind="")

        # Beispiel-Daten
        label_ases = [a[0] for a in plotable_ases]
        # labels = [as_to_name[i] for i in label_ases]
        # n_groups = len(labels)
        # # Drei Werte für jede Säule (hinterster Wert ist der größte)
        # values1 = np.array([a[3] for a in plotable_ases])  # Vorderster Wert
        # values2 = np.array([a[2] for a in plotable_ases])  # Mittlerer Wert
        # values3 = np.array([a[1] for a in plotable_ases])  # Hinterster Wert

        # color_dict = {0:"blue", 1:"red", 2:"green"}

        # Farben für jede Säule (Basisfarben für vorderste Werte)
        # base_colors = [color_dict[types[i]] for i in label_ases]
        colors =   [["#6495ed", "#4169e1", "#0000ff"], # blue
                    ["#f08080", "#cd5c5c", "#ff0000"], # red
                    ["#98fb98", "#32cd32", "#008000"]] # green
        base_colors = [[colors[types[a[0]]][0] for a in plotable_ases],#["#6495ed", "#f08080", "#98fb98"],
                    [colors[types[a[0]]][1] for a in plotable_ases],#["#4169e1", "#cd5c5c", "#32cd32"],
                    [colors[types[a[0]]][2] for a in plotable_ases]]#["#0000ff", "#ff0000", "#008000"]]


        fig, ax = plt.subplots(figsize=(16, 8))
        bar_width = 0.85
        opacity = 1
        fig.subplots_adjust(bottom=0.15)
        # ax.set_ylim([0, max([a[1] for a in plotable_ases])])

        bottom = np.zeros(len(df))  # Initial bottom for stacking
        for i, col in enumerate(df.columns):
            if (col != "as-type" and col != "reachability"):
                ax.bar(df.index, df[col], bottom=bottom, color=base_colors[i], label=col)
                #bottom += df[col].values  # Update bottom for next stack


        # # Hinterste Säule (größter Wert, volle Sichtbarkeit)
        # for i in range(n_groups):
        #     ax.bar(i, values3[i], color=base_colors[i], alpha=0.3, width=bar_width)

        # # Mittlere Säule (mittlerer Wert, halbtransparent)
        # for i in range(n_groups):
        #     ax.bar(i, values2[i], color=base_colors[i], alpha=0.5, width=bar_width)

        # # Vorderste Säule (kleinster Wert, voll sichtbar)
        # for i in range(n_groups):
        #     ax.bar(i, values1[i], color=base_colors[i], alpha=1.0, width=bar_width)

        # Achsenbeschriftungen
        xlabel = "Network{grouping} cloud providers, Tier-1, and Tier-2 ISPs and sorted by descending hierarchy-free reachability"
        title = "Network reachability on CAIDA dataset from december {year}"
        group_str = "s grouped by" if sort_by_type else ""
        year = filename.split("/")[-1][0:4]
        month = "december" if year == "2015" else "september"

        ax.set_xlabel(xlabel.format(grouping=group_str))
        ax.set_ylabel("Number of ASes reachable")
        ax.set_title(title.format(month=month, year=year))

        
        # ax.set_xticks(np.arange(n_groups))
        # ax.set_xticklabels(labels, rotation=90)
        ax.set_xlim(-1.5, len(types) + 6.5)


        legend_elements = [
            Line2D.Line2D([0], [0], color='black', lw=2, label="Cloud"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#0000ff', markersize=10, label="Provider-free"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#4169e1', markersize=10, label="Tier1-free"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#6495ed', markersize=10, label="Hierarchy-free"),

            Line2D.Line2D([0], [0], color='black', lw=2, label="Tier1"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#ff0000', markersize=10, label="Provider-free"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#cd5c5c', markersize=10, label="Tier1-free"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#f08080', markersize=10, label="Hierarchy-free"),

            Line2D.Line2D([0], [0], color='black', lw=2, label="Tier2"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#008000', markersize=10, label="Provider-free"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#32cd32', markersize=10, label="Tier1-free"),
            Line2D.Line2D([0], [0], marker='s', color='w', markerfacecolor='#98fb98', markersize=10, label="Hierarchy-free"),
        ]

        # Add the legend to the plot
        ax.legend(handles=legend_elements, loc="upper right", title="Reachability")

        plt.xticks(rotation=90)

        grouped = "" if sort_by_type else "un"
        png_name = "Diagrams/{year}_{un}grouped".format(year=year, un=grouped)
        plt.savefig(png_name)
        # plt.show()
        print("Created Diagram ", png_name)
    return df




def plot_reachability_perc(dataframe, year, compare=False, comparator=[]):
    df_display = dataframe.iloc[:20][["hierarchy-free", "reachability", "as-type"]]
    df_display["hierarchy-free"] = df_display["hierarchy-free"].astype(int)  # Convert to int
    df_display["reachability"] = (df_display["reachability"] * 100).map("{:.1f}%".format)  # Convert to %

    if (compare):
        df_display["reachability_inc"] = ((dataframe["reachability"] - comparator["reachability"]) * 100).map("{:.1f}%".format)

        # Prepare table data
    row_labels = df_display.index.astype(str)  # Use index as row labels
    col_labels = ["#", "Network", "Ases rechable", "Reachability"]  # Table headers
    if (compare):
        col_labels.append("Reachability inrease")
    if (compare):
        table_data = [[i+1, row_labels[i], df_display.iloc[i, 0], df_display.iloc[i, 1], df_display.iloc[i,3]] for i in range(len(df_display))]
    else:
        table_data = [[i+1, row_labels[i], df_display.iloc[i, 0], df_display.iloc[i, 1]] for i in range(len(df_display))]

    # Define colors based on "as-type"
    row_colors = {0: "#add8e6", 1: "#ff9999", 2: "#90ee90"}  # Blue, Red, Green
    row_color_list = [row_colors[val] for val in df_display["as-type"]]

    # Plot table
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis("tight")
    ax.axis("off")

    # Create table
    table = ax.table(cellText=table_data, 
                    colLabels=col_labels,
                    cellLoc="center",
                    loc="center",
                    cellColours=[[row_color_list[i]] * len(col_labels) for i in range(len(df_display))])

    # Format table
    #ax.set_title(year)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    # if (compare):
    #     width.append(5)
    # table.auto_set_column_width(width)  # Adjust column width
    table.scale(1,1.5)
    for i, col_label in enumerate(col_labels):
        table.auto_set_column_width([i])

    plt.savefig("Diagrams/{year}_reachability.png".format(year=year))
    #plt.show()


replot = True 
calculate_and_plot("Data/20151201.as-rel2.txt", True, replot)
data_2015 = calculate_and_plot("Data/20151201.as-rel2.txt", False, replot)
calculate_and_plot("Data/20200901.as-rel2.txt", True, replot)
data_2020 = calculate_and_plot("Data/20201201.as-rel2.txt", False, replot)
calculate_and_plot("Data/20240901.as-rel2.txt", True, replot)
data_2024 = calculate_and_plot("Data/20241201.as-rel2.txt", False, replot)

plot_reachability_perc(data_2015, "2015")
plot_reachability_perc(data_2020, "2020", True, data_2015)
plot_reachability_perc(data_2024, "2024", True, data_2020)

