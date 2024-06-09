#!/usr/bin/env python
import sys
import numpy as np

frFileName = sys.argv[1]

fr=open(frFileName)
basename = frFileName.split('.')[0]
fw=open('%s.coord'%basename,'w')

record=False
i=0
recordName = False
ligNames = []
ligCharges = []
ligAtomIds = []
atomName = []
atomType = []
resTypes = []
resIds = []
coordMat = []
#update to the print function
print ('Reading parameters...')
for line in fr:
 if recordName:
  name=line.strip()
  recordName = False
 if line.find('@<TRIPOS>MOLECULE')!=-1:
  recordName = True

 if line.find('@<TRIPOS>BOND')!=-1:
  record=False

 if record:
  sp=line.split()
  fw.write(name+'\t'+sp[0]+'\t'+sp[1]+'\t'+sp[2]+'\t'+sp[3]+'\t'+sp[4]+'\t'+sp[8]+'\n')
  coordMat.append([ sp[2],sp[3],sp[4] ])
  ligNames.append(name)
  ligCharges.append(sp[8])
  ligAtomIds.append(sp[0])
  atomName.append(sp[1])
  atomType.append(sp[5])
  resTypes.append(sp[7][:3])
  resIds.append(sp[6])

 if line.find('@<TRIPOS>ATOM')!=-1:
  i=i+1
  record=True
fr.close()
fw.close()
#update to the print function
print ('Array conversion...')
ligNames = np.array(ligNames)
ligCharges = np.array(ligCharges, dtype=float)
ligAtomIds = np.array(ligAtomIds, dtype=int)
resTypes = np.array(resTypes)
atomName = np.array(atomName)
resIds = np.array(resIds, dtype=int)
coordMat = np.array(coordMat, dtype=float)
atomType = np.array(atomType)
#update to the print function
print ('Array filtering...')
filter = np.bool_(1-np.isnan(coordMat).any(axis=1))
#update to the print function
print ('Writing parameter files...')
#np.save('%s_names.npy'%basename, ligNames[filter])
#np.save('%s_charges.npy'%basename, ligCharges[filter])
#np.save('%s_atomIds.npy'%basename, ligAtomIds[filter])
np.save('%s_coordMat.npy'%basename, coordMat[filter])
#np.save('%s_resTypes.npy'%basename, resTypes[filter])
#np.save('%s_resIds.npy'%basename, resIds[filter])
#np.save('%s_atomName.npy'%basename, atomName[filter])
#np.save('%s_atomType.npy'%basename, atomType[filter])
np.savez('%s_parameters.npz'%basename, names=ligNames[filter], charges=ligCharges[filter], atomIds=ligAtomIds[filter], resTypes=resTypes[filter], resIds=resIds[filter], atomNames=atomName[filter], atomTypes=atomType[filter])
