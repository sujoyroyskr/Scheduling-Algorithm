from operator import itemgetter
def nprint(jobs,string):
    print(5*"\t", string)
    print('Job_id\t' + 'Arrival Time\t' + 'Execution_time\t' + 'Start_time\t' +'Finish_time\t'
     + 'Remaining_time\t' + 'Completed' 
     )
    x =' '
    for i in jobs:
        
        jobid,x0 = i.get('id'), len("Job_id\t")-len(i.get('id'))
        ar,x1 = i.get('Arrival Time'), len('Arrival Time\t')-len(str(i.get('Arrival Time')))
        ex,x2 = i.get('Execution time'), len('Execution_time\t')-len(str(i.get('Execution time')))
        st,x3 = i.get('Strt_Time'), len('Start_time\t\t  ')-len(str(i.get('Strt_Time')))
        ft,x4 = i.get('Fin_Time'), len('Finish_time\t\t')-len(str(i.get('Fin_Time')))
        re,x5 = i.get('Execution left'), len('Remaining_time\t')-len(str(i.get('Execution left')))
        ct,x6 = i.get('Completed'), len('Completed')-len(i.get('Completed'))
        
        print(jobid , x*x0 , ar ,x*x1 , ex , x*x2 , st , x*x3 , ft , x*x4 ,re , x*x5,ct , x*x6)
    
        
    return



#display function to make life easier#display 

def display(time,done_jobs,job_queue,current,order):
    print(5*"\t" , "Current Clock Time: ",time)
            
    nprint(done_jobs,"Jobs Completed")
    print("\n")
            

    nprint(job_queue,"Job Queue")
    print("\n")
    nprint([current],"Current Job")
    print("\n")
    print("Order: ",order)
    print("\n")
            
    print(5*"\t","----------end-of-report--------------\n\n")
    return

d = int(raw_input("Enter processor allotted time d: "))


execTime = raw_input("Enter the initial set of jobs at time = 0(seperate by commas): ")


moreJobs = (raw_input("Any more jobs at later time [1/0]: "))


if moreJobs == '1':
    g =  raw_input("<Arrival_time, Execution_time> seperated by ; :")
else:
    g = None
    

display_time = int(raw_input("Enter the time instant for displaying the job scheduling result: "))


# d = 5
# execTime = '18,4,7,9,6'
# g = '18,20'
# display_time = 10

#creating the jobs based on their execution time as given in input

execTime = execTime.split(',')
execTime = [int(i) for i in execTime]
ArrivalTime = 0
# random.shuffle(execTime) #shuffle the exec times randomly , so jobs get in queue in random order
jobs = []
queue = []
k = 1
for i in execTime:
    dict_ = {}
    string = 'Job' + str(k)
    jobs.append(string)
    dict_ ={'id':string,'Arrival Time': 0,'Strt_Time': 'n/a','Fin_Time': 'n/a', 'Execution time':i, 'Execution left':i , 'Completed': 'no'}
    queue.append(dict_)
    k += 1
    
#creating the extra jobs that arrive later
if g!=None:
    a = [ g.split(';') ][0]

    more_work = []
    for i in list(a):
        string = 'Job' + str(k)
        temp = i.split(',')
        dict_ ={'id':string,'Arrival Time': int(temp[0]),'Strt_Time': 'n/a','Fin_Time': 'n/a','Execution time':int(temp[1]), 'Execution left':int(temp[1]) , 'Completed': 'no'}
        more_work.append(dict_)
        k += 1
        more_work = sorted(more_work, key=itemgetter('Arrival Time'))  #sorting this list by arrival time
    for i in more_work:
        print(i)

else:
    more_work=[]
    
for i in queue:
    print(i)

for i in more_work:
    print(i)


#job_queue = queue.copy()
job_queue = list(queue)


for i in job_queue:
    print(i)

job_queue.pop(0) #popping front example

for i in job_queue:
    print(i)
    
#job_queue = queue.copy()
#job_queue_extra = more_work.copy()

job_queue = list(queue)
job_queue_extra = list(more_work)

if len(job_queue_extra)!=0: #there might not be any extra jobs
    time_j = job_queue_extra[0].get('Arrival Time') #save the time when the first extra job will arrive
else:
    time_j = -10

done_jobs = [] #save the comepleted jobs here
time = 0; #keeping the time
order = [] #save the order in which the jobs get cpu time here

while(len(job_queue)!=0): #while the job queue is not empty
    
    cpu_time_remaining = d #reseting this every loop
    current = job_queue.pop(0) #pop the front of the queue
    
    order.append(current.get('id')) #append current's job_id in "order" so we know in what order the jobs got cpu time
    
    if (current['Strt_Time'] == 'n/a'): #set the starting time of the job
            current['Strt_Time']=time
    
    
    while(cpu_time_remaining!=0): #give the job the cpu
        
        time += 1
        cpu_time_remaining -= 1
        
        
        
        #we check if a extra job has arrived
        if(time == time_j): 
            
            #what if more than one extra job have the same arriving time? So..
            new = [i for i in job_queue_extra if i.get('Arrival Time') != time_j] #get all other jobs
            new = sorted(new, key=itemgetter('Arrival Time')) #sort them in ascending order of their arrival time
            
            now = [i for i in job_queue_extra if i.get('Arrival Time')==time_j] #get all jobs that need to be queued r8 now
            
            #append all the arrived jobs in the job queue as asked in the assignment
            for i in now:
                job_queue.append(i)
                
            job_queue_extra = new #update the extra jobs queue
            
            #if there are more extra jobs , get the next arrival time. Recall that these extra jobs are sorted in asc order
            if len(job_queue_extra) != 0:
                time_j = job_queue_extra[0].get('Arrival Time')
                
            
        
        
        #the job executes and its remaining execution time decreases
        current['Execution left'] = current.get('Execution left') - 1
        
        #at the end of the time slot if a job still needs more exection time, append it back into the job queue 
        if (cpu_time_remaining == 0) and current['Execution left'] !=0:
            job_queue.append(current)
            
        
        
        if (time%display_time == 0): #display at every given 'display interval'
            display(time,done_jobs,job_queue,current,order)

        
        #if the job finished execution , update its status and append it to the done_jobs queue
        if current['Execution left'] == 0:
            current['Completed'] = 'yes'
            current['Fin_Time'] = time
            done_jobs.append(current)
            break
    
    
    
print("Total time taken: ", time)

nprint(list(done_jobs), "Jobs Completed")
print("\nOrder: ",[i[3] for i in order])