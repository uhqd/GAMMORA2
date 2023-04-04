import os
import glob
import pydicom as dcm
import numpy as np
import pandas as pd
import Gammora_beam
import Gammora_print
import Gammora_generator

root = os.getcwd()

global UtilsMac
global UtilsPlacements
global UtilsMacActor
global UtilsMacPhantom
global config_default_scratch
global UtilsMLC
UtilsPlacements=root+'/utils/placement_template/'
UtilsMac=root+'/utils/mac/mac_template/'
UtilsMLC=root+'/utils/mlc/'
UtilsMacActor=root+'/utils/mac/actor/'
UtilsMacPhantom=root+'/utils/mac/phantom/'
config_default_scratch = {}

class GammoraManualBeam(Gammora_beam.GammoraBeam):

#==========================================================================================

# Initialisation

    def __init__(self, config, GammoraStudy):

# Default Config:

        # Default settings:
        #config['SIMU_NAME']=simu_name
        config_default_scratch['VISU']=False
        config_default_scratch['SIMU_NAME'] = 'test'
        config_default_scratch['VISU_MODE']=0
        config_default_scratch['PHYSICS']=True
        config_default_scratch['PHYSICS_NAME']='Xphysics.macX'
        config_default_scratch['HEAD_SIMULATION']=True
        config_default_scratch['PATIENT_SIMULATION']=True
        config_default_scratch['TEST_SIMULATION']=False # not working yet
        config_default_scratch['SPLIT_TYPE']='stat'
        config_default_scratch['INDEX']=1
        config_default_scratch['GANTRY']=0
        config_default_scratch['GANTRY_STOP']='X'
        config_default_scratch['DELTA_DEGREE'] = 0.5  # step in degree between each in gantry angle for manual arc therapy
        config_default_scratch['COLLI']=0.0
        config_default_scratch['X1']=50.0
        config_default_scratch['X2']=50.0
        config_default_scratch['Y1']=50.0
        config_default_scratch['Y2']=50.0
        config_default_scratch['MLC']=True
        config_default_scratch['MLC_FILE']=True
        config_default_scratch['PHSP_ACTOR']=True
        config_default_scratch['PATIENT_ACTOR']=True
        config_default_scratch['PHSP_ACTOR_FILE']='root_make_phspR_cyl.mac'
        config_default_scratch['PATIENT_ACTOR_FILE']='dose_actor.mac'
        config_default_scratch['PATIENT_ACTOR_SIZE']=[300.0, 300.0, 300.0]
        config_default_scratch['PATIENT_ACTOR_RESOLUTION']=[300, 300, 300]
        config_default_scratch['PATIENT_CT']=True
        config_default_scratch['PHANTOM']=False
        config_default_scratch['PHANTOM_FILE']='waterbox300.mac'
        config_default_scratch['SOURCE']=True
        config_default_scratch['ENERGY']='6X'
        config_default_scratch['SOURCE_GAGA']=False
        config_default_scratch['SOURCE_IAEA']=True
        config_default_scratch['NB_PART']=1000000000
        config_default_scratch['RECYCLING']=100

        config_default_scratch['CALMIP_USER']='leste'
        config_default_scratch['AUTO_SENDING']=False
        config_default_scratch['AUTO_LAUNCHING']=False
        


# General settings

# + Simu Name        
        
        if config['SIMU_NAME'] == 'auto':  
            self._set_beam_name(GammoraStudy._get_study_name())
        else:
            self._set_beam_name(config['SIMU_NAME'])
        #self._set_beam_name(GammoraStudy._get_study_name())


        Gammora_print._title("Creating GAMMORA Beam object for study : "+ GammoraStudy._get_study_name())
        Gammora_print._title2("Simulation Name : " + self._get_beam_name())
        Gammora_print._separator2()
        Gammora_print._title("General : ")
        

# Path
        self._set_local_output_dir(root+'/output/'+self._get_beam_name())


# + Material
        self._set_material(True)
        self._set_material_name('TBMaterials.tb')

        Gammora_print._title2("Material Table : " + str(self._get_material()))
        Gammora_print._title2("Material Table Name : " + str(self._get_material_name()))

# + Visualization        

        if config['VISU'] == 'auto':
            self._set_visualization(config_default_scratch['VISU'])
            Gammora_print._title2("Visualisation : "+ str(bool(self._get_visualization())))
            if self._get_visualization() == True:
                self._set_visualization_mode(config_default_scratch['VISU_MODE'])
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

