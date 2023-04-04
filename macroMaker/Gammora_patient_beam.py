import os
import glob
import shutil
import fileinput
import pydicom as dcm
import pandas as pd
import numpy as np
import Gammora_study
import Gammora_beam
import Gammora_generator
import Gammora_print
from stl import mesh


global UtilsMac
global UtilsPlacements
global UtilsMacActor
global UtilsMacPhantom
global config_default_patient
global UtilsMLC
global root

root = os.getcwd()


UtilsPlacements=root+'/utils/placement_template/'
UtilsMac=root+'/utils/mac/mac_template/'
UtilsMLC=root+'/utils/mlc/'
UtilsMacActor=root+'/utils/mac/actor/'
UtilsMacPhantom=root+'/utils/mac/phantom/'
config_default_patient = {}



class GammoraPatientBeam(Gammora_beam.GammoraBeam):


#==========================================================================================

# Initialisation
    def __init__(self, patient, beam, config, GammoraStudy):       

# Default Config:

        config_default_patient['VISU']=False
        config_default_patient['VISU_MODE']=0
        config_default_patient['PHYSICS']=True
        config_default_patient['PHYSICS_NAME']='Xphysics.macX'
        config_default_patient['HEAD_SIMULATION']=True
        config_default_patient['PATIENT_SIMULATION']=True
        config_default_patient['TEST_SIMULATION']=False # ** not working yet
        config_default_patient['SPLIT_TYPE']='dyn'
        config_default_patient['MLC']=True
        config_default_patient['PHSP_ACTOR']=True
        config_default_patient['PATIENT_ACTOR']=True
        config_default_patient['PHSP_ACTOR_FILE']='root_make_phspR_cyl.mac'
        config_default_patient['PATIENT_ACTOR_FILE']='dose_actor.mac' #'dose_actor.mac'
        config_default_patient['PATIENT_ACTOR_SIZE']=[300.0, 300.0, 300.0]
        config_default_patient['PATIENT_ACTOR_RESOLUTION']=[300, 300, 300]
        config_default_patient['PATIENT_CT']=True
        config_default_patient['PHANTOM']=False
        config_default_patient['PHANTOM_FILE']='waterbox300.mac'
        config_default_patient['SOURCE']=True
        config_default_patient['SOURCE_GAGA']=False
        config_default_patient['SOURCE_IAEA']=True
        config_default_patient['NB_PART']=1000000000
        config_default_patient['RECYCLING']=100

        config_default_patient['CALMIP_USER']='leste'
        config_default_patient['AUTO_SENDING']=False
        config_default_patient['AUTO_LAUNCHING']=False

#  Study Name      
        self._set_study_input_name(GammoraStudy)

# Set patient data directory
        self._set_local_input_dir(root+'/input/patient/'+str(GammoraStudy._get_study_input_name()))


# Simu Name        
        if config['SIMU_NAME'] == 'auto': 
            self._set_beam_name(GammoraStudy._get_study_name()+'_'+str(beam.BeamID))
        else:
            self._set_beam_name(config['SIMU_NAME']+'_'+beam.BeamID)


        Gammora_print._title("Creating GAMMORA Beam object for patient : "+ self._get_study_input_name() + ' ' + beam.BeamID)
        Gammora_print._title2("Simulation Name : " + self._get_beam_name())
        Gammora_print._separator2()
        Gammora_print._title("General : ")

# Material
        self._set_material(True)
        self._set_material_name('TBMaterials.tb')

        Gammora_print._title2("Material Table : " + str(self._get_material()))
        Gammora_print._title2("Material Table Name : " + str(self._get_material_name()))

        
# Visualization        

        if config['VISU'] == 'auto':
            self._set_visualization(config_default_patient['VISU'])
            Gammora_print._title2("Visualisation : "+ str(bool(self._get_visualization())))
            if self._get_visualization() == True:
                self._set_visualization_mode(config_default_patient['VISU_MODE'])
                Gammora_print._title2("Visualisation Mode : "+str(self._get_visualization_mode()))              
        elif config['VISU'] == '0':
            self._set_visualization(bool(int(config['VISU'])))
            Gammora_print._title2("Visualisation : "+str(bool(self._get_visualization())))
        elif config['VISU'] == '1':
            self._set_visualization(bool(int(config['VISU'])))
            self._set_visualization_mode(int(config['VISU']))
            Gammora_print._title2("Visualisation : "+str(bool(self._get_visualization())))
            Gammora_print._title2("Visualisation Mode : "+str(self._get_visualization_mode()))
        elif config['VISU'] == '2':
            self._set_visualization(True)
            self._set_visualization_mode(int(config['VISU']))
            Gammora_print._title2("Visualisation : "+str(bool(self._get_visualization_mode())))
            Gammora_print._title2("Visualisation Mode : "+str(self._get_visualization_mode()))

# Physics

        if config['PHYSICS'] == 'auto':
            self._set_physics(config_default_patient['PHYSICS'])
            Gammora_print._title2("Physics : "+ str(bool(self._get_physics())))
            if self._get_physics() == True:
                self._set_physics_name(UtilsMac+config_default_patient['PHYSICS_NAME'])
                #Gammora_print._title2("Physics file name :"+config_default_patient['PHYSICS_NAME'])
        elif config['PHYSICS'] == '0':
            self._set_physics(bool(int(config['PHYSICS'])))
            Gammora_print._title2("Physics :    "+str(bool(self._get_physics())))
        elif config['PHYSICS'] == '1':
            self._set_physics(bool(int(config['PHYSICS'])))
            self._set_physics_name(UtilsMac+config_default_patient['PHYSICS_NAME'])
            Gammora_print._title2("Physics : "+str(bool(self._get_physics())))
            Gammora_print._title2("Physics file name : "+str(bool(self._get_physics_name())))
        else:
            self._set_physics(bool((config['PHYSICS'])))
            self._set_physics_name(UtilsMac+(config['PHYSICS']))
            Gammora_print._title2("Physics : "+ str(bool(self._get_physics())))
            Gammora_print._title2("Physics file name : "+str(config['PHYSICS']))

