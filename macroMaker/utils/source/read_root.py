import os
import sys
import uproot

the_dir=sys.argv[1]
recycling=int(sys.argv[2])

folders = 0

for root, dirnames, filenames in os.walk(the_dir+'/phsp/output'):
    folders += len(dirnames)

for i in range(0,folders):
    nb_particle = nb_particle2 = 0
    root_phsp_file = the_dir+'/phsp/output/'+str(i)+'/myIAEA.root'
    phsp = uproot.open(root_phsp_file)["PhaseSpace"]
    nb_particle = phsp.numentries
    
    nb_particle2 = nb_particle * recycling

    
    #with open(the_dir+'/clinic/mac/'+str(i)+'/main.mac', 'a') as file:
    with open('p.dat', 'a') as file:
    	file.write(str(nb_particle2)+'\n')