# + Physics

        if config['PHYSICS'] == 'auto':
            self._set_physics(config_default_scratch['PHYSICS'])
            Gammora_print._title2("Physics : "+ str(bool(self._get_physics())))
            if self._get_physics() == True:
                self._set_physics_name(UtilsMac+config_default_scratch['PHYSICS_NAME'])
                #Gammora_print._title2("Physics file name :"+config_default_scratch['PHYSICS_NAME'])
        elif config['PHYSICS'] == '0':
            self._set_physics(bool(int(config['PHYSICS'])))
            Gammora_print._title2("Physics :    "+str(bool(self._get_physics())))
        elif config['PHYSICS'] == '1':
            self._set_physics(bool(int(config['PHYSICS'])))
            self._set_physics_name(UtilsMac+config_default_scratch['PHYSICS_NAME'])
            Gammora_print._title2("Physics : "+str(bool(self._get_physics())))
            Gammora_print._title2("Physics file name : "+str(bool(self._get_physics_name())))
        else:
            self._set_physics(bool((config['PHYSICS'])))
            self._set_physics_name(UtilsMac+(config['PHYSICS']))
            Gammora_print._title2("Physics : "+ str(bool(self._get_physics())))
            Gammora_print._title2("Physics file name : "+str(config['PHYSICS']))

# + Head part simulation

        if config['HEAD_SIMULATION'] == 'auto':
            self._set_head_part_siumulation(config_default_scratch['HEAD_SIMULATION'])
            Gammora_print._title2("Head Simulation : " + str(bool(self._get_head_part_siumulation())))
        elif config['HEAD_SIMULATION'] == '0':
            self._set_head_part_siumulation(bool(int(config['HEAD_SIMULATION'])))
            Gammora_print._title2("Head Simulation : " + str(bool(self._get_head_part_siumulation())))
        elif config['HEAD_SIMULATION'] == '1':
            self._set_head_part_siumulation(bool(int(config['HEAD_SIMULATION'])))
            Gammora_print._title2("Head Simulation : " + str(bool(self._get_head_part_siumulation())))
                
# + Patient part simulation
                
        if config['PATIENT_SIMULATION'] == 'auto':
            self._set_patient_part_siumulation(config_default_scratch['PATIENT_SIMULATION'])
            Gammora_print._title2("Patient Simulation : " + str(bool(self._get_patient_part_siumulation())))
        elif config['PATIENT_SIMULATION'] == '0':
            self._set_patient_part_siumulation(bool(int(config['PATIENT_SIMULATION'])))
            Gammora_print._title2("Patient Simulation : " + str(bool(self._get_patient_part_siumulation())))
        elif config['PATIENT_SIMULATION'] == '1':
            self._set_patient_part_siumulation(bool(int(config['PATIENT_SIMULATION'])))
            Gammora_print._title2("Patient Simulation : " + str(bool(self._get_patient_part_siumulation())))

# + Test simulation in local

        # To do **
        if config['TEST_SIMULATION'] == 'auto':
           #self._set_test_siumulation(config_default_scratch['TEST_SIMULATION'])
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
        

# + Split type

        if config['SPLIT_TYPE'] == 'stat':
            self._set_split_type('stat')
        elif config['SPLIT_TYPE'] == 'dyn':
                self._set_split_type('dyn')
        if config['SPLIT_TYPE'] == 'auto':
            self._set_split_type(config_default_scratch['SPLIT_TYPE'])
        Gammora_print._title2("Split Type : "+str(self._get_split_type()))
        
# + Number of index        

        if self._get_head_part_siumulation() != True: # if == True -> number of index depending on gantry angle choice and is then defined after
            if config['INDEX'] == 'auto':
                self._set_nb_index(config_default_scratch['INDEX'])
            else:
                self._set_nb_index(int(config['INDEX']))
            Gammora_print._title2("Number of Index : " + str(self._get_nb_index()))

# Head Part Simulation
# + Geometry HEAD
        Gammora_print._separator2()
        Gammora_print._title("Head Part Simulation Geometry :")

        if self._get_head_part_siumulation() == True:

# ++ Gantry To Do read Gantry from .csv file
            if config['GANTRY'] == 'auto':
                self._set_gantry_angle_start(float(config_default_scratch['GANTRY']))
            else:
                self._set_gantry_angle_start(float(config['GANTRY']))

            if config['GANTRY_STOP'] == 'auto' :
                self._set_gantry_angle_stop((config_default_scratch['GANTRY_STOP']))           
            else:
                self._set_gantry_angle_stop((config['GANTRY_STOP']))