# Head part simulation

        if config['HEAD_SIMULATION'] == 'auto':
            self._set_head_part_siumulation(config_default_patient['HEAD_SIMULATION'])
            Gammora_print._title2("Head Simulation : " + str(bool(self._get_head_part_siumulation())))
        elif config['HEAD_SIMULATION'] == '0':
            self._set_head_part_siumulation(bool(int(config['HEAD_SIMULATION'])))
            Gammora_print._title2("Head Simulation : " + str(bool(self._get_head_part_siumulation())))
        elif config['HEAD_SIMULATION'] == '1':
            self._set_head_part_siumulation(bool(int(config['HEAD_SIMULATION'])))
            Gammora_print._title2("Head Simulation : " + str(bool(self._get_head_part_siumulation())))

# Patient part simulation
                
        if config['PATIENT_SIMULATION'] == 'auto':
            self._set_patient_part_siumulation(config_default_patient['PATIENT_SIMULATION'])
            Gammora_print._title2("Patient Simulation : " + str(bool(self._get_patient_part_siumulation())))
        elif config['PATIENT_SIMULATION'] == '0':
            self._set_patient_part_siumulation(bool(int(config['PATIENT_SIMULATION'])))
            Gammora_print._title2("Patient Simulation : " + str(bool(self._get_patient_part_siumulation())))
        elif config['PATIENT_SIMULATION'] == '1':
            self._set_patient_part_siumulation(bool(int(config['PATIENT_SIMULATION'])))
            Gammora_print._title2("Patient Simulation : " + str(bool(self._get_patient_part_siumulation())))

# Test simulation in local

        # To do **
        if config['TEST_SIMULATION'] == 'auto':
           #self._set_test_siumulation(config_default_patient['TEST_SIMULATION'])
           #print(" * Test Simulation:    ", str(bool(self._test_siumulation())))
           pass
        elif config['TEST_SIMULATION'] == '0':
           #self._set_test_siumulation(bool(int(config['TEST_SIMULATION'])))
           #print(" * Test Simulation:    ",self._get_test_siumulation())
           pass
        elif config['TEST_SIMULATION'] == '1':
            pass
           #self._set_test_siumulation(bool(int(config['TEST_SIMULATION'])))
           #print(" * Test Simulation:    ",self._get_test_siumulation())
        
# Split type

        if config['SPLIT_TYPE'] == 'stat':
            self._set_split_type('stat')
        elif config['SPLIT_TYPE'] == 'dyn':
                self._set_split_type('dyn')
        if config['SPLIT_TYPE'] == 'auto':
            self._set_split_type(config_default_patient['SPLIT_TYPE'])
        Gammora_print._title2("Split Type : "+str(self._get_split_type()))

# Number of index        

        self._set_beam_nb_cpi(beam._get_nb_cpi())
        if config['INDEX'] == 'auto':
            self._set_nb_index(beam._get_nb_cpi())
        else:
            if self._get_split_type() == 'stat':
                if int(config['INDEX']) < beam._get_nb_cpi():
                    Gammora_print._warning("Index of value : "+config['INDEX'], ["For this patient, with 'stat splitting' the number of index must be at least : "+str(beam._get_nb_cpi()), 
                    "Number of Index is automatically set to : "+str(beam._get_nb_cpi())])
                    self._set_nb_index(beam._get_nb_cpi())
                if int(config['INDEX']) <= beam._get_nb_cpi():
                    self._set_nb_index(beam._get_nb_cpi())
                if int(config['INDEX']) > beam._get_nb_cpi():
                    self._set_nb_index(int(config['INDEX']))
            if self._get_split_type() == 'dyn':
                self._set_nb_index(int(config['INDEX']))
        Gammora_print._title2("Number of Index : " + str(self._get_nb_index()))

# Head Part Simulation
# Geometry HEAD

        Gammora_print._separator2()
        Gammora_print._title("Head Part Simulation Geometry :")

# + MLC
        if self._get_head_part_siumulation() == True:
            if config['MLC'] == 'auto':
                self._set_mlc(config_default_patient['MLC'])
                self._set_mlc_sequence(beam._get_mlc())
                #self._create_mlc_file(beam)
            elif config['MLC'] == '0':
                self._set_mlc(bool(int(config['MLC'])))
                #Gammora_print._warning('MLC is disabled', [''])
            elif config['MLC'] == '1':
                self._set_mlc(bool(int(config['MLC'])))
                self._set_mlc_sequence(beam._get_mlc())
                #self._create_mlc_file(beam)
            else:
                print('It is not possible to use a mlc file for patient')
                exit()
            #print(" * MLC:    ", str(self._get_mlc()))    

# + Get patient data (deals with splitting : interpolation if stat plitting)

            if self._get_split_type() == 'dyn':                             
                self._set_gantry_angle(beam._get_gantry_angle())
                self._set_colli_angle((np.zeros(beam._get_nb_cpi())+beam._get_colli_angle()).tolist())
                self._set_x1(beam._get_x1())
                self._set_x2(beam._get_x2())
                self._set_y1(beam._get_y1())
                self._set_y2(beam._get_y2())
                self._set_dose_rate(beam._create_dose_rate().tolist())
                if self._get_mlc() == True:
                    self._create_mlc_file(beam)
            
            if self._get_split_type() == 'stat':                        # all setting for head component jaw, mlc, colli etc ... are set in 'interp' functiun
                self._interp_geometry(beam , self._get_nb_index())
                if self._get_mlc() == True:
                    self._create_mlc_file(beam)


