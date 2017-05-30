import plant_propagation as ppa
import Elevator_hill as eh
import Elevator as el
import matplotlib.pyplot as plt
from random import randint

# input examples
# netlist_list = [2,4,3], average_.. = 5, methods = ["ppa","helev","decrmut"]
def create_graph(netlist_list, average_over_X_repeats, methods, standardOn=True):
    salt = str(randint(0,200))
    for net in netlist_list:
        filename = "netlist_" + str(net) +"_" + str(methods) + "repeats_is_" + str(average_over_X_repeats) + "salt_is" + salt + ".png"
        textfilename = "netlist_" + str(net) +"_" + str(methods) + "repeats_is_" + str(average_over_X_repeats) + "salt_is" + str(randint(0, 200)) + ".txt"
        textfile = open(textfilename, 'w')
        fig, ax = plt.subplots()
        if "ppa" in methods:
            ppa_results = [None]*average_over_X_repeats
        if "helev" in methods:
            helev_results = [None]*average_over_X_repeats
        if "decrmut" in methods:
            decrmut_results = [None]*average_over_X_repeats
        for method in methods:
            if method == "ppa":
                #line length plot
                for k in range(average_over_X_repeats):
                    print("repeat number", k, "of netlist", net)
                    ppa_results[k] = ppa.PPA_data(net)
                ppa_iteration_sizes = [0]*average_over_X_repeats
                for k in range(average_over_X_repeats):
                    ppa_iteration_sizes[k] = len(ppa_results[k][0])-1
                ppa_average_lengths = [0]*max(ppa_iteration_sizes)
                for k in range(average_over_X_repeats):
                    for i in range(len(ppa_results[k][0])-1):
                        ppa_average_lengths[i] += ppa_results[k][0][i]
                ppa_iteration_sizes.sort()
                for k in range(len(ppa_average_lengths)):
                    print("ok")
                    if k == ppa_iteration_sizes[0]:
                        del ppa_iteration_sizes[0]
                        print(ppa_iteration_sizes)
                    ppa_average_lengths[k] = ppa_average_lengths[k]/len(ppa_iteration_sizes)
                ax.plot(ppa_average_lengths, 'g')

                # generation point plot
                ppa_generation_amount = [0]*average_over_X_repeats
                for k in range(average_over_X_repeats):
                    ppa_generation_amount[k] = len(ppa_results[k][1])
                ppa_average_generation_points = [0]*max(ppa_generation_amount)
                for k in range(average_over_X_repeats):
                    for i in range(len(ppa_results[k][1])-1):
                        ppa_average_generation_points[i] += ppa_results[k][1][i]
                for i in range(len(ppa_average_generation_points)-1):
                    ppa_average_generation_points[i] = ppa_average_generation_points[i]/average_over_X_repeats
                for xc in ppa_average_generation_points:
                    ax.axvline(x=xc, color='g')

                #earliest/average first constraint satisfaction
                first_constraint_satisfaction_list = []
                for k in range(average_over_X_repeats):
                    first_constraint_satisfaction_list.append(ppa_results[k][2])
                # for earliest use min(...), for average use sum(...)/average_over..
                # ax.axhline(sum(first_constraint_satisfaction_list)/average_over_X_repeats, color='y')

                #data
                best_heights = []
                for k in range(average_over_X_repeats):
                    best_heights.append(ppa_results[k][4])
                best_lengths = []
                for k in range(average_over_X_repeats):
                    best_lengths.append(ppa_results[k][5])
                best_orders = []
                for k in range(average_over_X_repeats):
                    best_orders.append(ppa_results[k][3])
                combined_height_order = []
                for k in range(average_over_X_repeats):
                    combined_height_order.append([best_heights[k], best_orders[k]])
                #sort
                best_lengths, combined_height_order = (list(x) for x in zip(
                    *sorted(zip(best_lengths, combined_height_order),
                            key=lambda pair: pair[0])))
                ppa_first_csa = min(first_constraint_satisfaction_list)
                best_height = combined_height_order[0][0]
                best_order = combined_height_order[0][1]
                best_length = best_lengths[0]
                ppa_text = "for netlist " + str(net) + ", using the plant propagation algorithm, the constraint was first satisfied at " + str(ppa_first_csa) +"\n" + \
                "the best order is: " + str(best_order) + "\n" + \
                "the best height is: " + str(best_height) + "\n" + \
                "the best length is: " + str(best_length) + "\n"
                textfile.write(ppa_text)

            if method == "helev":
                for k in range(average_over_X_repeats):
                    helev_results[k] = eh.hill_climber_data(net)
                # line length plot
                iteration_amount = len(helev_results[0][0])-1
                helev_average_lengths = [0]*iteration_amount
                for k in range(average_over_X_repeats):
                    for i in range(len(helev_results[k][0]) - 1):
                        helev_average_lengths[i] += helev_results[k][0][i]
                for k in range(len(helev_average_lengths)):
                    helev_average_lengths[k] = helev_average_lengths[k] / average_over_X_repeats
                ax.plot(helev_average_lengths)


                # earliest/average first constraint satisfaction
                first_constraint_satisfaction_list = []
                for k in range(average_over_X_repeats):
                    first_constraint_satisfaction_list.append(
                        helev_results[k][1])
                # for earliest use min(...), for average use sum(...)/average_over..
                #ax.axhline(sum(
                #    first_constraint_satisfaction_list) / average_over_X_repeats,
                #            color='g')

                # data possibilities
                best_heights = []
                for k in range(average_over_X_repeats):
                    best_heights.append(helev_results[k][3])
                best_lengths = []
                for k in range(average_over_X_repeats):
                    best_lengths.append(helev_results[k][4])
                best_orders = []
                for k in range(average_over_X_repeats):
                    best_orders.append(helev_results[k][2])
                combined_height_order = []
                for k in range(average_over_X_repeats):
                    combined_height_order.append(
                        [best_heights[k], best_orders[k]])
                # sort
                best_lengths, combined_height_order = (list(x) for x in zip(
                    *sorted(zip(best_lengths, combined_height_order),
                            key=lambda pair: pair[0])))
                helev_first_csa = min(first_constraint_satisfaction_list)
                best_height = combined_height_order[0][0]
                best_order = combined_height_order[0][1]
                best_length = best_lengths[0]
                helev_text = "for netlist " + str(
                    net) + ", using the hillclimber algorithm, the constraint was first satisfied at " + str(
                    helev_first_csa) + "\n" + \
                           "the best order is: " + str(best_order) + "\n" + \
                           "the best height is: " + str(best_height) + "\n" + \
                           "the best length is: " + str(best_length) + "\n"
                textfile.write(helev_text)

            if method == "decrmut":
                for k in range(average_over_X_repeats):
                    decrmut_results[k] = eh.decreasing_mutations(net)
                #line length plot
                decrmut_iteration_sizes = [0]*average_over_X_repeats
                for k in range(average_over_X_repeats):
                    decrmut_iteration_sizes[k] = len(decrmut_results[k][0])-1
                decrmut_average_lengths = [0]*max(decrmut_iteration_sizes)
                for k in range(average_over_X_repeats):
                    for i in range(len(decrmut_results[k][0])-1):
                        decrmut_average_lengths[i] += decrmut_results[k][0][i]
                decrmut_iteration_sizes.sort()
                for k in range(len(decrmut_average_lengths)-0):
                    while k > decrmut_iteration_sizes[0]:
                        del decrmut_iteration_sizes[0]
                    decrmut_average_lengths[k] = decrmut_average_lengths[k]/len(decrmut_iteration_sizes)
                ax.plot(decrmut_average_lengths)

                # generation point plot
                decrmut_generation_amount = [0]*average_over_X_repeats
                for k in range(average_over_X_repeats):
                    decrmut_generation_amount[k] = len(decrmut_results[k][1])
                decrmut_average_generation_points = [0]*max(decrmut_generation_amount)
                for k in range(average_over_X_repeats):
                    for i in range(len(decrmut_results[k][1])-1):
                        decrmut_average_generation_points[i] += decrmut_results[k][1][i]
                for i in range(len(decrmut_average_generation_points)-1):
                    decrmut_average_generation_points[i] = decrmut_average_generation_points[i]/average_over_X_repeats
                for xc in decrmut_average_generation_points:
                    ax.axvline(x=xc, color='c')

                #earliest/average first constraint satisfaction
                first_constraint_satisfaction_list = []
                for k in range(average_over_X_repeats):
                    first_constraint_satisfaction_list.append(decrmut_results[k][2])
                # for earliest use min(...), for average use sum(...)/average_over..
                #ax.axhline(sum(first_constraint_satisfaction_list)/average_over_X_repeats, color='m')

                #data possibilities
                best_heights = []
                for k in range(average_over_X_repeats):
                    best_heights.append(decrmut_results[k][4])
                best_lengths = []
                for k in range(average_over_X_repeats):
                    best_lengths.append(decrmut_results[k][5])
                best_orders = []
                for k in range(average_over_X_repeats):
                    best_orders.append(decrmut_results[k][3])
                combined_height_order = []
                for k in range(average_over_X_repeats):
                    combined_height_order.append([best_heights[k], best_orders[k]])
                #sort
                best_lengths, combined_height_order = (list(x) for x in zip(
                    *sorted(zip(best_lengths, combined_height_order),
                            key=lambda pair: pair[0])))
                decrmut_first_csa = min(first_constraint_satisfaction_list)
                best_height = combined_height_order[0][0]
                best_order = combined_height_order[0][1]
                best_length = best_lengths[0]
                decrmut_text = "for netlist " + str(
                    net) + ", using the decreasing_mutations algorithm, the constraint was first satisfied at " + str(
                    decrmut_first_csa) + "\n" + \
                           "the best order is: " + str(best_order) + "\n" + \
                           "the best height is: " + str(best_height) + "\n" + \
                           "the best length is: " + str(best_length) + "\n"
                textfile.write(decrmut_text)
        if standardOn:
            standard_elevator_solution = el.return_value_elevator(net)
            ax.axhline(standard_elevator_solution[1], color='r')
            standard_solution = standard_elevator_solution[2]
            standard_solution_height = standard_elevator_solution[0]
            repAstarOrder_text = "for netlist " + str(
                net) + ", using the decreasing a* order algorithm" + "\n" + \
                                 "the resulting length is: " + str(
                standard_elevator_solution[1]) + "\n" + \
                                 "the resulting height is: " + str(
                standard_solution_height) + "\n" + \
                                 "the resulting wire order is: " + str(
                standard_solution) + "\n"
            textfile.write(repAstarOrder_text)
        plt.ylabel('length')
        plt.xlabel('iterations')
        fig.savefig(filename)
        plt.clf()



#main(wireList, gatesList, size, Dimensions)

#ppa.PPA_graph([2])

#create_graph(netlist_list, average_over_X_repeats, methods, standardOn=True)
# examples
# netlist_list = [2,4,3], average_.. = 5, methods = ["ppa","helev","decrmut"]
# ppa = plant propagation algortithm
# helev = hillclimber elevator
# decrmut = decreasing mutations
# standardOn=True geeft een horizontale lijn van het resultaat uit jochem's algoritme
# don't forget: meerdere methods geeft een zooi.
create_graph([6], 4, ["ppa"], standardOn=True)