# ++ Number of Index (static beam)

            if self._get_gantry_angle_stop() == 'X':
                if config['INDEX'] == 'auto':
                    self._set_nb_index(config_default_scratch['INDEX'])
                    self._set_beam_nb_cpi(self._get_nb_index())
                else:
                    self._set_nb_index(int(config['INDEX']))
                    self._set_beam_nb_cpi(self._get_nb_index())

            if self._get_gantry_angle_stop() == 'X':
                g=np.repeat(self._get_gantry_angle_start(), self._get_nb_index()).tolist()
                self._set_gantry_angle(g)
                Gammora_print._title2("Static Gantry position")
                Gammora_print._title2("Gantry Angle : "+ str(self._get_gantry_angle()[0])+ "°")
             
            else:                
                g=np.arange(self._get_gantry_angle_start(), float(self._get_gantry_angle_stop())+config_default_scratch['DELTA_DEGREE'], config_default_scratch['DELTA_DEGREE']).tolist()
                self._set_gantry_angle(g)
                #print(len(g))
                self._set_beam_nb_cpi(len(g))
                Gammora_print._title2("Arc Thearpy")
                Gammora_print._title2("Gantry Angle Start : "+ str(self._get_gantry_angle()[0])+ "°")
                Gammora_print._title2("Gantry Angle Stop : "+ str(self._get_gantry_angle()[-1])+ "°")

# + Number of index (if arc therapy)    

            if self._get_split_type() == 'dyn':
                if config['INDEX'] == 'auto':
                    self._set_nb_index(config_default_scratch['INDEX'])
                else:
                    self._set_nb_index(int(config['INDEX']))
            if self._get_split_type() == 'stat':
                self._set_nb_index(len(g))
              
# + Numbre of index print
            Gammora_print._title2("Number of Index : " + str(self._get_nb_index())) 
            
# ++ Colli

            if config['COLLI'] == 'auto': 
                colli=np.repeat(float(config_default_scratch['COLLI']), self._get_nb_index()).tolist()
                self._set_colli_angle(colli)                         
            else:
                colli=np.repeat(float(config['COLLI']), self._get_nb_index()).tolist()
                self._set_colli_angle(colli)
            
            Gammora_print._title2("Colli Angle : " + str(self._get_colli_angle()[0])+ "°")
# ++ Jaws
# +++ X1
            if config['X1'] == 'auto':
                if self._get_split_type() == 'stat': 
                    x1=np.repeat(float(config_default_scratch['X1']), self._get_nb_index()).tolist()
                    self._set_x1(x1)
                if self._get_split_type() == 'dyn':
                    x1=np.repeat(float(config_default_scratch['X1']), self._get_beam_nb_cpi()).tolist()
                    self._set_x1(x1)

            else:
                if self._get_split_type() == 'stat':
                    x1=np.repeat(float(config['X1']), self._get_nb_index()).tolist()
                    self._set_x1(x1)
                if self._get_split_type() == 'dyn':
                    x1=np.repeat(float(config['X1']), self._get_beam_nb_cpi()).tolist()
                    self._set_x1(x1)
            
            Gammora_print._title2("X1 Position : " + str(self._get_x1()[0]) + " mm")
# +++ X2           
            if config['X2'] == 'auto': 
                if self._get_split_type() == 'stat':
                    x2=np.repeat(float(config_default_scratch['X2']), self._get_nb_index()).tolist()
                    self._set_x2(x2)  
                if self._get_split_type() == 'dyn':
                    x2=np.repeat(float(config_default_scratch['X2']), self._get_beam_nb_cpi()).tolist()
                    self._set_x2(x2)  
                                       
            else:
                if self._get_split_type() == 'stat':
                    x2=np.repeat(float(config['X2']), self._get_nb_index()).tolist()
                    self._set_x2(x2)
                if self._get_split_type() == 'dyn':
                    x2=np.repeat(float(config['X2']), self._get_nb_index()).tolist()
                    self._set_x2(x2)
            
            Gammora_print._title2("X2 Position : "+ str(self._get_x2()[0])+ " mm")
# +++ Y1           
            if config['Y1'] == 'auto': 
                if self._get_split_type() == 'stat':
                    y1=np.repeat(float(config_default_scratch['Y1']), self._get_nb_index()).tolist()
                    self._set_y1(y1)  
                if self._get_split_type() == 'dyn':
                    y1=np.repeat(float(config_default_scratch['Y1']), self._get_beam_nb_cpi()).tolist()
                    self._set_y1(y1)                         
            else:
                if self._get_split_type() == 'stat':
                    y1=np.repeat(float(config['Y1']), self._get_nb_index()).tolist()
                    self._set_y1(y1)
                if self._get_split_type() == 'dyn':
                    y1=np.repeat(float(config['Y1']), self._get_beam_nb_cpi()).tolist()
                    self._set_y1(y1)
            
            Gammora_print._title2("Y1 Position : "+ str(self._get_y1()[0])+ " mm")