# + Gantry
            #self._set_gantry_angle
            if config['GANTRY'] != 'auto' or config['GANTRY_STOP'] != 'auto' :
                Gammora_print._title2("Gantry :")
                Gammora_print._warning("Manual Gantry position when using patient data is not allowed", ["Positions from patient data are automatically used"])

            if all(angle == self._get_gantry_angle()[0] for angle in self._get_gantry_angle()) != True:
                Gammora_print._title2("Arc Thearpy")
                Gammora_print._title2("Gantry Angle Start : " + str(self._get_gantry_angle()[0])+ "°")
                Gammora_print._title2("Gantry Angle Stop :" + str(self._get_gantry_angle()[-1])+ "°")
            else:
                Gammora_print._title2("Static Gantry position")
                Gammora_print._title2("Gantry Angle:    "+ str(self._get_gantry_angle()[0])+ "°")

# + Colli            
            if config['COLLI'] != 'auto':
                Gammora_print._title2("Colli :")
                Gammora_print._warning("Manual Colli position when using patient data is not allowed", ["Positions from patient data are automatically used"])
                #Gammora_print._warning("Colli Angle : "+ str(self._get_colli_angle()[0])+"°", ["GAMMORA does not support colli roatation during beam"])              
            else:
                Gammora_print._title2("Colli Angle : "+ str(self._get_colli_angle()[0])+"°" +" (GAMMORA does not support colli roatation during beam)")
                #Gammora_print._warning("Colli Angle : "+ str(self._get_colli_angle()[0])+"°", ["GAMMORA does not support colli roatation during beam"])              
# + Jaws
# ++ X1
            if config['X1'] != 'auto':
                Gammora_print._title2("X1 :")
                Gammora_print._warning("Manual X1 position when using patient data is not allowed", ["Positions from patient data are automatically used"])
            
            if all(pos == self._get_x1()[0] for pos in self._get_x1()) != True:
                Gammora_print._title2("X1 Initial Position : " + str(self._get_x1()[0])+ " mm (Dynamic Jaw)")
                Gammora_print._title2("X1 Final Position : " + str(self._get_x1()[-1])+ " mm  (Dynamic Jaw)")
            else:
                Gammora_print._title2("X1 Position : "+ str(self._get_x1()[0])+ " mm (Static Jaw)")
# ++ X2            
            if config['X2'] != 'auto':
                Gammora_print._title2("X2 :")
                Gammora_print._warning("Manual X2 position when using patient data is not allowed", ["Positions from patient data are automatically used"])
            
            if all(pos == self._get_x2()[0] for pos in self._get_x2()) != True:
                Gammora_print._title2("X2 Initial Position : " + str(self._get_x2()[0]) + " mm (Dynamic Jaw)")
                Gammora_print._title2("X2 Final Position : " + str(self._get_x2()[-1]) + " mm (Dynamic Jaw)")
            else:
                Gammora_print._title2("X2 Position : " + str(self._get_x2()[0]) + " mm (Static Jaw)")
# ++ Y1           
            if config['Y1'] != 'auto':
                Gammora_print._title2("Y1 :")
                Gammora_print._warning("Manual Y1 position when using patient data is not allowed", ["Positions from patient data are automatically used"])
            
            if all(pos == self._get_y1()[0] for pos in self._get_y1()) != True:
                Gammora_print._title2("Y1 Initial Position : " + str(self._get_y1()[0]) + " mm (Dynamic Jaw)")
                Gammora_print._title2("Y1 Final Position : " + str(self._get_y1()[-1]) + " mm (Dynamic Jaw)")
            else:
               Gammora_print._title2("Y1 Position : " + str(self._get_y1()[0]) + " mm  (Static Jaw)")
# ++ Y2        
            if config['Y2'] != 'auto':
                Gammora_print._title2("Y2 :")
                Gammora_print._warning("Manual Y2 position when using patient data is not allowed", ["Positions from patient data are automatically used"])
            
            if all(pos == self._get_y2()[0] for pos in self._get_y2()) != True:
                Gammora_print._title2("Y2 Initial Position : " + str(self._get_y2()[0]) + " mm  mm (Dynamic Jaw)")
                Gammora_print._title2("Y2 Final Position : " + str(self._get_y2()[-1]) + " mm (Dynamic Jaw)")
            else:
                Gammora_print._title2("Y2 Position : " + str(self._get_y2()[0]) + " mm (Static Jaw)")
# MLC (print)
            Gammora_print._title2("MLC : " + str(bool(self._get_mlc())))

            
# + Source  
            Gammora_print._separator2()
            Gammora_print._title("Source (Head Part Simulation) :")          

            if config['SOURCE'] == 'auto':
                self._set_source(config_default_patient['SOURCE'])
                Gammora_print._title2("Source : " + str(self._get_source()))
            elif config['SOURCE'] == '0':
                self._set_source(bool(int(config['SOURCE'])))
                Gammora_print._title2("Source : " + str(self._get_source()))
            else:  # iaea or gaga
                self._set_source(True)
                Gammora_print._title2("Source : " + str(self._get_source()))
