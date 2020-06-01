from sarcscovdb import case_history
import matplotlib.pyplot as plt
import numpy as np

new_cases=[]
previous_daycases=0
daycases=0
xlegend=[x for x in range(1,len(case_history)+1)]
xaxislegend=[x for x in range(1,len(case_history)+1,5)]

for v in case_history.values():
    daycases=v-previous_daycases
    new_cases.append(daycases)
    previous_daycases=v

daycases_reg= np.poly1d(np.polyfit(xlegend,new_cases, 10))

height=float(10)
width=float(height)*(1+1/4)
plt.figure(figsize=(width,height))

plt.plot(xlegend, daycases_reg(xlegend))
plt.scatter(xlegend, new_cases)

plt.title("CoViD-19 in Portugal", fontsize=24) 
plt.xlabel("Dias(1ºdia:2/03/2020)", fontsize=14) 
plt.ylabel("Número de Casos", fontsize=14)
plt.grid()
plt.xticks(xaxislegend)

plt.savefig('NewCasesPerDay.png')
plt.show()