# +++ Y2        
            if config['Y2'] == 'auto': 
                if self._get_split_type() == 'stat':
                    y2=np.repeat(float(config_default_scratch['Y2']), self._get_nb_index()).tolist()
                    self._set_y2(y2)
                if self._get_split_type() == 'dyn':
                    y2=np.repeat(float(config_default_scratch['Y2']), self._get_beam_nb_cpi()).tolist()
                    self._set_y2(y2)

            else:
                if self._get_split_type() == 'stat':
                    y2=np.repeat(float(config['Y2']), self._get_nb_index()).tolist()
                    self._set_y2(y2)
                if self._get_split_type() == 'dyn':
                    y2=np.repeat(float(config['Y2']), self._get_beam_nb_cpi()).tolist()
                    self._set_y2(y2)
            
            Gammora_print._title2("Y2 Position : " + str(self._get_y2()[0])+ " mm")

# ++ MLC
            if config['MLC'] == 'auto':
                self._set_mlc(config_default_scratch['MLC'])
            elif config['MLC'] == '0':
                self._set_mlc(bool(int(config['MLC'])))
            elif config['MLC'] == '1':
                self._set_mlc(bool(int(config['MLC'])))
            Gammora_print._title2("MLC : " + str(self._get_mlc()))

            if self._get_mlc() == True:
                if config['MLC_FILE'] == 'auto':
                    mlc=self._read_mlc_file(config_default_scratch['MLC_FILE'])
                else:
                    mlc=self._read_mlc_file(config['MLC_FILE'])
                
                self._set_mlc_sequence(mlc)

                if self._get_split_type() == 'dyn':
                    self._create_mlc_file()

                # To Do check this functiun works fine
                if self._get_split_type() == 'stat':
                    if len(self._get_mlc_sequence()) < self._get_nb_index():
                        self._interp_geometry()
                    self._create_mlc_file()

# ++ Dose Rate
            self._set_dose_rate(np.ones(self._get_beam_nb_cpi()).tolist())  # constant Dose Rate    
# + Source
            Gammora_print._separator2()
            Gammora_print._title("Source (Head Part Simulation) :") 

            if config['SOURCE'] == 'auto':
                self._set_source(config_default_scratch['SOURCE'])
                Gammora_print._title2("Source : "+ str(self._get_source()))
            elif config['SOURCE'] == '0':
                self._set_source(bool(int(config['SOURCE'])))
                Gammora_print._title2("Source : " + str(self._get_source()))
            else:  # iaea or gaga
                self._set_source(True)
                Gammora_print._title2("Source : "+  str(self._get_source()))
# + Source Type            
            if self._get_source() == True:
                if config['SOURCE'] == 'gaga':
                    self._set_source_iaea(False)
                    self._set_source_gaga(True)
                    self._set_source_root(False) #not working
                    self._set_source_gps(False) #not working
                    Gammora_print._title2("Source Type : GAGA")
                elif config['SOURCE'] == 'iaea':
                    self._set_source_iaea(True)
                    self._set_source_gaga(False)
                    self._set_source_root(False) #not working
                    self._set_source_gps(False) #not working
                    Gammora_print._title2("Source Type : IAEA")
                else: # if auto
                    self._set_source_iaea(config_default_scratch['SOURCE_IAEA'])
                    self._set_source_gaga(config_default_scratch['SOURCE_GAGA'])
                    if self._get_source_gaga() == True :
                        Gammora_print._title2("Source Type : GAGA")
                    elif self._get_source_iaea() == True :
                        Gammora_print._title2("Source Type : IAEA")
                    else:
                        Gammora_print._warning("No source type in set in default Config", ["Set a source type by default"])
                    #self._set_source_root(config_default_scratch['SOURCE_IAEA']) #not working
                    #self._set_source_gps(config_default_scratch['SOURCE_IAEA']) #not workin
                
# + Energy
            if self._get_source() == True:
                if config['ENERGY'] == 'auto':
                    self._set_energy(config_default_scratch['ENERGY'])
                else:
                    self._set_energy(config['ENERGY'])

                Gammora_print._title2("Energy : " + self._get_energy())

# Recycling
                if self._get_patient_part_siumulation() == True:
                    if config['RECYCLING'] == 'auto':
                        self._set_recycling(config_default_scratch['RECYCLING'])
                    else:
                        self._set_recycling(int(config['RECYCLING']))
                    #print('*Recycling of reducued phase space for Patient simulation:     ', self._get_recycling())