# + Source type            
            if self._get_source() == True:
                if config['SOURCE'] == 'gaga':
                    self._set_source_iaea(False)
                    self._set_source_gaga(True)
                    self._set_source_root(False) # not working
                    self._set_source_gps(False)  # not working
                    Gammora_print._title2("Source Type : GAGA")
                elif config['SOURCE'] == 'iaea':
                    self._set_source_iaea(True)
                    self._set_source_gaga(False)
                    self._set_source_root(False) #not working
                    self._set_source_gps(False) #not working
                    Gammora_print._title2("Source Type : IAEA")
                else: # if auto
                    self._set_source_iaea(config_default_patient['SOURCE_IAEA'])
                    self._set_source_gaga(config_default_patient['SOURCE_GAGA'])
                    if self._get_source_gaga() == True :
                        Gammora_print._title2("Source Type : GAGA")
                    elif self._get_source_iaea() == True :
                        Gammora_print._title2("Source Type : IAEA")
                    else:
                        Gammora_print._warning("No source type in set in default Config", ["Set a source type by default"])
                    #self._set_source_root(config_default_patient['SOURCE_IAEA']) #not working
                    #self._set_source_gps(config_default_patient['SOURCE_IAEA']) #not working
# Energy                
                if config['ENERGY'] == 'auto':
                    self._set_energy(beam._get_energy())
                    Gammora_print._title2("Energy : " + str(self._get_energy()))
                elif config['ENERGY'] == beam._get_energy():
                    self._set_energy(config['ENERGY'])
                    Gammora_print._title2("Energy : " + str(self._get_energy()))
                else:
                    Gammora_print._title2("Energy : " + config['ENERGY'])
                    Gammora_print._warning("Engergy choosen is different from patient data", [])
                    self._set_energy(config['ENERGY'])
# Recycling
                if self._get_patient_part_siumulation() == True:
                    if config['RECYCLING'] == 'auto':
                        self._set_recycling(config_default_patient['RECYCLING'])
                    else:
                        self._set_recycling(int(config['RECYCLING']))
                    #print('*Recycling of reducued phase space for Patient simulation:     ', self._get_recycling())
# Number of particle
                if config['NB_PART'] != 'auto' and self._get_source_iaea() ==True:
                    self._set_manual_nb_part(False)
                    Gammora_print._title2('Number of particle (including recycling seeting) :')
                    Gammora_print._warning('When using IAEA PHSP number of particle is set automatically', ['Number of particle set to '+str(self._get_nb_part_tot_varian()[0]*self._get_recycling()), str(self._get_nb_part_tot_varian()[1])+"\% Varian PHSP used"])   
                
                if config['NB_PART'] == 'auto' and self._get_source_iaea() ==True:
                    self._set_manual_nb_part(False)
                    Gammora_print._title2("Number of particle (including recycling seeting) : "+str(self._get_nb_part_tot_varian()[0]*self._get_recycling()) + " ("+str(self._get_nb_part_tot_varian()[1])+" % Varian PHSP used)")
                                       
                elif config['NB_PART'] == 'auto' and self._get_source_gaga() == True:
                    self._set_manual_nb_part(False)
                    self._set_gaga_nb_part(config_default_patient['NB_PART'])
                    Gammora_print._title2("Number of particle (including recycling seeting) : "+str(config_default_patient['NB_PART']))
                elif config['NB_PART'] != 'auto' and self._get_source_gaga() == True:
                    self._set_manual_nb_part(True)
                    self._set_gaga_nb_part(int(config['NB_PART']))
                    Gammora_print._title2("Number of particle (including recycling seeting) : "+str(self._get_gaga_nb_part()))

# Recycling print
                Gammora_print._title2("Rcycling of Reduced Phase Space : " + str(self._get_recycling()))
                
# No Head Part Simulation
        else:
            Gammora_print._title2("Head Part Simulation is disabled !")
# Patient Part Simulation

        Gammora_print._separator2()
        Gammora_print._title("Patient Part Simulation :")

        if self._get_patient_part_siumulation() == True:

# Phantom and Patient CT

            if config['PHANTOM'] == 'auto':
                self._set_phantom(config_default_patient['PHANTOM'])
                self._set_patient_ct(config_default_patient['PATIENT_CT'])

                if self._get_phantom() == True:
                    self._set_phantom_name(UtilsMacPhantom+config_default_patient['PHANTOM_FILE'])

            elif config['PHANTOM'] == '0':
                self._set_phantom(False)
                self._set_patient_ct(False)
            
            else: 
                if config['PHANTOM'].endswith(".mac"):
                    self._set_phantom(True)
                    self._set_patient_ct(False)
                    self._set_phantom_name(UtilsMacPhantom+config['PHANTOM'])

                if config['PHANTOM'].endswith(".mhd"):
                    self._set_phantom(False)
                    self._set_patient_ct(False) #set to true whan done to do **
                    print("Simulation on mhd image not possible yet")
                    self._set_phantom_name(UtilsMacImages+config['PHANTOM'])
            
            if self._get_patient_ct() == True:
                self._set_patient_ct_name(root+'/input/patient/'+GammoraStudy._get_study_input_name()+'/dicom/ct')
                self._set_isocenter_position(beam._get_isocenter())
                self._set_patient_orientation(1)
                self._create_stl_couch(patient)

            Gammora_print._title2("Simulation On Phantom : " + str(self._get_phantom()))
            Gammora_print._title2("Simulation On Patient CT : " + str(self._get_patient_ct()))

            if self._get_phantom() == True:
                Gammora_print._title2("Phantom file : " + config['PHANTOM'])
                Gammora_print._title2("Phantom Motion : Not yet possible")
            if self._get_patient_ct() == True:
                Gammora_print._title2("Dicom CT of patient : " + self._get_study_input_name())

# No Patient Part Simulation

        else:
             Gammora_print._title2("Patient Part Simulation is disabled !")
# Actor Difinition
        Gammora_print._separator2()
        Gammora_print._title('Actor Definition')

        if self._get_head_part_siumulation() == True:

