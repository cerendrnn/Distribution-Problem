# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""

import numpy as np
import random as rand
import time
import matplotlib.pyplot as plt
from sys import exit

def travelTimeMatrixGenerator(numStudents):
    # constants
    size = numStudents+1  # we need to include professor so we increase row and column sizes by 1
    bottom = 100
    top = 300
    # 6x6 empty matrix
    arr = np.zeros((size, size))
    # fill the skew symmetric matrix with random variables with values 100 to 300
    for i in range(size):
        for j in range(size):
            # keep main diagonal zero, the rest is symmetric
            if i != j and arr[i, j] == 0:
                arr[i, j] = rand.randint(bottom, top)
                arr[j, i] = arr[i, j]
            elif i == j:
                arr[i][j] = np.Inf # set diagonal values to infinity
    return arr

def studyTimeListGenerator(numStudents):
    # constants1
    bottom = 300
    top = 500
    # generate unique study times for students
    arr = rand.sample(range(bottom, top), numStudents)
    print("Homework time matrix is: ", arr)
    return arr

def averageMatrixGeneratorV1(travel_time):
    # Take the overall sum of eacch matrix's [i][j] values and pass these overal sums to global_time_matrix
    for i in range(len(travel_time)):
        for j in range(len(travel_time)):
            global_time_matrix[i][j] += travel_time[i][j]

# take the global_time matrix and divide each value to N2 in order to get average values in the matrix
def averageMatrixGeneratorV2(global_list_time, avgNo):
   for i in range(len(global_list_time)):
        for j in range(len(global_list_time)):
            global_list_time[i][j] = (global_list_time[i][j] / avgNo)

def deliverHomeworks(travel_matrix, homework_time_list):
    # This function computes the minimum value in current row
    # Then the value is added to the total_travel_time  
    # Find the index of the min value in row # = controller  
    # Then set column # = controller & set row # = controller to Infinity, in order not to visit the current student again
    # Then the col number of the min value is set to the row no of the next location
    # Go to next iteration with the updated row number
    # Index 0 indicates the intructor in the average travel time matrix
    global controller # controller points to global 'controller' variable 
    value = 0
    total_time = 0
    for i in range(len(travel_matrix)):
        # the code line below gets the min element of row number == controller 
        # and passes it to 'value' variable
        value = np.min(travel_matrix[controller]) # find th min number in the row
        if value != np.Inf:
            total_time += value # update the total_value 
        target = (np.where(travel_matrix[controller] == value))[0].tolist() # find the index of the value in the row
        x = controller  # target holds the related x and y coordinates[x,y]
        y =  target[0]  # x and y coordinates in target list is passes through x & y variables
        travel_matrix[:,controller] = np.Inf # set the column = controller to infinity
        travel_matrix[controller,:] = np.Inf # set the row = controller to infinity
        # travel time path for students are printed on console
        print("Visited [x,y]: [", x," , ", y,"] , ", "Value: ", value)
        # set the location and its symmetry to infinity to indicate that the student is visited 
        #travel_matrix[x][y] = np.Inf 
        #travel_matrix[y][x] = np.Inf
        controller = y # set controller to y_coordinate value for deciding next student number to travel
        visited_students_list.append(controller)
    print("\nUpdated matrix: \n\n", travel_matrix ,"\n")
    print("Visited students:" , visited_students_list,"\n","Array Size: ", len(visited_students_list),"\n")
    for i in range(len(homework_times)):
        total_time += homework_times[i] ## add the homework time values of students to the total_time
    return total_time
    
# Global Variables
N = 5 #student amount
N2 = (int) (round(N * np.log(N)))
travel_time_matrix = []  # holds the travel times matrix
controller = 0
iteration = 0
total_time_result = 0 # final optimal value
optimal_array = [] # hold results in array for graph
runtime_array= [] # hold result in array for graph
N_array = [] # hold N values for graph
f = open("output.txt","w+") 
# create & print sample matrices   
# generate the average matrix from the samples
while(N <= 75):
    start = time.clock() #start timer
    N_array.append(N) # graph
    global_time_matrix = np.zeros((N+1,N+1))
    visited_students_list = [0]
    print("\nIteration: ", iteration+1, "\tN == ", N,"\n")
    
    for i in range(N2):
        travel_time_matrix = travelTimeMatrixGenerator(N)
        #print("Matrix", i+1,":\n", travel_time_matrix,"\n") # see the matrixes printed for each N
        averageMatrixGeneratorV1(travel_time_matrix)
                
    averageMatrixGeneratorV2(global_time_matrix,N2) # computes the average matrix 
    homework_times = studyTimeListGenerator(N) # generate random homework times for each student
    # print values on console
    print("\nAverage time travel matrix is: ", "\n\n", global_time_matrix,"\n")
    total_time_result = deliverHomeworks(global_time_matrix,homework_times)
    print("Optimal value is: ", total_time_result, "minutes") 
    stop = time.clock() # stop timer after computation finishes
    timer = stop-start
    print('Runtime is: ',timer, "seconds")  
    # write the optimal values to  output.txt
    f.write("For N = " + str(N) +"\tOptimal Value is: " + str(total_time_result) + "\tRuntime: " + str(stop - start) + " seconds\n") 
    optimal_array.append(total_time_result)
    runtime_array.append(timer)
    del global_time_matrix
    del visited_students_list
    N = N + 5
    iteration+= 1
    
# plot graphs    
plt.plot(N_array,optimal_array, color='lightblue', linewidth=3) 
plt.xlabel("No of Students (N)")
plt.ylabel("Optimal Values (minutes)")
plt.show()
plt.plot(N_array,runtime_array,color='lightblue', linewidth=3) 
plt.xlabel("No of Students (N)")
plt.ylabel("Runtime Values (seconds)")
plt.show()

f.close() #close file when program finishes executing values
exit(0)