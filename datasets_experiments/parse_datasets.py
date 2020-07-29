import numpy as np
from scipy.io import arff
from glob import glob

for fn in glob('datasets/*/*.arff'):
	print(fn)
	try:
		data, meta = arff.loadarff(fn)
	except:
		continue
	try:
		class_column = list(map(lambda x:x.lower(),meta._attributes)).index('class')
	except:
		continue
		print(meta._attributes)
	print('class column',class_column)

	data = np.array(data)
	ys = []
	xs = []
	skip_it = False
	for item in data:
		ys.append( str(item[class_column]) )
		xs.append( [x for i,x in enumerate(item) if i!=class_column] )
		if 'b' in "".join(map(str,xs[-1])):
			skip_it = True
	if skip_it: continue
	classes = list(sorted(set(ys)))
	print("classes",len(classes))
	ys = [classes.index(x) for x in ys]
	ofn1 = fn.replace('datasets','datasets_parsed').replace('.arff','.features').replace('artificial\\','artificial_').replace('real-world\\','real-world_')
	ofn2 = fn.replace('datasets','datasets_parsed').replace('.arff','.gt').replace('artificial\\','artificial_').replace('real-world\\','real-world_')

	with open(ofn1,'w') as ofh:
		for item in xs:
			print("\t".join(map(str,item)),file=ofh)
	with open(ofn2,'w') as ofh:
		for item in ys:
			print(item,file=ofh)