# + PHSP Actor
            if config['PHSP_ACTOR'] == 'auto':
                self._set_phsp_actor(config_default_patient['PHSP_ACTOR'])
                if self._get_phsp_actor() == True:
                    self._set_phsp_actor_name(UtilsMacActor+config_default_patient['PHSP_ACTOR_FILE'])
            
            elif config['PHSP_ACTOR'] == '0':
                self._set_phsp_actor(bool(int(config['PHSP_ACTOR'])))

            elif config['PHSP_ACTOR'] == '1':
                self._set_phsp_actor(bool(int(config['PHSP_ACTOR'])))
                self._set_phsp_actor_name(UtilsMacActor+config_default_patient['PHSP_ACTOR_FILE'])
            else:
                self._set_phsp_actor(True)
                self._set_phsp_actor_name(UtilsMacActor+config['PHSP_ACTOR'])

            if self._get_phsp_actor() == True:
                Gammora_print._title2("Phase space actor : " + str(self._get_phsp_actor()))
                if config['PHSP_ACTOR'] == 'auto' or config['PHSP_ACTOR'] == '1':
                    Gammora_print._title2("Phase space actor file : " + config_default_patient['PHSP_ACTOR_FILE'])
                else:
                    Gammora_print._title2("Phase space actor file : " + config['PHSP_ACTOR'])
            else:
                Gammora_print._title2("Phase space actor : " + str(self._get_phsp_actor()))

# + Patient Actor
            
        if self._get_patient_part_siumulation() == True:
            if config['PATIENT_ACTOR'] == 'auto':
                self._set_patient_actor(config_default_patient['PATIENT_ACTOR'])
                if self._get_patient_actor() == True:
                    self._set_patient_actor_name(UtilsMacActor+config_default_patient['PATIENT_ACTOR_FILE'])
            
            elif config['PATIENT_ACTOR'] == '0':
                self._set_patient_actor(bool(int(config['PATIENT_ACTOR'])))

            elif config['PATIENT_ACTOR'] == '1':
                self._set_patient_actor(bool(int(config['PATIENT_ACTOR'])))
                self._set_patient_actor_name(UtilsMacActor+config_default_patient['PATIENT_ACTOR_FILE'])
            else:
                self._set_patient_actor(True)
                self._set_patient_actor_name(UtilsMacActor+config['PATIENT_ACTOR'])

            if self._get_patient_actor() == True:
                Gammora_print._title2("Patient actor : " + str(self._get_patient_actor()))
                if config['PATIENT_ACTOR'] == 'auto' or config['PATIENT_ACTOR'] == '1':
                    Gammora_print._title2("Patient actor file : "+ config_default_patient['PATIENT_ACTOR_FILE'])
                else:
                    Gammora_print._title2("Phase space actor file : " + config['PATIENT_ACTOR'])
            else:
               Gammora_print._title2("Patient actor : "+ self._get_patient_actor())

# ++ Patient Actor Size

            if self._get_patient_actor() == True:
                if config['PATIENT_ACTOR'].endswith('.mac'):
                    Gammora_print._title2("Patient actor size defined in : " + str(config['PATIENT_ACTOR']))
                    Gammora_print._title2("Patient actor size defined in : " + str(config['PATIENT_ACTOR']))

                else:
                    if config['PATIENT_ACTOR_SIZE'] == 'auto':
                        self._set_patient_actor_size(self._get_size_from_rt_dose(patient))
                        Gammora_print._title2("Patient actor size (from Dicom RT dose) : " + str(self._get_patient_actor_size()) + " (x,y,z)")
                    else:
                        self._set_patient_actor_size([float(val) for val in list(config['PATIENT_ACTOR_SIZE'].split())])
                        Gammora_print._title2("Patient actor size (x,y,z) : " + str(self._get_patient_actor_size()))
        
    # ++ Patient Actor Resolution
                    
                    if config['PATIENT_ACTOR_RESOLUTION'] == 'auto':
                        self._set_patient_actor_resolution(self._get_resolution_from_rt_dose(patient))
                        Gammora_print._title2("Patient actor resolution (from Dicom RT dose) : " + str(self._get_patient_actor_resolution())+" (x,y,z)")
                    else:
                        self._set_patient_actor_resolution([int(val) for val in list(config['PATIENT_ACTOR_RESOLUTION'].split())])
                        Gammora_print._title2("Patient actor resolution (from Dicom RT dose) : " + str(self._get_patient_actor_resolution()))
     
# Add a GAMMORA Patient simu object to GAMMORA Patient Beam object 

        self.Simu = Gammora_generator.GammoraPatientSimu(config, self, GammoraStudy)
        

#========================================================================================================================
# Other Function       