# + Number of particle
                if config['NB_PART'] != 'auto' and self._get_source_iaea() ==True:
                    self._set_iaea_nb_part(int(config['NB_PART']))
                    self._set_manual_nb_part(True)
                    Gammora_print._title2("Number of particle (including recycling seeting) : "+str(self._get_iaea_nb_part()))
                    #Gammora_print._title2('Number of particle (including recycling seeting) :')
                    #Gammora_print._warning('When using IAEA PHSP number of particle is set automatically', ['Number of particle set to '+str(self._get_nb_part_tot_varian()[0]*self._get_recycling()), str(self._get_nb_part_tot_varian()[1])+" % Varian PHSP used"])   
                                
                if config['NB_PART'] == 'auto' and self._get_source_iaea() ==True:
                    self._set_manual_nb_part(False)  
                    Gammora_print._title2("Number of particle (including recycling seeting) : "+str(self._get_nb_part_tot_varian()[0]*self._get_recycling()) + " ("+str(self._get_nb_part_tot_varian()[1])+" % Varian PHSP used)")
                                       
                elif config['NB_PART'] == 'auto' and self._get_source_gaga() == True:
                    self._set_manual_nb_part(False)  
                    self._set_gaga_nb_part(config_default_scratch['NB_PART'])

                    Gammora_print._title2("Number of particle (including recycling seeting) : "+str(config_default_scratch['NB_PART']))
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
        Gammora_print._title("Patient Part Simulation Geometry :")

        if self._get_patient_part_siumulation() == True:


# Phantom and Patient CT

            if config['PHANTOM'] == 'auto':
                self._set_phantom(config_default_scratch['PHANTOM'])
                self._set_patient_ct(config_default_scratch['PATIENT_CT'])

                if self._get_phantom() == True:
                    self._set_phantom_name(UtilsMacPhantom+config_default_scratch['PHANTOM_FILE'])

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
            
            #if self._get_patient_ct() == True:
            #    self._set_patient_ct_name(root+'/input/patient/'+GammoraStudy._get_study_input_name()+'/dicom/ct')
            #    self._set_isocenter_position(beam._get_isocenter())
            #    self._set_patient_orientation(1)
            #    self._create_stl_couch(patient)

            Gammora_print._title2("Simulation On Phantom : " + str(self._get_phantom()))
            Gammora_print._title2("Simulation On Patient CT : " + str(self._get_patient_ct()))

            if self._get_phantom() == True:
                Gammora_print._title2("Phantom file : " + config['PHANTOM'])
                Gammora_print._title2("Phantom Motion : Not yet possible")
            #if self._get_patient_ct() == True:
            #    Gammora_print._title2("Dicom CT of patient : " + self._get_study_input_name())


# No Patient Part Simulation

        else:
            Gammora_print._title2("Patient Part Simulation is disabled !")

# Actor Difinition
        Gammora_print._separator2()
        Gammora_print._title('Actor Definition')

        if self._get_head_part_siumulation() == True:

# + PHSP Actor
            if config['PHSP_ACTOR'] == 'auto':
                self._set_phsp_actor(config_default_scratch['PHSP_ACTOR'])
                if self._get_phsp_actor() == True:
                    self._set_phsp_actor_name(UtilsMacActor+config_default_scratch['PHSP_ACTOR_FILE'])
            
            elif config['PHSP_ACTOR'] == '0':
                self._set_phsp_actor(bool(int(config['PHSP_ACTOR'])))

            elif config['PHSP_ACTOR'] == '1':
                self._set_phsp_actor(bool(int(config['PHSP_ACTOR'])))
                self._set_phsp_actor_name(UtilsMacActor+config_default_scratch['PHSP_ACTOR_FILE'])
            else:
                self._set_phsp_actor(True)
                self._set_phsp_actor_name(UtilsMacActor+config['PHSP_ACTOR'])

            if self._get_phsp_actor() == True:
                Gammora_print._title2("Phase space actor : " + str(self._get_phsp_actor()))
                if config['PHSP_ACTOR'] == 'auto' or config['PHSP_ACTOR'] == '1':
                    Gammora_print._title2("Phase space actor file : " + config_default_scratch['PHSP_ACTOR_FILE'])
                else:
                    Gammora_print._title2("Phase space actor file : " + config['PHSP_ACTOR'])
            else:
                Gammora_print._title2("Phase space actor : " + str(self._get_phsp_actor()))
            


