import matplotlib.pyplot as plt
import numpy as np

filename = "/homes/kt3118/Desktop/Robotics_CO333/Logfiles/feedforward290.txt"

with open(filename, "r") as f :
    file = f.read()
    files = file.split("\n")
# print(files)
a=0
b=0
#file = open(filename, "r")
N = sum(1 for line in files)
# print(N)
logs = np.zeros((N,5))
i=0
#file = str(file)
for line in files:
    temp = line.split("\t")
    if len(temp[0]) != 0:
        if len(temp) < 5:
            pass
        else:
            if a == 0 :
                time = float(temp[0])
                refangle0 = float(temp[1])
                angle0 = float(temp[2])
                refangle1 = float(temp[3])
                angle1 = float(temp[4])
                #logs[i][0] = float(temp[0])
                #logs[i][1] = float(temp[1])
                #logs[i][2] = float(temp[2])
                #logs[i][3] = float(temp[3])
                #logs[i][4] = float(temp[4])
            else :
                logs[i][0] = float(temp[0]) - time
                logs[i][1] = float(temp[1]) - refangle0
                logs[i][2] = float(temp[2]) - angle0
                logs[i][3] = float(temp[3]) - refangle1
                logs[i][4] = float(temp[4]) - angle1
            a = a+1
        i=i+1

logs=logs[:N-1]
#print(list(logs[:,0]))

#print(a+b)
fig1 = plt.figure(1)
plt.plot(list(logs[:,0]), list(logs[:,1]), 'g', list(logs[:,0]), list(logs[:,2]), 'r')
plt.xlabel("Time (s)", fontsize=10)
plt.ylabel("Motor angle", fontsize=10)
plt.title("Optimal PID Gains, Feedforward = 290/20")
fig1.show()
plt.show()