# + oversampling of beam variable 

    def _interp_geometry(self, beam, a):

        if self._get_nb_index() > beam._get_nb_cpi():
            Gammora_print._warning("With 'stat splitting' and a number of index of : "+str(self._get_nb_index()), ['An oversampling of RT plan is performed', 'New values of : gantry, jaws, mlc, dose rate are obtained with linear interpolation',
            'Need to check gantry angle close to 0°'])

        if self._get_head_part_siumulation() == True:
            old_dose_rate=beam._create_dose_rate().tolist()
            old_gantry=beam._get_gantry_angle()
            old_colli=(np.zeros(beam._get_nb_cpi())+beam._get_colli_angle()).tolist() # assuming no dynamic rotation of colli
            old_x1=beam._get_x1()
            old_x2=beam._get_x2()
            old_y1=beam._get_y1()
            old_y2=beam._get_y2()

            if self._get_mlc() == True:
                old_mlc=beam._get_mlc()
        
            old_index=np.arange(0, beam._get_nb_cpi())

            if len(old_index) == 1:  

                if self._get_head_part_siumulation() == True:
                    new_x1=np.repeat(beam._get_x1(), self._get_nb_index()).tolist()
                    new_x2=np.repeat(beam._get_x2(), self._get_nb_index()).tolist()
                    new_y1=np.repeat(beam._get_y1(), self._get_nb_index()).tolist()
                    new_y2=np.repeat(beam._get_y2(), self._get_nb_index()).tolist()
                    new_dose_rate=np.ones(self._get_nb_index()).tolist()
                    new_gantry=np.repeat(beam._get_gantry_angle(), self._get_nb_index()).tolist()
                    new_colli=np.repeat(beam._get_colli_angle(), self._get_nb_index()).tolist()
                
                if self._get_mlc() == True:
                    new_mlc=[]
                    if self._get_mlc() == True:
                        for i in range(0, self._get_nb_index()):
                            new_mlc.append(old_mlc[0])

            if len(old_index) > 1:
                new_index=np.linspace(old_index.min(), old_index.max(), self._get_nb_index())        

                if self._get_head_part_siumulation() == True:
                    new_dose_rate=np.interp(new_index, old_index, old_dose_rate).tolist()
                    new_gantry=np.interp(new_index, old_index, old_gantry).tolist()
                    new_colli=np.interp(new_index, old_index, old_colli).tolist()
                    new_x1=np.interp(new_index, old_index, old_x1).tolist()
                    new_x2=np.interp(new_index, old_index, old_x2).tolist()
                    new_y1=np.interp(new_index, old_index, old_y1).tolist()
                    new_y2=np.interp(new_index, old_index, old_y2).tolist()

                    if self._get_mlc() == True:
                        
                        temp_mlc=[]
                        new_mlc=[]
                        for i in range(0, 120):
                                temp_mlc.append(np.zeros(len(old_index)))
                                j=0
                                for index in old_index:
                                    temp_mlc[i][j]=old_mlc[index][i]
                                    j=j+1
                        temp_mlc2=[]
                        for i in range(0, 120):
                                temp_mlc2.append(np.interp(new_index, old_index, temp_mlc[i]))

                        for i in range(0, len(new_index)):
                                new_mlc.append(np.zeros(120).tolist())
                                for j in range(0, 120):
                                    new_mlc[i][j]=temp_mlc2[j][i]
            self._set_x1(new_x1)
            self._set_x2(new_x2)
            self._set_y1(new_y1)
            self._set_y2(new_y2)
            self._set_dose_rate(new_dose_rate)
            self._set_gantry_angle(new_gantry)
            self._set_colli_angle(new_colli)
            if self._get_mlc() == True:
                self._set_mlc_sequence(new_mlc)

# + get size from Dicom RT dose 

    def  _get_size_from_rt_dose(self, patient):
        root = os.getcwd()
        try:
            rt_dose_file=glob.glob(root+"/input/patient/"+self._get_study_input_name()+"/dicom/RD*")[0]
            rt_dose=dcm.read_file(rt_dose_file)
            rt_dose_array=rt_dose.pixel_array
            shape=[rt_dose_array.shape[2], rt_dose_array.shape[1], rt_dose_array.shape[0]]
            spacing=[]
            for val in rt_dose.PixelSpacing: spacing.append(float(val))
            spacing.append(float(rt_dose.GridFrameOffsetVector[1]-rt_dose.GridFrameOffsetVector[0]))
            size=[]
            for a, b in zip(spacing, shape):
                size.append(a *float(b))
        except IndexError:
            size = config_default_patient['PATIENT_ACTOR_SIZE']
            print("")
            print("  !!! WARNING !!! ")
            print("         No RT Dose file found: Actor Size is defined to default value", config_default_patient['PATIENT_ACTOR_SIZE'])
            print("")
            

        return(size)

# + get resolution from Dicom RT dose 


    def  _get_resolution_from_rt_dose(self, patient):
        root = os.getcwd()
        try:
            rt_dose_file=glob.glob(root+"/input/patient/"+self._get_study_input_name()+"/dicom/RD*")[0]
            rt_dose=dcm.read_file(rt_dose_file)
            rt_dose_array=rt_dose.pixel_array
            rt_dose=dcm.read_file(rt_dose_file)
            rt_dose_array=rt_dose.pixel_array
            shape=[rt_dose_array.shape[2], rt_dose_array.shape[1], rt_dose_array.shape[0]]
        except IndexError:
            shape = config_default_patient['PATIENT_ACTOR_RESOLUTION']
            print("")
            print("  !!! WARNING !!! ")
            print("         No RT Dose file found: Actor Resolution is defined to default value: ", config_default_patient['PATIENT_ACTOR_RESOLUTION'])
            print("")
            

        return(shape)

