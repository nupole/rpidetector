import matplotlib.pyplot
import matplotlib.colors

file = open('Run207.txt', 'r')
linears1 = []
quadratics1 = []
corrlins1 = []

for row in file:
    columns = row.split()
    if((float(columns[2]) < 0.0025 + float(columns[1])) and (float(columns[2]) > -0.0025 + float(columns[1]))):
    	linears1.append(float(columns[1]))
    	if(float(columns[2]) != -1.0):
	    quadratics1.append(float(columns[2]))
	    corrlins1.append(float(columns[1]))

bin=[x * 0.0001 for x in range(0,300)]

matplotlib.pyplot.figure(1)
matplotlib.pyplot.hist(linears1, bins = bin, normed=1.0, alpha=0.5, label = 'Linear')
matplotlib.pyplot.hist(quadratics1, bins = bin, normed=1.0, alpha=0.5, label='Quadratic')
matplotlib.pyplot.legend()
matplotlib.pyplot.xlabel('S1')
matplotlib.pyplot.title('S1 Distribution')
matplotlib.pyplot.show()

print len(quadratics1)

matplotlib.pyplot.figure(2)
matplotlib.pyplot.hist2d(corrlins1, quadratics1, bins=100, norm=matplotlib.colors.LogNorm())
matplotlib.pyplot.colorbar()
matplotlib.pyplot.show()

file.close()