# + Patient Actor
            
        if self._get_patient_part_siumulation() == True:
            if config['PATIENT_ACTOR'] == 'auto':
                self._set_patient_actor(config_default_scratch['PATIENT_ACTOR'])
                if self._get_patient_actor() == True:
                    self._set_patient_actor_name(UtilsMacActor+config_default_scratch['PATIENT_ACTOR_FILE'])
            
            elif config['PATIENT_ACTOR'] == '0':
                self._set_patient_actor(bool(int(config['PATIENT_ACTOR'])))

            elif config['PATIENT_ACTOR'] == '1':
                self._set_patient_actor(bool(int(config['PATIENT_ACTOR'])))
                self._set_patient_actor_name(UtilsMacActor+config_default_scratch['PATIENT_ACTOR_FILE'])
            else:
                self._set_patient_actor(True)
                self._set_patient_actor_name(UtilsMacActor+config['PATIENT_ACTOR'])

            if self._get_patient_actor() == True:
                Gammora_print._title2("Patient actor : " + str(self._get_patient_actor()))
                if config['PATIENT_ACTOR'] == 'auto' or config['PATIENT_ACTOR'] == '1':
                    Gammora_print._title2("Patient actor file : "+ config_default_scratch['PATIENT_ACTOR_FILE'])
                else:
                    Gammora_print._title2("Phase space actor file : " + config['PATIENT_ACTOR'])
            else:
               Gammora_print._title2("Patient actor : "+ self._get_patient_actor())

# + Patient Actor Size         
            if self._get_patient_actor() == True:
                if config['PATIENT_ACTOR'].endswith('.mac') and config['PATIENT_ACTOR'] != 'dose_actor.mac':
                    Gammora_print._title2("Patient actor size defined in : " + str(config['PATIENT_ACTOR']))
                    Gammora_print._title2("Patient actor size defined in : " + str(config['PATIENT_ACTOR']))
                else:
                    if config['PATIENT_ACTOR_SIZE'] == 'auto':
                        self._set_patient_actor_size([float(val) for val in list(config_default_scratch['PATIENT_ACTOR_SIZE'])])
                        Gammora_print._title2("Patient actor size (from Dicom RT dose) : " + str(self._get_patient_actor_size()) + " (x,y,z)")

                    else:
                        self._set_patient_actor_size([float(val) for val in list(config['PATIENT_ACTOR_SIZE'].split())])
                        Gammora_print._title2("Patient actor size (x,y,z) : " + str(self._get_patient_actor_size()))
      

# + Patient Actor Resolution                  
                    if config['PATIENT_ACTOR_RESOLUTION'] == 'auto':
                        self._set_patient_actor_resolution([int(val) for val in list(config_default_scratch['PATIENT_ACTOR_RESOLUTION'])])
                        Gammora_print._title2("Patient actor resolution (from Dicom RT dose) : " + str(self._get_patient_actor_resolution())+" (x,y,z)")

                    else:
                        self._set_patient_actor_resolution([int(val) for val in list(config['PATIENT_ACTOR_RESOLUTION'].split())])
                        Gammora_print._title2("Patient actor resolution (from Dicom RT dose) : " + str(self._get_patient_actor_resolution()))
                    
                    Gammora_print._title2("Patient actor size : " + str(self._get_patient_actor_size()) + " (x,y,z)")
                    Gammora_print._title2("Patient actor resolution : " + str(self._get_patient_actor_resolution()) + " (x,y,z)")

# Add a GAMMORA Manual simu object to GAMMORA Manual Beam object 

        self.Simu = Gammora_generator.GammoraPatientSimu(config, self, GammoraStudy)

        # Computing
#        print('* Computing')
#        if config['EXECUTE_ON_CLUSTER'] == '0':
#            self._set_calmip(False)
#            self._set_apple_cluster(False)
#            self._set_local(True)
#            print(' * Local simulation')
#        if config['EXECUTE_ON_CLUSTER'] == '3':
#            self._set_calmip(True)
#            self._set_apple_cluster(False)
#            self._set_local(False)
#            print(' * CALMIP simulation')

#        if self._get_calmip() == True:
#            self._set_user(config_default_scratch['CALMIP_USER'])
#            self._set_sending(config_default_scratch['AUTO_SENDING'])
#            self._set_launching(config_default_scratch['AUTO_LAUNCHING'])
#            self._set_input_dir('/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name())
#            self._set_output_dir('/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/output')
#            self._set_phsp_dir1('/tmpdir/'+self._get_user()+'/phsp')
#            print('* CALMIP user: ', self._get_user())
            
#        if self._get_local() == True:
#            self._set_input_dir(self._get_local_output_dir())
        