# + Create radiotherapy Couch 

    def _create_stl_couch(self, patient):
        root = os.getcwd()
        try:
            rt_struct_file=glob.glob(root+"/input/patient/"+self._get_study_input_name()+"/dicom/RS*")[0]
            rs=dcm.read_file(rt_struct_file)

            #looking for couch structure in dicom rt struct
            i=0
            for st in rs.StructureSetROISequence:
                found1 = False
                found2 = False
                if st.ROIName == "CouchSurface" or st.ROIName == "CouchSurface1" :
                    ind_ext = i
                    found1 = True
                if st.ROIName == "CouchInterior" or st.ROIName == "CouchInterior1":
                    ind_int = i
                    found2 = True
                i = i+1

            if found1 != True and found2 != True:
                Gammora_print._title2('Couch Structure not found in Dicom RT Struct file -> Couch is not modelled ! ')
                self._set_couch(False)
                return
            else:
            
                x_ext=[]
                y_ext=[]
                z_ext=[]
                z_ext2=[]
                x_int=[]
                y_int=[]
                z_int=[]
                z_int2=[]  
                
                
                
                # compute STL file for Surface couch
                # get x y and z off courch surface values from dicom rt struct
                for i in range(0, len(rs.ROIContourSequence[ind_ext].ContourSequence[0].ContourData), 3):
                    x_ext.append(float(rs.ROIContourSequence[ind_ext].ContourSequence[0].ContourData[i]))
                for i in range(1, len(rs.ROIContourSequence[ind_ext].ContourSequence[0].ContourData), 3):
                    y_ext.append(float(rs.ROIContourSequence[ind_ext].ContourSequence[0].ContourData[i]))
                for i in range(2, len(rs.ROIContourSequence[ind_ext].ContourSequence[0].ContourData), 3):
                    z_ext.append(float(rs.ROIContourSequence[ind_ext].ContourSequence[0].ContourData[i]))
                for i in range(2, len(rs.ROIContourSequence[ind_ext].ContourSequence[-1].ContourData), 3):
                    z_ext2.append(float(rs.ROIContourSequence[ind_ext].ContourSequence[-1].ContourData[i]))

                y_center_ext = min(y_ext)+((max(y_ext)-min(y_ext))/2)
                pts_up=[]

                for i in range(len(x_ext)):
                    pt=[]
                    pt.append(x_ext[i])
                    pt.append(y_ext[i])
                    pt.append(z_ext[0])
                    pts_up.append(pt)

                origin1=[0, y_center_ext, z_ext[0]]

                stl_top=[]
                for i in range(0, len(pts_up)):
                    f=[]
                    z=i+1 
                    if z > len(pts_up)-1: 
                        f.append(pts_up[0])
                    else:
                        f.append(pts_up[z])
                    f.append(pts_up[i])
                    f.append(origin1)
                    stl_top.append(f)

                pts_down=[]
                for i in range(len(x_ext)):
                    pt=[]
                    pt.append(x_ext[i])
                    pt.append(y_ext[i])
                    pt.append(z_ext2[0])
                    pts_down.append(pt)
                    
                origin2=[0, y_center_ext, z_ext2[0]] 

                stl_bot=[]
                for i in range(0, len(pts_down)):
                    f=[]
                    z=i+1
                    f.append(pts_down[i])
                    if z > len(pts_down)-1: 
                        f.append(pts_down[0])
                    else:
                        f.append(pts_down[z])
                    f.append(origin2)
                    stl_bot.append(f)

                vertices = np.asarray([stl_top])
                vertices.resize((len(stl_top),3,3))
                vertices1 = np.asarray([stl_bot])
                vertices1.resize((len(stl_bot),3,3))

                pts_side=[]
                stl_side=[]

                for i in range(len(stl_top)):
                    fa=[]
                    fb=[]
                    fa.append(stl_top[i][0])    
                    if i == len(stl_top)-1:
                            fa.append(stl_bot[0][0])
                    else:
                        fa.append(stl_bot[i+1][0])
                    fa.append(stl_bot[i][0])
                    
                    fb.append(stl_top[i][0])
                    if i == len(stl_top)-1:
                        fb.append(stl_top[0][0])
                        fb.append(stl_bot[0][0])
                                
                    else:
                        fb.append(stl_top[i+1][0])
                        fb.append(stl_bot[i+1][0])
                        
                    stl_side.append(fa)
                    stl_side.append(fb)     
                vertice2=np.asarray(stl_side)
                tot_len=vertices.shape[0]+vertices1.shape[0]+vertice2.shape[0]
                vertex=np.zeros(tot_len)
                vertex.resize((tot_len,3 ,3))

                for i, f in enumerate(vertices): 
                    vertex[i]=f
                for i in range(len(vertices), len(vertices)+len(vertices1)):
                    vertex[i]=vertices1[i-len(vertices)]
                for i in range((len(vertices)+len(vertices1)),tot_len):
                    vertex[i]=vertice2[i-(len(vertices)+len(vertices1))]

                couch_ext = mesh.Mesh(np.zeros(tot_len, dtype=mesh.Mesh.dtype))
                for i, f in enumerate(vertex):
                    couch_ext.vectors[i]=f
                couch_ext.save(root+'/temp/couch_ext.stl')



                # compute STL file for Interior couch
                # get x y and z off courch interior values from dicom rt struct
                for i in range(0, len(rs.ROIContourSequence[ind_int].ContourSequence[0].ContourData), 3):
                    x_int.append(float(rs.ROIContourSequence[ind_int].ContourSequence[0].ContourData[i]))
                for i in range(1, len(rs.ROIContourSequence[ind_int].ContourSequence[0].ContourData), 3):
                    y_int.append(float(rs.ROIContourSequence[ind_int].ContourSequence[0].ContourData[i]))
                for i in range(2, len(rs.ROIContourSequence[ind_int].ContourSequence[0].ContourData), 3):
                    z_int.append(float(rs.ROIContourSequence[ind_int].ContourSequence[0].ContourData[i]))
                for i in range(2, len(rs.ROIContourSequence[ind_int].ContourSequence[-1].ContourData), 3):
                    z_int2.append(float(rs.ROIContourSequence[ind_int].ContourSequence[-1].ContourData[i]))

                y_center_int = min(y_int)+((max(y_int)-min(y_int))/2)
                pts_up_int=[]

                for i in range(len(x_int)):
                    pt=[]
                    pt.append(x_int[i])
                    pt.append(y_int[i])
                    pt.append(z_int[0])
                    pts_up_int.append(pt)
                
                origin1_int=[0, y_center_int, z_int[0]]

                stl_top_int=[]
                for i in range(0, len(pts_up_int)):
                    f=[]
                    z=i+1 
                    if z > len(pts_up_int)-1: 
                        f.append(pts_up_int[0])
                    else:
                        f.append(pts_up_int[z])
                    f.append(pts_up_int[i])
                    f.append(origin1_int)
                    stl_top_int.append(f)

                pts_down_int=[]
                for i in range(len(x_int)):
                    pt=[]
                    pt.append(x_int[i])
                    pt.append(y_int[i])
                    pt.append(z_int2[0])
                    pts_down_int.append(pt)
                    
                origin2_int=[0, y_center_int, z_int2[0]] 

                stl_bot_int=[]
                for i in range(0, len(pts_down_int)):
                    f=[]
                    z=i+1
                    f.append(pts_down_int[i])
                    if z > len(pts_down_int)-1: 
                        f.append(pts_down_int[0])
                    else:
                        f.append(pts_down_int[z])
                    f.append(origin2_int)
                    stl_bot_int.append(f)

                vertices_int = np.asarray([stl_top_int])
                vertices_int.resize((len(stl_top_int),3,3))
                vertices1_int = np.asarray([stl_bot_int])
                vertices1_int.resize((len(stl_bot_int),3,3))

                pts_side_int=[]
                stl_side_int=[]

                for i in range(len(stl_top_int)):
                    fa=[]
                    fb=[]
                    fa.append(stl_top_int[i][0])    
                    if i == len(stl_top_int)-1:
                            fa.append(stl_bot_int[0][0])
                    else:
                        fa.append(stl_bot_int[i+1][0])
                    fa.append(stl_bot_int[i][0])
                    
                    fb.append(stl_top_int[i][0])
                    if i == len(stl_top_int)-1:
                        fb.append(stl_top_int[0][0])
                        fb.append(stl_bot_int[0][0])
                                
                    else:
                        fb.append(stl_top_int[i+1][0])
                        fb.append(stl_bot_int[i+1][0])
                        
                    stl_side_int.append(fa)
                    stl_side_int.append(fb)

                vertice2_int=np.asarray(stl_side_int)
                tot_len_int=vertices_int.shape[0]+vertices1_int.shape[0]+vertice2_int.shape[0]
                vertex_int=np.zeros(tot_len_int)
                vertex_int.resize((tot_len_int,3 ,3))

                for i, f in enumerate(vertices_int): 
                    vertex_int[i]=f
                for i in range(len(vertices_int), len(vertices_int)+len(vertices1_int)):
                    vertex_int[i]=vertices1_int[i-len(vertices_int)]
                for i in range((len(vertices_int)+len(vertices1_int)),tot_len_int):
                    vertex_int[i]=vertice2_int[i-(len(vertices_int)+len(vertices1_int))]

                couch_int = mesh.Mesh(np.zeros(tot_len_int, dtype=mesh.Mesh.dtype))
                for i, f in enumerate(vertex_int):
                    couch_int.vectors[i]=f
                couch_int.save(root+'/temp/couch_int.stl')
                self._set_couch(True)

        except IndexError:
            self._set_couch(False)
            print("")
            print("  !!! WARNING !!! ")
            print("         No RT struct file found: couch is not modeled")
            print("")       



    def _get_couch(self):
        return(self.Couch)

    def _set_couch(self, a):
        self.Couch = a



