import os, glob
import shutil
import fileinput
#import myImages
import pickle
import functools
#import beam_simu_generator
#import scratch_simu_generator
import Gammora_print
import Gammora_patient
import Gammora_beam
import Gammora_patient_beam
import Gammora_manual_beam
import Gammora_generator

global root
global Utils
global UtilsMLC
global UtilsImages
global UtilsMac
global UtilsPlacements
global UtilsMacActor
global UtilsMacPhantom


root=os.getcwd()


Utils=root+'/utils/'
UtilsPlacements=root+'/utils/placement_template/'
UtilsMac=root+'/utils/mac/mac_template/'
UtilsMacActor=root+'/utils/mac/actor/'
UtilsMacPhantom=root+'/utils/mac/phantom/'
UtilsMLC=root+'/utils/mlc/'
UtilsImages=root+'/utils/images/'





class GammoraStudy():
    def __init__(self, config_file, study_type, study_name):

        Gammora_print._gammora_ascii()


# Patient Mode
        if study_type == 'patient':

            # check if the patient exist
            if os.path.isdir(root+"/input/patient/"+study_name)== True:         
                
                # define gammora study type
                self._set_from_patient(True)

                Gammora_print._title("Simulation From Patient Data")
                Gammora_print._title("Patient: "+study_name+" found")
                
                # list RT plan for patient
                list_rt_plan = glob.glob(root+"/input/patient/"+study_name+"/dicom/RP*")
     
                #create a images directory                
                mypath=root+"/input/patient/"+study_name+"/images"
                if os.path.isdir(mypath) != True:
                    os.mkdir(mypath)
 
                # check if an RT plan exist if not a==1
                if len(list_rt_plan) >= 1:

                    # the first RT plan is read
                    if os.path.isfile(list_rt_plan[0]) == True:
                        Gammora_print._title("Dicom RT plan for patient "+study_name+" found")
                        rt_plan=list_rt_plan[0]

                        Gammora_print._title2("Reading Dicom RT plan ... ")


                        # Call Gammora_patient class to create a patient object from RT plan
                        patient = Gammora_patient.Patient(rt_plan)

                        Gammora_print._title2(str(patient._get_nb_beam())+" beam found ")
                        Gammora_print._title2(str(patient._get_nb_beam())+" beam will be generated according to config file")


                        # read user config file
                        config=self._read_config_file(config_file)

                        # check user's settings
                        self._check_config(study_name, config)
                      
                        self._set_study_input_name(study_name)
                        if config['SIMU_NAME'] == 'auto':  
                            self._set_study_name(study_name)
                        else:
                            self._set_study_name(config['SIMU_NAME'])

                        self.Beam=[]
                        
                        for beam in patient.Beam:
                            self.Beam.append(Gammora_patient_beam.GammoraPatientBeam(patient, beam, config, self))

                    Gammora_print._separator1()        
                    Gammora_print._title("Generating Gate Macros for patient : " + str(self._get_study_input_name()))

                    for beam in self.Beam:
                        beam.Simu._generate_macros()
                            
                        
                    Gammora_print._separator1() 
                    Gammora_print._title("Gate macros generated")

                    self._save_simu()
                    Gammora_print._title("Simu object saved in: input/gammora_study/"+str(self._get_study_name())+".gmr")
                    Gammora_print._separator1()
                    self._clear()
                    #print('end.')

                else:
                    Gammora_print._error("Dicom RT plan for study : "+study_name+" not found", [])
                    exit()

            else:
                Gammora_print._error("Study "+study_name+" not found", [])
                exit()
                
# Manual Mode 
        elif study_type == 'manual':
            
            # define gammora study type
            self._set_from_scratch(True)

            Gammora_print._title("Simulation From Scratch")
            
            config=self._read_config_file(config_file)
                    
            self._check_config(study_name, config)

            #if config['SIMU_NAME'] == 'auto':  
            self._set_study_name(study_name)
            #else:
            #    self._set_study_name(config['SIMU_NAME'])

            Gammora_print._title("Study Name : "+study_name)
            self.Beam=[]
            self.Beam.append(Gammora_manual_beam.GammoraManualBeam(config, self))

            for beam in self.Beam:
                beam.Simu._generate_macros()
            print()
            print("Gate macros generated")

            self._save_simu()
            print("Simu object saved in: input/simu_obj/"+study_name+".gtb")
            print('')
            self._clear()
            print('end.')


