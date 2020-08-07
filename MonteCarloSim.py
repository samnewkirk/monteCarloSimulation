import random

def U():
    u = random.random() 
    return u

def myBernoulli(p):
    u = U()
    if (u<p):
        x = 1
    else:
        x = 0
    return x

def variables():
    n = int(input("Please enter how many computers are in the network: "))
    f = int(input("Please enter how many computers are infected on the first day: "))
    clean = int(input("Please enter how many computers can be cleaned each day: "))
    p = float(input("Please enter the probability of infection: "))
    n = n - f
    network = []
    infected = []
    for i in range (f):
        infected.append(i)
        network.append(1)
    for i in range(n):
        network.append(0)
    
    return network, infected, clean, p

def infection(network, p):              #run trial for every uninfected computer per infected computer
    for i in range(len(network)):
        for j in range(len(network)):
            if network[i] == 1 and network[j]==0:
                x = myBernoulli(p)              
                if x ==1:
                    network[j]=2
    for k in range (len(network)):
        if network[k]==2:
            network[k] = 1
    return network

def count_infected(network):        #list comprehension to keep track of indices of infected computers
    for i in range(len(network)):
        index = [i for i, x in enumerate(network) if x == 1]  
    return index

def technician(network, infected, clean): #technician can clean 5 infected computers a day
    if (len(infected)) <= clean:       #if there are 5 or less infected they will clean all infected
        for i in range(len(network)):
            if network[i]==1:
                network[i]=0
                infected.clear()   #clear the infected list as there are no longer any infected computers
    else:
        choose = random.sample(infected, clean) #this will be a list of randomly choosen indices to be cleaned
        for i in range(len(network)):
            for j in range(len(choose)):
                if i == choose[j]:   #if the index of network is equal to the value in our random list
                    network[i]=0     #we will change the value in the network to 0, meaning uninfected
    return network, infected         #we need to return the infected list cuz if it is cleared we need to know

def simulation(network, infected, clean, p):  
    days = 0              
    saturated_runs = 0
    comps_affected = {0}        #using a set so there are no duplicates
    while(len(infected)!= 0):   #when the infected list is empty we are done with the simulation
        days+=1
        network2 = infection(network, p)            #this returns network after a run of the infection
        infected = count_infected(network2)         #this returns a list with the indices of infected computers
        if (len(infected) == 0):
            break
        elif(len(infected)== 20):   #if length of infected is 20 that means all comps are infected
            saturated_runs+=1
            for i in range (len(infected)):
                comps_affected.add(infected[i])
        else:                   
            for i in range (len(infected)):
                comps_affected.add(infected[i]) 
                
        network, infected = technician(network2, infected, clean) 

    return days, saturated_runs, comps_affected

def MonteCarlo(N):
    #Network, Infected, Clean, x = variables()
    total_days = 0
    total_infection_probability = 0
    total_infected = 0
    count = 0
    while count < N:
        network = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        infected = [0]
        clean = 5
        p = 0.1   
        a,b,c = simulation(network, infected, clean, p) #a=days, b=saturated_runs, c=comps_affected
        count+=1
        total_days+=a
        total_infection_probability+=b
        for i in range(len(c)):
            total_infected+=1
            
    expected_time = total_days/N
    probability = total_infection_probability/N
    expected_number_infected = total_infected/N
    
    return expected_time, probability, expected_number_infected

def main():
    N = int(input("Please enter how many simulations you would like to run: "))
    x,y,z = MonteCarlo(N)
    print("Per simulation, the expected time to remove the virus from the entire network: ")
    print(x)
    print("Per simulation, the probability that each computer gets infected at least once: ")
    print(y)
    print("Per simulation, the expected number of computers to become infected: ")
    print(z)

########################################################################################
if __name__ == "__main__":
    main()