#        print()
#        print("                 -----           ")
#        print()
       

    def _interp_geometry(self):
         
        old_mlc=self._get_mlc_sequence()
        
        old_index=np.arange(0, len(old_mlc))

        if len(old_index) == 1:    
            new_mlc=[]
            for i in range(0, self._get_nb_index()):
                new_mlc.append(old_mlc[0])

        if len(old_index) > 1:
            new_index=np.linspace(old_index.min(), old_index.max(), self._get_nb_index())        
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
            
        self._set_mlc_sequence(new_mlc)


    def  _get_size_from_rt_dose(self, patient):
        root = os.getcwd()
        try:
            rt_dose_file=glob.glob(root+"/input/patient/"+patient._get_patient_id()+"/dicom/RD*")[0]
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
            size = config_default_scratch['PATIENT_ACTOR_SIZE']
            print("")
            print("  !!! WARNING !!! ")
            print("         No RT Dose file found: Actor Size is defined to default value", config_default_scratch['PATIENT_ACTOR_SIZE'])
            print("")
            

        return(size)

    def  _get_resolution_from_rt_dose(self, patient):
        root = os.getcwd()
        try:
            rt_dose_file=glob.glob(root+"/input/patient/"+patient._get_patient_id()+"/dicom/RD*")[0]
            rt_dose=dcm.read_file(rt_dose_file)
            rt_dose_array=rt_dose.pixel_array
            rt_dose=dcm.read_file(rt_dose_file)
            rt_dose_array=rt_dose.pixel_array
            shape=[rt_dose_array.shape[2], rt_dose_array.shape[1], rt_dose_array.shape[0]]
        except IndexError:
            shape = config_default_scratch['PATIENT_ACTOR_RESOLUTION']
            print("")
            print("  !!! WARNING !!! ")
            print("         No RT Dose file found: Actor Resolution is defined to default value: ", config_default_scratch['PATIENT_ACTOR_RESOLUTION'])
            print("")
            

        return(shape)

    def _create_stl_couch(self, patient):
        root = os.getcwd()
        try:
            rt_struct_file=glob.glob(root+"/input/patient/"+patient._get_patient_id()+"/dicom/RS*")[0]
            rs=dcm.read_file(rt_struct_file)

            #looking for couch structure in dicom rt struct
            i=0
            for st in rs.StructureSetROISequence:
                if st.ROIName == "CouchSurface":
                    ind_ext = i
                if st.ROIName == "CouchInterior":
                    ind_int = i
                i = i+1
            
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
    
    def _add_stl_couch(self, mac_directory, data_directory, exec_dir):
        root = os.getcwd()
        shutil.copyfile(root+'/temp/couch_int.stl',data_directory+'/couch_int.stl')
        shutil.copyfile(root+'/temp/couch_ext.stl',data_directory+'/couch_ext.stl')
        shutil.copyfile(UtilsMac+'Xcouch.macX',data_directory+'/couch.mac')

        with open(mac_directory+'/main.mac', 'a') as file:
            c='/control/execute '+exec_dir+'/couch.mac'
            file.write(c+"\n")

        file=fileinput.FileInput(data_directory+'/couch.mac', inplace=1)
        for line in file:
            line=line.replace("x_shift", str(self._get_isocenter_position()[0]*-1))
            line=line.replace("y_shift", str(self._get_isocenter_position()[1]*-1))
            line=line.replace("z_shift", str(self._get_isocenter_position()[2]*-1))
            print(line)


    def _get_couch(self):
        return(self.Couch)
    
    def _set_couch(self, a):
        self.Couch = a

    def _read_mlc_file(self, mlc_file_name):
            mlc=[]
            with open(UtilsMLC+mlc_file_name, "r") as f:
                a=f.readlines()
            i=0
            mlc=[]
            for line in a:
                #print(line)
                #if 'Number of Fields =' in line:
                    #index=int(line.split(' ')[-1])
                if 'Leaf 1A =' in line or 'Leaf  1A =' in line:
                    mlc.append([])
                if 'Leaf' in line:
                    pos_leaf=float(line.split(' ')[-1])
                    mlc[i].append(pos_leaf)
                if 'Leaf 60B =' in line:
                    i = i+1
            mlc = mlc
            return(mlc)

    #def _compute_mlc_position_fromC(self, file):
    #    root = os.getcwd()
    #    shutil.copyfile(root+'/utils/C/bin/makeMLC', root+'/makeMLC')
    #    proc = subprocess.Popen(["./makeMLC", file])
    #    proc.wait()

    def _create_mlc_file(self):
        root = os.getcwd()
        for cpi in range(0, len(self._get_mlc_sequence())):
            with open(root+ '/temp/'+str(cpi)+'-'+self._get_simu_name()+'_mlc.mlc', 'w') as mlc_file:
                mlc_file.write('File Rev = H ' + '\n')
                mlc_file.write('Treatment = ' + 'DYNAMIC' + '\n')
                mlc_file.write('Last Name = ' + self._get_simu_name() + '\n')
                mlc_file.write('First Name = ' + '\n')
                mlc_file.write('Patient ID = ' + self._get_simu_name() + '\n')
                mlc_file.write('Number of Fields = ' + str(self._get_nb_index()) + '\n')
                mlc_file.write('Model = Varian HD120' + '\n')
                mlc_file.write('Tolerance = 0.00' + '\n')
                mlc_file.write('\n')
                #i=beam.BeamID
                
                mlc_file.write('Field = ' + 'Beam X.'+str(cpi) + '\n')
                mlc_file.write('Index = ' + str(cpi) + '\n')
                mlc_file.write('Carriage Group = 1 ' + '\n')
                mlc_file.write('Operator = ' + '\n')
                mlc_file.write('Collimator = 0.00' + '\n')  
                
                ii=0
                for leafs_ in self._get_mlc_sequence()[cpi]:

                    if ii < 60:
                        #posa=round(((leafs_/10.0)*-1), 4)
                        posa=leafs_
                        mlc_file.write('Leaf ' + str(ii + 1) + 'A = ' + str(posa) + '\n')
                        #listB.append(leafs_)
                        #print('Leaf ' + str(ii + 1) + 'A = ' + str((leafs_/10.0)*-1) + '\n')
                    else:
                        #listA.append(leafs_)
                        posb=leafs_
                        #posb=round((leafs_/10.0), 4)
                        mlc_file.write('Leaf ' + str(ii - 59) + 'B = ' + str(posb) + '\n')
                        #print('Leaf ' + str(ii - 59) + 'B = ' + str(leafs_/10.0) + '\n')                  
                    ii=ii+1                

                mlc_file.write('Note = 0' + '\n')
                mlc_file.write('Shape = 0' + '\n')
                mlc_file.write('Magnification  = 1.00' + '\n' + '\n')            
                
    #            #print(mlc_file_name + ' --> created')    
    #            mlc_file.close()