# Gammora Object Mode
        elif study_type == 'gammora':
            print('gammora')

            if study_name.endswith('.gtb'):
                print()
                print("Simulation From Gate Simu Object")
                print("Config File is ignored")
                print()
                print("* Simu Object: "+study_name+" found")
                print()
                self._set_study_name(study_name)
                print("Loading Simu Obj")
                self=self._load_simu(study_name)
                for simu in self.simu:
                    print("     * "+str(simu._get_simu_name())+" beam found ")
                    print("     * "+str(simu._get_simu_name())+" beam will be generated (config file ignored")

                    simu._generate_macros0()

                self._clear()

                #self._set_default_settings_from_simu_obj(name)
#                self._set_from_scratch(False)
#                self._set_from_simu_obj(True)
#                self._set_from_patient(False)
#        self._set_from_scratch(False)
#        self._set_from_simu_obj(True)
#        self._set_from_patient(False)
        


        
# =============================================================    
# Getteur and Setteur------------------------------------------
# =============================================================

# General Gate settings ----------------------------------------
    def _set_from_scratch(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: From Scratch mode must be bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == True:
            self._set_from_patient(False)
            self._set_from_simu_obj(False)
        self.fromScratch = a

    def _get_from_scratch(self):
        return(self.fromScratch)

    def _set_from_patient(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: From Patient mode must be bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == True:
            self._set_from_scratch(False)
            self._set_from_simu_obj(False)
        self.fromPatient = a

    def _get_from_patient(self):
        return(self.fromPatient)
    
    def _set_from_simu_obj(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: From Simu Object mode must be bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == True:
            self._set_from_patient(False)
            self._set_from_scratch(False)
        self.fromSimuObj = a

    def _get_from_simu_obj(self):
        return(self.fromSimuObj)
    
    def _set_study_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Simu Name type must be string")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.Name = a

    def _get_study_name(self):
        return(self.Name)
    
    def _set_study_input_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Simu Name type must be string")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.InputName = a

    def _get_study_input_name(self):
        return(self.InputName)

# Read config file ----------------------------------------
    def _read_config_file(self, config_file):
        Gammora_print._separator1()
        print("* Reading Configuration ... ")
        root = os.getcwd()
        config = {}
        with open(root+'/'+config_file, 'r') as file:
            lines = file.readlines()

            simu_name=lines[lines.index("=SIMULATION_NAME=\n")+1].rstrip()
            visu=lines[lines.index("=VISU=\n")+1].rstrip()
            physics=lines[lines.index("=PHYSICS=\n")+1].rstrip()
            head_part=lines[lines.index("=HEAD_SIMULATION=\n")+1].rstrip()
            patient_part=lines[lines.index("=PATIENT_SIMULATION=\n")+1].rstrip()
            test_part=lines[lines.index("=TEST_SIMULATION=\n")+1].rstrip()
            index=lines[lines.index("=INDEX=\n")+1].rstrip()
            split_type=lines[lines.index("=SPLIT_TYPE=\n")+1].rstrip()
            
            gantry=lines[lines.index("=GANTRY=\n")+1].rstrip()
            gantry_stop=lines[lines.index("=GANTRY_STOP=\n")+1].rstrip()
            gant_rot_dir=lines[lines.index("=ROTATION_DIRECTION=\n")+1].rstrip()
            colli=lines[lines.index("=COLLI=\n")+1].rstrip()
            x1=lines[lines.index("=X1=\n")+1].rstrip()
            x2=lines[lines.index("=X2=\n")+1].rstrip()
            y1=lines[lines.index("=Y1=\n")+1].rstrip()
            y2=lines[lines.index("=Y2=\n")+1].rstrip()
            mlc=lines[lines.index("=MLC=\n")+1].rstrip()
            mlc_file=lines[lines.index("=MLC_FILE=\n")+1].rstrip()
            phantom=lines[lines.index("=PHANTOM=\n")+1].rstrip()
            
            phsp_actor=lines[lines.index("=PHSP_ACTOR=\n")+1].rstrip()
            patient_actor=lines[lines.index("=PATIENT_ACTOR=\n")+1].rstrip()
            patient_actor_size=lines[lines.index("=PATIENT_ACTOR_SIZE=\n")+1].rstrip()
            patient_actor_res=lines[lines.index("=PATIENT_ACTOR_RESOLUTION=\n")+1].rstrip()

            source=lines[lines.index("=SOURCE=\n")+1].rstrip()
            energy=lines[lines.index("=ENERGY=\n")+1].rstrip()
            nb_part=lines[lines.index("=NB_PART=\n")+1].rstrip()
            recycling=lines[lines.index("=RECYCILNG=\n")+1].rstrip()

            execute_on_cluster=lines[lines.index("=EXECUTE_ON_CLUSTER=\n")+1].rstrip()

            config['SIMU_NAME']=simu_name
            config['VISU']=visu
            config['PHYSICS']=physics
            config['HEAD_SIMULATION']=head_part
            config['PATIENT_SIMULATION']=patient_part
            config['TEST_SIMULATION']=test_part
            config['INDEX']=index
            config['SPLIT_TYPE']=split_type

            config['GANTRY']=gantry
            config['GANTRY_STOP']=gantry_stop
            config['ROTATION_DIRECTION']=gant_rot_dir
            config['COLLI']=colli
            config['X1']=x1
            config['X2']=x2
            config['Y1']=y1
            config['Y2']=y2
            config['MLC']=mlc
            config['MLC_FILE']=mlc_file
            config['PHANTOM']=phantom

            config['PHSP_ACTOR']=phsp_actor
            config['PATIENT_ACTOR']=patient_actor
            config['PATIENT_ACTOR_SIZE']=patient_actor_size
            config['PATIENT_ACTOR_RESOLUTION']=patient_actor_res

            config['SOURCE']=source
            config['ENERGY']=energy
            config['NB_PART']=nb_part
            config['RECYCLING']=recycling

            config['EXECUTE_ON_CLUSTER']=execute_on_cluster

            return config

# Check config file --------------------------------------
    def _check_config(self, study_name, config):
        # check individually all parameters of config file

        root = os.getcwd()
        Gammora_print._separator1()
        Gammora_print._title("Checking Configuration ... ")
        

        if config['VISU'] == '0' or config['VISU'] == '1' or config['VISU'] == '2' or config['VISU'] == 'auto':
            Gammora_print._title2("Visualization : ok")
        else:
            Gammora_print._error_config("Visualization", config['VISU'], ["0 = no", "1 = yes", "2 : yes (MLC view)", "auto"])
            exit()

        if config['PHYSICS'] == '0' or config['PHYSICS'] == 'auto' or config['PHYSICS'] == '1':
            Gammora_print._title2("Physics : ok")
        elif config['PHYSICS'].endswith('.mac'):
            if os.path.isfile(UtilsMac+config['PHYSICS']) == True:
                Gammora_print._title2("Physics '"+config['PHYSICS']+"' found")
            else:
                Gammora_print._title2("Physics : ")   
                Gammora_print._error_config_file_not_found(UtilsMac+config['PHYSICS'])
                exit()
        else:
            #Gammora_print._title2("Physics : ")   
            Gammora_print._error_config("Physics", config['PHYSICS'], ["0 = no", "1 = yes", "auto", "'.mac file' located in utils/mac/mac_template"])
            exit()


        if config['HEAD_SIMULATION'] == '0' or config['HEAD_SIMULATION'] == '1' or config['HEAD_SIMULATION'] == 'auto':
           Gammora_print._title2("Head simulation : ok")
        else:
            Gammora_print._error_config("Head Simulation", config['HEAD_SIMULATION'], ["0 = no", "1 = yes", "auto"])
            exit()
        
        if config['PATIENT_SIMULATION'] == '0' or config['PATIENT_SIMULATION'] == '1' or config['PATIENT_SIMULATION'] == 'auto':
            Gammora_print._title2("Patient simulation : ok")
        else:
            Gammora_print._error_config("Patient Simulation", config['PATIENT_SIMULATION'], ["0 = no", "1 = yes", "auto"])
            exit()

        if config['TEST_SIMULATION'] == '0' or config['TEST_SIMULATION'] == '1' or config['TEST_SIMULATION'] == 'auto':
            Gammora_print._title2("Test simulation : ok")
        else:
            Gammora_print._error_config("Patient Simulation", config['TEST_SIMULATION'], ["0 = no", "1 = yes", "auto"])
            exit()

        if config['INDEX'] == 'auto':
            Gammora_print._title2("Number of Index : ok")
        else:
            try: 
                int(config['INDEX'])
            except ValueError:
                Gammora_print._error_config("Number of Index", config['INDEX'], ["int > 0", "auto"])
                exit()
            if int(config['INDEX']) < 0:
                Gammora_print._error_config("Number of Index", config['INDEX'], ["int > 0", "auto"])
                exit()

        if config['SPLIT_TYPE'] == 'auto' or config['SPLIT_TYPE'] == 'stat' or config['SPLIT_TYPE'] == 'dyn':
            Gammora_print._title2("Split Type : ok")
        else:
            Gammora_print._error_config("Spliting type", config['SPLIT_TYPE'], ["'stat' (for static)", "'dyn' (for dynamic)"])
            exit()
        
        if config['GANTRY'] == 'auto':
            Gammora_print._title2("Gantry start : ok")
        else:
            try: 
                float(config['GANTRY'])
            except ValueError:
                Gammora_print._error_config("Gantry", config['GANTRY'], ["float value", "auto"])
                exit()
            if float(config['GANTRY']) >= 0 and float(config['GANTRY']) <= 360.0 :
                Gammora_print._title2("Gantry start : ok")
            else:
                Gammora_print._error_config("Gantry", config['GANTRY'], ["float value in [0-360]", "auto"])
                exit()

        if config['GANTRY_STOP'] == 'auto' or config['GANTRY_STOP'] == 'X':
            Gammora_print._title2("Gantry stop : ok")
        else:
            try: 
                float(config['GANTRY_STOP'])
            except ValueError:
                Gammora_print._error_config("Gantry Stop", config['GANTRY_STOP'], ["float value", "X (for static)", "auto"])
                exit()
            if float(config['GANTRY_STOP']) >= 0 and float(config['GANTRY_STOP']) < 360.0 :
                Gammora_print._title2("Gantry Stop : ok")
            else:
                Gammora_print._error_config("Gantry Stop", config['GANTRY_STOP'], ["float value [0-360]", "X (for static)", "auto"])
                exit()
  
        if config['ROTATION_DIRECTION'] == 'auto' or config['ROTATION_DIRECTION'] == '0' or config['ROTATION_DIRECTION'] == '1':
            Gammora_print._title2("Rotation Direction : ok")
        else:
            Gammora_print._error_config("Rotation Direction", config['ROTATION_DIRECTION'], ["0 for clockwise", "1 for counter clockwise", "auto"])
            exit()
        
        if config['COLLI'] == 'auto':
            Gammora_print._title2("Collimator angle : ok")
        else:
            try: 
                int(config['COLLI'])
            except ValueError:
                Gammora_print._error_config("Colli", config['COLLI'], ["auto", "float value in [-180 - 180]"])
                exit()
            if float(config['COLLI']) > -180 and float(config['COLLI']) < 180.0 :
                Gammora_print._title2("Collimator Angle : ok")
            else:
                Gammora_print._error_config("Colli", config['COLLI'], ["auto", "float value in [-180 - 180]"])
                exit()

        if config['X1'] == 'auto':
            Gammora_print._title2("X1 positions : ok")
        else:
            try: 
                float(config['X1'])
            except ValueError:
                Gammora_print._error_config("X1", config['X1'], ["auto", "float value in [0-210]"])
                exit()
            if float(config['X1']) > 0 or float(config['X1']) < 210 :
                Gammora_print._title2("X1 positions : ok")
            else:
                Gammora_print._error_config("X1", config['X1'], ["auto", "float value in [0-210]"])
                exit()

        if config['X2'] == 'auto':
            Gammora_print._title2("X2 positions : ok")
        else:
            try: 
                float(config['X2'])
            except ValueError:
                Gammora_print._error_config("X2", config['X2'], ["auto", "float value in [0-210]"])
                exit()
            if float(config['X2']) > 0 or float(config['X2']) < 210 :
                Gammora_print._title2("X2 positions : ok")
            else:
                Gammora_print._error_config("X2", config['X2'], ["auto", "float value in [0-210]"])
                exit()

        if config['Y1'] == 'auto':
            Gammora_print._title2("Y1 positions : ok")
        else:
            try: 
                float(config['Y1'])
            except ValueError:
                Gammora_print._error_config("Y1", config['Y1'], ["auto", "float value in [0-210]"])
                exit()
            if float(config['Y1']) > 0 or float(config['Y1']) < 210 :
                Gammora_print._title2("Y1 positions : ok")
            else:
                Gammora_print._error_config("Y1", config['Y1'], ["auto", "float value in [0-210]"])
                exit()

        if config['Y2'] == 'auto':
            Gammora_print._title2("Y2 positions : ok")
        else:
            try: 
                float(config['Y2'])
            except ValueError:
                Gammora_print._error_config("Y2", config['Y2'], ["auto", "float value in [0-210]"])
                exit()
            if float(config['Y2']) > 0 or float(config['Y2']) < 210 :
                Gammora_print._title2("Y2 positions : ok")
            else:
                Gammora_print._error_config("Y2", config['Y2'], ["auto", "float value in [0-210]"])
                exit()

        if config['MLC'] == '0' or config['MLC'] == 'auto' or  config['MLC'] == '1' :
            Gammora_print._title2("MLC :    ok")
        else:
                Gammora_print._error_config("MLC", config['MLC'], ["auto", "0 = no", "1 = yes"])
                exit()

                
        if self._get_from_patient() == True:
        # if MLC option is choosen (1)
            if config['MLC'] == '1' or config['MLC'] == 'auto': 
                if config['MLC_FILE'] != 'auto' and config['MLC_FILE'].endswith('.mlc'):
                        Gammora_print._warning("MLC positions from '.mlc' file when using patient mode not allowed",
                        ["MLC positions from patient data are automatically used"])

        if self._get_from_scratch() == True:
            # if MLC option is choosen (1) for manual simulation a .mlc file must be specified 
            if config['MLC'] == '1' or config['MLC'] == 'auto': 
                if os.path.isfile(UtilsMLC+config['MLC_FILE']) == True and config['MLC_FILE'] != 'auto':
                        Gammora_print._title2(UtilsMLC+config['MLC_FILE']+ " found")
                else:
                        Gammora_print._error_config_file_not_found(UtilsMLC+config['MLC_FILE'])
                        exit()

        
        if config['PHANTOM'] == '0' or config['PHANTOM'] == 'auto' :
            Gammora_print._title2("Phantom : ok")
        else:

            # check if the .mac file of a phantom exist
            if config['PHANTOM'].endswith(".mac"):
                if os.path.isfile(UtilsMacPhantom+config['PHANTOM']) == True:
                    Gammora_print._title2("Phantom : ok")
                    Gammora_print._title2(UtilsMacPhantom+config['PHANTOM'] +" found")
                else:
                    Gammora_print._error_config_file_not_found(UtilsMacPhantom+config['PHANTOM'])
                    exit()

            # To do (not yet possible need to implement functiun to read from mhd in image directory)
            # check if the .mhd file of a pahntom/patient image exist
            elif config['PHANTOM'].endswith(".mhd"):
                if os.path.isfile(UtilsImages+config['PHANTOM']) == True:
                    Gammora_print._title2("Phantom : ok")
                    print("     * ",UtilsImages+config['PHANTOM'], " : found")
                else:
                    Gammora_print._error_config_file_not_found(UtilsMacPhantom+config['PHANTOM'])
                    exit()
            else:
                Gammora_print._error_config("Phantom", config['PHANTOM'], ["auto", "0 = no", "1 = yes", ".mac file", ".mhd file (not yet available)"])
                exit()
        
        if config['PHSP_ACTOR'] == '0' or config['PHSP_ACTOR'] == 'auto'  or config['PHSP_ACTOR'] == '1' :
            Gammora_print._title2("Phsp Actor : ok")

        elif config['PHSP_ACTOR'].endswith('.mac') == True:
            if os.path.isfile(UtilsMacActor+config['PHSP_ACTOR']) == True:
                Gammora_print._title2("Phsp Actor : ok")
                print("     * ",config['PHSP_ACTOR'], ": found")
            else:
                Gammora_print._title2("Phsp Actor :")
                Gammora_print._error_config_file_not_found(UtilsMacActor+config['PHSP_ACTOR'])
                exit()
        else:
            Gammora_print._error_config("Phsp Actor", config['PHSP_ACTOR'], ["auto", "0 = no", "1 = yes", ".mac file"])
            exit()


        if config['PATIENT_ACTOR'] == '0' or config['PATIENT_ACTOR'] == 'auto' or config['PATIENT_ACTOR'] == '1' :
            Gammora_print._title2("Patient Actor :    ok")

        elif config['PATIENT_ACTOR'].endswith('.mac') == True:
            if os.path.isfile(UtilsMacActor+config['PATIENT_ACTOR']) == True:
                Gammora_print._title2("Patient Actor : ok")
                print("     * ",config['PATIENT_ACTOR'], ": found")
            else:
                Gammora_print._title2("Patient Actor :")
                Gammora_print._error_config_file_not_found(UtilsMacActor+config['PATIENT_ACTOR'])
                exit()
        else:
            Gammora_print._error_config("Patient Actor", config['PATIENT_ACTOR'], ["auto", "0 = no", "1 = yes", ".mac file"])
            exit()

        # if config is auto and simulation is built from patient : resolution and actor are slected from DICOM RT dose
        if config['PATIENT_ACTOR_SIZE'] == 'auto':
            if self._get_from_patient() == True:
                # list rt dose for the patient 
                list_rt_dose=glob.glob(root+"/input/patient/"+study_name+"/dicom/RD*")
                if len(list_rt_dose) >= 1:
                    # the first rt dose is used
                    if list_rt_dose[0] == True:
                        Gammora_print._title2("Dicom RT Dose for patient "+study_name+" found")
                        Gammora_print._title2("Patient Actor Size : ok")
                else:
                    Gammora_print._error_config_file_not_found("Dicom RT Dose for patient "+study_name)
                    print(" * Patient Actor size : ok (set to default)")
            # if config is auto and simulation is built from scratch : a default actor is selected 
            if self._get_from_scratch() == True:
                Gammora_print._title2("Patient Actor Size:   ok (set to default)")

        # a .mac actor must be in utils/ dir  
        elif config['PATIENT_ACTOR'].endswith(".mac"):
            if os.path.isfile(UtilsMacActor+config['PATIENT_ACTOR']) == True:
                Gammora_print._title2("Patient Actor Size : ok (set in "+config['PATIENT_ACTOR']+")")
        
        # the size and resolution can be directly specified 
        else :
            try: 
                for val in list(config['PATIENT_ACTOR_SIZE'].split()): float(val)
                #all(isinstance(val,float) for val in list(config['PATIENT_ACTOR_SIZE'].split()))
            except ValueError:
                Gammora_print._error_config("Patient Actor Size", config['PATIENT_ACTOR_SIZE'], ["auto", "list 3 positive float value (for : x, y, z in mm)"])
                exit()
            a=[float(val) for val in list(config['PATIENT_ACTOR_SIZE'].split())]
            
            if len(a) !=3:
                Gammora_print._error_config("Patient Actor Size", config['PATIENT_ACTOR_SIZE'], ["auto", "list 3 positive float value (for : x, y, z in mm)"])
                exit()
            if all(val > 0 for val in a) != True:
                Gammora_print._error_config("Patient Actor Size", config['PATIENT_ACTOR_SIZE'], ["auto", "list 3 positive float value (for : x, y, z in mm)"])
                exit()
        
        if config['PATIENT_ACTOR_RESOLUTION'] == 'auto':
            # if config is auto and simulation is built from patient : resolution and actor are slected from DICOM RT dose

            if self._get_from_patient() == True:
                list_rt_dose=glob.glob(root+"/input/patient/"+study_name+"/dicom/RD*")
                if len(list_rt_dose) >= 1:
                    if list_rt_dose[0] == True:
                        Gammora_print._title2("Patient Actor Resolution : ok")
                else:
                    Gammora_print._error_config_file_not_found("Dicom RT Dose for patient "+study_name)
                    Gammora_print._title2("Patient Actor Resolution : ok (set to default)")
            
            if self._get_from_scratch() == True:
                Gammora_print._title2("Patient Actor Resolution : ok (set to default)")
                
        elif config['PATIENT_ACTOR'].endswith(".mac"):
            if os.path.isfile(UtilsMacActor+config['PATIENT_ACTOR']) == True:
                Gammora_print._title2("Patient Actor Resolution : ok (set in "+config['PATIENT_ACTOR']+")")

        
        else:
            try: 
                for val in list(config['PATIENT_ACTOR_RESOLUTION'].split()): int(val)
            except ValueError:
                Gammora_print._error_config("Patient Actor Size", config['PATIENT_ACTOR_RESOLUTION'], ["auto", "list 3 positive int value (for : x, y, z voxels)"])
                exit()
                exit()
            a=[int(val) for val in list(config['PATIENT_ACTOR_RESOLUTION'].split())]

            if len(a) !=3:
                Gammora_print._error_config("Patient Actor Size", config['PATIENT_ACTOR_RESOLUTION'], ["auto", "list 3 positive int value (for : x, y, z voxels)"])
                exit()
                exit()

            if all(val > 0 for val in a) != True:
                Gammora_print._error_config("Patient Actor Size", config['PATIENT_ACTOR_RESOLUTION'], ["auto", "list 3 positive int value (for : x, y, z voxels)"])
                exit()

        if config['SOURCE'] == '0' or config['SOURCE'] == 'iaea' or config['SOURCE'] == 'gaga' or config['SOURCE'] == 'auto' :
            Gammora_print._title2("Source:    ok")
        elif config['SOURCE'] == 'npy' or config['SOURCE'] == 'root':
            Gammora_print._error_config("Source 'npy' and 'root' to do", config['SOURCE'], ["0 = no", "auto", "iaea", "gaga"])
            exit()
        else:
            Gammora_print._error_config("Source", config['SOURCE'], ["0 = no", "auto", "iaea", "gaga"])
            exit()

        if config['ENERGY'] == 'auto' or config['ENERGY'] == '6X' or config['ENERGY'] == '10X' or config['ENERGY'] == '6FFF' or config['ENERGY'] == '10FFF' :
            Gammora_print._title2("Energy:    ok")
        else:
            Gammora_print._error_config("Energy", config['ENERGY'], [ "auto", "6X" , "10X" , "6FFF" , "10FFF"])
            exit()

        if config['NB_PART'] == 'auto':
            Gammora_print._title2("Number of particle:    ok")
        else:
            try: 
                int(config['NB_PART'])
            except ValueError:
                Gammora_print._error_config("Number of Particle", config['NB_PART'], [ "auto", "int (> 0)"])
                exit()
            # To test
            #if int(config['NB_PART']) >  100:
            #    Gammora_print._title2(" Number of particle:    ok")
            #else:
            #    print(" * Number of particle:   !!! ERROR !!!")
            #    print("     * '",config['NB_PART'],"' not allowed ")
            #    print("     * Choose:  'auto' ; or int > 100 " )
            #    print("     * Please Check config file" )

        if config['RECYCLING'] == 'auto':
            Gammora_print._title2("Recycling:    ok")
        else:
            try:
                int(config['RECYCLING'])
            except ValueError:
                Gammora_print._error_config("Energy", config['RECYCLING'], [ "auto", "float value"])
                exit()
            if int(config['RECYCLING']) >  0:
                Gammora_print._title2("Recycling:    ok")
            else:
                Gammora_print._error_config("Energy", config['RECYCLING'], [ "auto", "float value"])
                exit()

        if config['EXECUTE_ON_CLUSTER'] == 'auto'or config['EXECUTE_ON_CLUSTER'] == '0' or config['EXECUTE_ON_CLUSTER'] == '3' :
            Gammora_print._title2("Execute On Cluster:    ok")

        elif config['EXECUTE_ON_CLUSTER'] == '1' or config['EXECUTE_ON_CLUSTER'] == '2':
            Gammora_print._error_config("Execute On Cluster (for CondorHTC not working yet)", config['EXECUTE_ON_CLUSTER'], [ "0 = no (local simulation)", "auto", "3"])
            exit()
        else:
            Gammora_print._error_config("Execute On Cluster (for CondorHTC not working yet)", config['EXECUTE_ON_CLUSTER'], [ "0 = no (local simulation)", "auto", "3"])
            exit()
        
        Gammora_print._title("Configuration Checked: OK")
        Gammora_print._separator1()


# Save Simu object --------------------------------------
    def _save_simu(self):
        root = os.getcwd()
        with open(root+'/input/gammora_study/'+self._get_study_name()+'.gmr', "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

# Load Simu object --------------------------------------
    def _load_simu(self, name):
        root = os.getcwd()
        with open(root+'/input/gammora_study/'+name, "rb") as f:
            dump = pickle.load(f)
        return dump   


    def _clear(self):
        #print("cleaning..")
        #root = os.getcwd()
        shutil.rmtree(root+"/__pycache__")

        for file in os.listdir():
            if file.endswith(".dat"):
                os.remove(root+'/'+file)
        
        
        for file in os.listdir(root+'/temp'):
            if file == '.gitignore':
                pass
            else:
                os.remove(root+'/temp/'+file)