import numpy as np

#array = eval(input("Enter the array of (xi,yi) positions as [x0,y0,x1,y1]: "))
array=[0.2,-3.75,-1.7,2.2,1.7,4.5,-0.5,1.4,-0.8,2.7,6.5,-4.8,4.3,-2.5,-5,-5,-4.6,6.1,-6.8,6.1]
array = np.array(array)
N = len(array)

if (N%2==0):
    n=int(N/2)
    array.shape = (n,2)
    print(array)
    array_mean = np.sum(array/n,axis=0)
    mean_x = array_mean[0]
    mean_y = array_mean[1]
    print("mean_x=",mean_x,"mean_y=",mean_y)
    
    xi_minus_xmean=[]
    yi_minus_ymean=[]
    P = np.zeros((2,2))
    
    for i in range(n):
        xi_minus_xmean.append(array[i,0]-mean_x)
        yi_minus_ymean.append(array[i,1]-mean_y)
        P[0][0] = P[0][0] + xi_minus_xmean[i]*xi_minus_xmean[i]
        P[1][1] = P[1][1] + yi_minus_ymean[i]*yi_minus_ymean[i]
        P[0][1] = P[0][1] + xi_minus_xmean[i]*yi_minus_ymean[i]
        P[1][0] = P[0][1]
    P = P/n
    print("Covariance matrix P=",P)
    
    #print(np.sqrt(P[0][0]),np.sqrt(P[1][1]))
    #print(np.std(array[:,0]),np.std(array[:,1]))
        
else:
    print("Incomplete array!")