# + Number of part (IAEA Varian PHSP) # To Do TO CHECK !!!! different for stat and dyn

# + Number of part (IAEA Varian PHSP)
    def _get_nb_part_tot_varian(self):
        """
        Get the number of particle used for the simulation 
        """
        root = os.getcwd()

        #with open()

        data_phsp=pd.read_csv(root+'/utils/source/data_varian_phsp.csv')
        #print(data_phsp)
        if self._get_split_type() == 'stat':
            total_number_of_primaries=0
            total_number_of_primaries_to_simulate=data_phsp['total_nb_part_energy'].loc[data_phsp['energy'] == self._get_energy()].to_numpy()[0]
            number_of_phsp_file=data_phsp['index'].loc[data_phsp['energy']==self._get_energy()].to_numpy()[-1]
            #print(data_phsp['index'].loc[data_phsp['energy']==self._get_energy()])
        
            for cpi in range(0, self._get_beam_nb_cpi()):
                i = cpi % (number_of_phsp_file+1)
                
                if self._get_nb_index() <= number_of_phsp_file:
                    number_of_primaries = int(data_phsp['nb_part_phsp'].loc[data_phsp['energy']==self._get_energy()].to_numpy()[i]*self._get_dose_rate()[cpi])
                    #print(number_of_primaries)
                if self._get_nb_index() > number_of_phsp_file:
                    number_of_primaries=int(int(total_number_of_primaries/self._get_nb_index())*self._get_dose_rate()[cpi])
                    #print(number_of_primaries)

                total_number_of_primaries = total_number_of_primaries + number_of_primaries

            a=round((total_number_of_primaries/total_number_of_primaries_to_simulate)*100, 2)


        
        if self._get_split_type() == 'dyn':
            total_number_of_primaries=0
            total_number_of_primaries_phsp=data_phsp['total_nb_part_energy'].loc[data_phsp['energy'] == self._get_energy()].to_numpy()[0]
            #print('total to simulate : ', total_number_of_primaries_phsp*self._get_recycling())
            number_of_phsp_file=data_phsp['index'].loc[data_phsp['energy']==self._get_energy()].to_numpy()[-1]
            primaries_per_simu=total_number_of_primaries_phsp/self._get_nb_index()
            #print('per simu : ', primaries_per_simu)

            for cpi in range(0,self._get_beam_nb_cpi()):
                i = cpi % (number_of_phsp_file+1)
                number_of_primaries=int(int(primaries_per_simu/self._get_beam_nb_cpi())*self._get_dose_rate()[cpi])
                total_number_of_primaries = total_number_of_primaries + number_of_primaries
            
            
            total_number_of_primaries = total_number_of_primaries * self._get_nb_index()
            a=round((total_number_of_primaries/total_number_of_primaries_phsp)*100, 2)
            #print(a)
                    
        return(total_number_of_primaries, a)