# + Number of part (IAEA Varian PHSP) # To Do TO CHECK !!!! different for stat and dyn
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
            #print(total_number_of_primaries_to_simulate)
            #print(data_phsp['index'].loc[data_phsp['energy']==self._get_energy()])
        
            for cpi in range(0, self._get_nb_index()):
                i = cpi % (number_of_phsp_file+1)
                
                if self._get_nb_index() <= number_of_phsp_file:
                    number_of_primaries = int(data_phsp['nb_part_phsp'].loc[data_phsp['energy']==self._get_energy()].to_numpy()[i]*self._get_dose_rate()[cpi])
                    #print('nn', data_phsp['nb_part_phsp'].loc[data_phsp['energy']==self._get_energy()].to_numpy()[i])
                    #print(number_of_primaries)

                if self._get_nb_index() > number_of_phsp_file:
                    number_of_primaries=int(int(total_number_of_primaries_to_simulate/self._get_nb_index())*self._get_dose_rate()[cpi])
                    #print(number_of_primaries)

                total_number_of_primaries = total_number_of_primaries + number_of_primaries

            a=round((total_number_of_primaries/total_number_of_primaries_to_simulate)*100, 2)
            
        if self._get_split_type() == 'dyn':
            total_number_of_primaries=0
            total_number_of_primaries_phsp=data_phsp['total_nb_part_energy'].loc[data_phsp['energy'] == self._get_energy()].to_numpy()[0]
            number_of_phsp_file=data_phsp['index'].loc[data_phsp['energy']==self._get_energy()].to_numpy()[-1]
            primaries_per_simu=total_number_of_primaries_phsp/self._get_nb_index()

            for cpi in range(0,self._get_beam_nb_cpi()):
                #print(cpi)
                i = cpi % (number_of_phsp_file+1)
                number_of_primaries=int(int(primaries_per_simu/self._get_beam_nb_cpi())*self._get_dose_rate()[cpi])
                total_number_of_primaries = total_number_of_primaries + number_of_primaries
            
            total_number_of_primaries = total_number_of_primaries * self._get_nb_index()
            a=round((total_number_of_primaries/total_number_of_primaries_phsp)*100, 2)
            
                      
                    
        return(total_number_of_primaries, a)