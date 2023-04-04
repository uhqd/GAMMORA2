import os, glob
import shutil
import fileinput
import math as m
import numpy as np
import pandas as pd
import Gammora_patient

#import myImages
import pickle
import functools
import pydicom as dcm
import subprocess
from stl import mesh

# Class GateSimu
class GammoraBeam():
    def __init__(self):
        pass
# =============================================================    
# Getteur and Setteur------------------------------------------
# =============================================================

# General Gate settings ----------------------------------------

    def _set_study_input_name(self, GammoraStudy):
        self.InputName = GammoraStudy._get_study_input_name() 
        

    def _get_study_input_name(self):
        return(self.InputName)

    def _set_visualization(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Visualization mode must be bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.Visualization = a

    def _get_visualization(self):
        return(self.Visualization)

    def _set_visualization_mode(self, a):
        if type(a) != int:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Visualization mode must be int")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == 1 or  a == 2:
            self.VisualizationMode = a
        else:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Visualization mode must 1 or 2")
            print('!!!!!!!!!!!!!!!!!')
            raise ValueError
    
    def _get_visualization_mode(self):
        return(self.VisualizationMode)

    def _set_material(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: set Material mode must be bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.Material = a

    def _get_material(self):
        return(self.Material)
    
    def _set_material_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Material name mode must be string")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.MaterialName = a
    
    def _get_material_name(self):
        return(self.MaterialName)

    def _set_physics(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Physics must be a bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.Physics = a

    def _get_physics(self):
        return(self.Physics)

    def _set_physics_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Physics Name must be a str")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PhysicsName = a

    def _get_physics_name(self):
        return(self.PhysicsName) 
    
    def _set_head_part_siumulation(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Head Part Simu type must be bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.HeadPartSiumulation = a

    def _get_head_part_siumulation(self):
        return(self.HeadPartSiumulation)

    def _set_patient_part_siumulation(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Patient Part Simu type must be bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PatientPartSimulation = a

    def _get_patient_part_siumulation(self):
        return(self.PatientPartSimulation)

    def _set_test_simulation(self, a):
        if type(a) != bool:
            raise TypeError
        self.TestSimulation = a
    
    def _get_test_siumulation(self):
        return(self.TestSimulation)   

    def _set_beam_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Simu Name type must be string")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.SimuName = a

    def _get_beam_name(self):
        return(self.SimuName) 

    def _set_nb_index(self, a):
        self.Index = a
        
    def _get_nb_index(self):
        return(self.Index)

    def _set_split_type(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Index type must be str")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.SplitType=a   
        
    def _get_split_type(self):
        return(self.SplitType)

    def _set_beam_nb_cpi(self, a):
        if type(a) != int:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Index type must be str")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.Beamcpi=a   
        
    def _get_beam_nb_cpi(self):
        return(self.Beamcpi)
    

# Geometry Gate settings ----------------------------------------

    def _get_gantry_angle(self):
        return(self.GantryAngle)

    def _set_gantry_angle(self, a):
            if type(a) != list:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Gantry Angle must be type of list")
                print('!!!!!!!!!!!!!!!!!')
                raise TypeError
            if all(isinstance(n, float) for n in a) != True:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Gantry Angle must be type of list float")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError
            if min(a) < 0.0 or max(a) > 360.0:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Gantry Angle Value must be positive and < 360")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError
            self.GantryAngle = a

    def _set_gantry_angle_start(self, a):
        if type(a) != float:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Gantry Start Angle must be type of float")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if a < 0.0 or a > 360.0:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Gantry Angle Start Value must be positive and < 360 and > 0")
            print('!!!!!!!!!!!!!!!!!')
            raise ValueError
        self.GantryAngleStart = a

    def _get_gantry_angle_start(self):
        return(self.GantryAngleStart)


    def _set_gantry_angle_stop(self, a):
        #if type(a) != float or  type(a) != str:
        #    print('!!!!!!!!!!!!!!!!!')
        #    print("ERROR: Gantry Stop Angle must be type of float or str ('X')")
        #    print('!!!!!!!!!!!!!!!!!')
        #    raise TypeError
        self.GantryAngleStop = a

    def _get_gantry_angle_stop(self):
        return(self.GantryAngleStop)


    def _get_colli_angle(self):
        return(self.ColliAngle)

    def _set_colli_angle(self, a):
        if type(a) != list:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Colli Angle must be type of list")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if all(isinstance(n, float) for n in a) != True:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Colli Angle must be type of list float")
            print('!!!!!!!!!!!!!!!!!')
            raise ValueError
        self.ColliAngle = a

    def _get_x1(self):
        return(self.X1)

    def _set_x1(self, a):
            if type(a) != list:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: X1 must be type of list")
                print('!!!!!!!!!!!!!!!!!')
                raise TypeError
            if all(isinstance(n, float) for n in a) != True:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: X1 must be type of list float")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError
            if  max(a) > 210.0:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: X1 Value must be positive and < 210.0 mm")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError   
            self.X1 = a

    def _get_x2(self):
        return(self.X2)

    def _set_x2(self, a):
            if type(a) != list:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: X2 must be type")
                print('!!!!!!!!!!!!!!!!!')
                raise TypeError
            if all(isinstance(n, float) for n in a) != True:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: X2 must be type of list float")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError
            if  max(a) > 210.0:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: X2 Value must be positive and < 210.0 mm")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError   
            self.X2 = a

    def _get_y1(self):
        return(self.Y1)

    def _set_y1(self, a):
            if type(a) != list:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Y1 must be type of list")
                print('!!!!!!!!!!!!!!!!!')
                raise TypeError
            if all(isinstance(n, float) for n in a) != True:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Y1 must be type of list float")
                print('!!!!!!!!!!!!!!!!!')
            if  max(a) > 210.0:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Y1 Value must be positive and < 210.0 mm")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError   
            self.Y1 = a
    
    def _get_y2(self):
        return(self.Y2)

    def _set_y2(self, a):
            if type(a) != list:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Y2 must be type of list")
                print('!!!!!!!!!!!!!!!!!')
                raise TypeError
            if all(isinstance(n, float) for n in a) != True:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Y2 must be type of list float")
                print('!!!!!!!!!!!!!!!!!')
            if  max(a) > 210.0:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Y2 Value must be positive and < 210.0 mm")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError   
            self.Y2 = a

    def _get_mlc(self):
        return(self.MLC)

    def _set_mlc(self, a):
        #if type(a) != bool:
        #    print('!!!!!!!!!!!!!!!!!')
        #    print("ERROR: Set MLC must be type of bool")
        #    print('!!!!!!!!!!!!!!!!!')
        #    raise TypeError


        #if a == True and self._get_from_scratch() == True:
        #    #print(a)
        #    print(self._get_from_scratch())
        #    self._set_mlc_sequence([np.arange(0, 120, dtype=np.float).tolist()])

        self.MLC = a

    def _set_mlc_sequence(self, a):
        #print(a)
        if type(a) != list:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: MLC sequence must be type of list")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        for m in a:
            if len(m) > 120 or len(m) < 120:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: One MLC Leaves sequence must have a length of 120")
                print('!!!!!!!!!!!!!!!!!')
                raise ValueError
            if all(isinstance(n, float) for n in m) != True:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: MLC leaf position must be type of float")
                print('!!!!!!!!!!!!!!!!!')
                print(m)
                #raise ValueError
        self.MLC_SEQ = a
        
    def _get_mlc_sequence(self):
        return(self.MLC_SEQ)
    
    def _set_phantom(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phantom must be type of bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.Phantom = a

    def _get_phantom(self):
        return(self.Phantom)

    def _set_patient_ct(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient CT must be type of bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PatientCT = a

    def _get_patient_ct(self):
        return(self.PatientCT)

    def _set_patient_ct_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Ct name must be type of str")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PatientCTName = a

    def _get_patient_ct_name(self):
        return(self.PatientCTName)

    def _set_phantom_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phantom must be type of str")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PhantomName = a

    def _get_phantom_name(self):
        return(self.PhantomName)

    def _set_phantom_motion(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phantom Motion must be type of bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PhantomMotion = a

    def _get_phantom_motion(self):
        return(self.PhantomMotion)

    def _set_phantom_motion_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phantom Motion Name must be type of str")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PhantomMotionName = a

    def _get_phantom_motion_name(self):
        return(self.PhantomMotionName)

    def _set_isocenter_position(self, a):
        if type(a) != list:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Isocenter Position must be type of list")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if len(a) != 3:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Isocenter Position must be a list of lenght 3")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if all(isinstance(n, float) for n in a) != True:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Isocenter Position must be a list of float")
            print('!!!!!!!!!!!!!!!!!')
            raise ValueError
        self.IsocenterPosition = a
         
    def _get_isocenter_position(self):
        return(self.IsocenterPosition)

    def _set_patient_orientation(self, a):
        if type(a) != int:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Orientation must be a int")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == 1 or  a == 2:
            self.PatientOrientation = a
        else:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Orientation must be a int with a value of 1 or 2")
            print('!!!!!!!!!!!!!!!!!')
            raise ValueError
        
    def _get_patient_orientation(self):
        return(self.PatientOrientation)
    
# Actors ----------------------------------------
    def _set_patient_actor(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Actor must be a bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PatientActor = a

    def _get_patient_actor(self):
        return(self.PatientActor)

    def _set_patient_actor_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Actor Name must be a str")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        self.PatientActorName = a

    def _get_patient_actor_name(self):
        return(self.PatientActorName)

    def _set_phsp_actor(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phsp Actor must be a bool")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.PhspActor = a
         
    def _get_phsp_actor(self):
        return(self.PhspActor)
    
    def _set_phsp_actor_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phsp Actor Name must be a str")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.PhspActorName = a

    def _get_phsp_actor_name(self):
        return(self.PhspActorName)

    def _set_patient_actor_size(self, a):
        if type(a) != list:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Actor Size must be a list")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if len(a) != 3:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Actor Size must be a list of lenght 3")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if all(isinstance(n, float) for n in a) != True:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Actor Size must be a list of float")
            print('!!!!!!!!!!!!!!!!!')
            raise ValueError
        self.PatientActorSize = a
        
    def _get_patient_actor_size(self):
        return(self.PatientActorSize)

    def _set_patient_actor_resolution(self, a):
        if type(a) != list:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Actor Resolution must be a list")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if len(a) != 3:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Actor Resolution must be a list of lenght 3")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if all(isinstance(n, int) for n in a) != True:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Patient Actor Resolution must be a list of lenght int")
            print('!!!!!!!!!!!!!!!!')
            raise ValueError
        self.PatientActorResolution = a
        
    def _get_patient_actor_resolution(self):
        return(self.PatientActorResolution)

# Sources ----------------------------------------

    def _set_source(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Source must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.Source = a

    def _get_source(self):
        return(self.Source)

    def _set_energy(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Energy must be str with value of 6X, 6FFF, 10X, 10FFF, 6E, 9E, 12E, 15E, or 18E")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == '6X' or a == '6FFF' or a == '10X' or a == '10FFF' or a == '6E' or a == '9E' or a == '12E' or a == '15E' or a == '18E':
            self.Energy = a
        else:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Energy must be 6X, 6FFF, 10X, 10FFF, 6E, 9E, 12E, 15E, or 18E")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        

    def _get_energy(self):
        return(self.Energy)

    def _set_dose_rate(self, a ):
        if type(a) != list:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Dose Rate must be list")
            print('!!!!!!!!!!!!!!!!!')
            raise TypeError
        if all(isinstance(n, float) for n in a) != True:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Dose Rate value must be list of float")
            print('!!!!!!!!!!!!!!!!!')
            raise ValueError
        else:
            self.DoseRate = a

    def _get_dose_rate(self):
        return(self.DoseRate)

    def _set_source_iaea(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set source IAEA must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.SourceIaea = a

    def _get_source_iaea(self):
        return(self.SourceIaea)

    def _set_source_gaga(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set source IAEA must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.SourceGaga = a

    def _set_gaga_nb_part(self, a):
            """
            set the number the total number of particle for the simulation
            used when a gaga source is used
            """
            if type(a) != int:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Set Number of Particle for GAGA-PHSP must be a int")
                print('!!!!!!!!!!!!!!!!')
                raise TypeError
            self.NbPartGaga = a
            
    def _get_gaga_nb_part(self):
        """
        get the total number of primaries used for gaga source simulation
        """
        return(self.NbPartGaga)
    def _set_iaea_nb_part(self, a):
            """
            set the number the total number of particle for the simulation
            used when a iaea source is used in manual mode
            """
            if type(a) != int:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Set Number of Particle for GAGA-PHSP must be a int")
                print('!!!!!!!!!!!!!!!!')
                raise TypeError
            self.NbPartIAEA = a
    def _get_iaea_nb_part(self):
        """
        get the total number of primaries used for iaea source simulation in manual mode
        """
        return(self.NbPartIAEA)
            
    def _get_manual_nb_part(self):
        """
        get the total number of primaries used for iaea source simulation in manual mode
        """
        return(self.NbPartManual)
    def _set_manual_nb_part(self, a):
            """
            set the number the total number of particle for the simulation
            used when a iaea source is used in manual mode
            """
            if type(a) != bool:
                print('!!!!!!!!!!!!!!!!!')
                print("ERROR: Set Number of Particle for GAGA-PHSP must be a int")
                print('!!!!!!!!!!!!!!!!')
                raise TypeError
            self.NbPartManual = a
            
    def _get_source_gaga(self):
        return(self.SourceGaga)

    def _set_source_root(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set source Root must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.SourceRoot = a

    def _get_source_root(self):
        return(self.SourceRoot)
    
    def _set_source_gps(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set source GPS must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.SourceGPS = a

    def _get_source_gps(self):
        return(self.SourceGPS)

    def _set_reduced_source_name(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Reduced Phsp Name must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.ReducedPhaseSpaceName = a

    def _get_reduced_source_name(self):
        return(self.ReducedPhaseSpaceName)

    def _set_recycling(self, a):
        if type(a) != int:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Recycilng must be a int")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.Recycling = a
        
    def _get_recycling(self):
        return(self.Recycling)

# Computing ----------------------------------------

    def _set_sending(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Sending must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.Send = a

    def _get_sending(self):
        return(self.Send)

    def _set_launching(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Launching must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.Launch = a

    def _get_launching(self):
        return(self.Launch)
    
    def _set_resampling_value(self, a):
        if type(a) != int:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set resampling Value must be a int")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.ResamplingValue = a

    def _get_resampling_value(self):
        return(self.ResamplingValue)

    def _set_resampled(self, a ):
        if type(a) != bool:
            raise TypeError
        self.Resampled = a

    def _is_resampled(self):
        return(self.Resampled)

# Directories ----------------------------------------

    def _set_input_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Input dir must be a int")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.InputDir = a
    
    def _get_input_dir(self):
        return(self.InputDir)

    def _set_output_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Output dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.OutputDir = a
    
    def _get_output_dir(self):
        return(self.OutputDir)

    def _set_local_input_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Local Input dir must be a ste")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.LocalInputDir = a
    
    def _get_local_input_dir(self):
        return(self.LocalInputDir)

    def _set_local_output_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Local Output dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.LocalOutputDir = a

    def _get_local_output_dir(self):
        return(self.LocalOutputDir)
    
    def _set_phsp_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phsp dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.PhspDir = a

    def _get_phsp_dir(self):
        return(self.PhspDir) 

    def _set_phsp_mac_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phsp mac dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.PhspMacDir = a

    def _get_phsp_mac_dir(self):
        return(self.PhspMacDir)     

    def _set_phsp_data_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phsp data dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.PhspDataDir = a

    def _get_phsp_data_dir(self):
        return(self.PhspDataDir)

    def _set_clinic_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Clinic dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.ClinicDir = a

    def _get_clinic_dir(self):
        return(self.ClinicDir) 

    def _set_clinic_mac_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Clinic mac dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.ClinicMacDir = a

    def _get_clinic_mac_dir(self):
        return(self.ClinicMacDir)     

    def _set_clinic_data_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set clinic data dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.ClinicDataDir = a

    def _get_clinic_data_dir(self):
        return(self.ClinicDataDir)

    def _set_test_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Test dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.TestDir = a

    def _get_test_dir(self):
        return(self.TestDir) 

    def _set_test_mac_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Test mac dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.TestMacDir = a

    def _get_test_mac_dir(self):
        return(self.TestMacDir)     

    def _set_test_data_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Test data dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.TestDataDir = a

    def _get_test_data_dir(self):
        return(self.TestDataDir)

    def _set_phsp_dir1(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Phsp file dir must be a str")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        else:
            self.PhspDir1 = a

    def _get_phsp_dir1(self):
        return(self.PhspDir1)
    
# =============================================================    
# Functions for Gate Macros -------------------------------------
# =============================================================  

    def _add_applicator(self): # To Do **
        pass
    def _add_insert(self): # To Do **
        pass
    
    def _define_exact_field_size(self, field):
        """
        Adjust field size with linear model (affine) obtained from experimental measurment vs simulation
        """
        x1_user=field[0]
        x2_user=field[1]
        y1_user=field[2]
        y2_user=field[3]

        if x1_user < 0:
           x1_user = x1_user * -1
        if x2_user < 0:
           x2_user = x2_user * -1
        if y1_user < 0:
           y1_user = y1_user * -1
        if y2_user < 0:
           y2_user = y2_user * -1

        a=1.0004
        b=4.0157
        c=1.0025308
        d=5.7196847
        # divide by 10 for mm->cm
        X1=2*x1_user
        X2=2*x2_user
        Y1=2*y1_user
        Y2=2*y2_user

        x1=(X1-b)/(2*a)
        x2=(X2-b)/(2*a)
        y1=(Y1-d)/(2*c)
        y2=(Y2-d)/(2*c)
        return(x1,x2,y1,y2)        

    def _compute_x1_position(self, x1_user):
        """
        compute x, y translation and rotation
        """
        a = 1.5
        b = 134.62
        c = 77.724
        d = 34.036
        e = 43.688
        f = 30.226
        g = 366.1
        sourceToIso = 1000.0

        X1user = x1_user
        alfaR = m.atan((X1user-a)/sourceToIso) 
        alfaD = alfaR*180.0/m.pi

        h = (g+d)*m.tan(alfaR)
        i = f / m.cos(alfaR)
        betaR = m.atan(b/c)
        OMprim = m.sqrt((b/2.0)*(b/2.0)+(c/2.0)*(c/2.0))
        xMprim = OMprim*m.sin(betaR + alfaR)
        gammaR = m.atan(f/d)
        OTprim = m.sqrt(f*f+d*d)
        xTprim = OTprim*m.sin(gammaR + alfaR)
        j = abs(xMprim - xTprim)
        XMprime = a + h + i + j

        yMprim = OMprim*m.cos(betaR + alfaR)
        yTprim = OTprim*m.cos(gammaR + alfaR)
        k = abs(yMprim - yTprim)
        YMprime = g+ d + k
        
        #print(XMprime,-YMprime,alfaD)
        return(XMprime,-YMprime,alfaD)

    def _compute_x2_position(self, x2_user):
        """
        compute x, y translation and rotation
        """
        a = 1.5
        b = 134.62
        c = 77.724
        d = 34.036
        e = 43.688
        f = 30.226
        g = 366.1
        sourceToIso = 1000.0
        X2user = x2_user
        alfaR = m.atan((X2user-a)/sourceToIso) 
        alfaD = alfaR*180.0/m.pi
        h = (g+d)*m.tan(alfaR)
        i = f / m.cos(alfaR)
        betaR = m.atan(b/c)
        OMprim = m.sqrt((b/2.0)*(b/2.0)+(c/2.0)*(c/2.0))
        xMprim = OMprim*m.sin(betaR + alfaR)
        gammaR = m.atan(f/d)
        OTprim = m.sqrt(f*f+d*d)
        xTprim = OTprim*m.sin(gammaR + alfaR)
        j = abs(xMprim - xTprim)
        XMprime = a + h + i + j

        yMprim = OMprim*m.cos(betaR + alfaR)
        yTprim = OTprim*m.cos(gammaR + alfaR)
        k = abs(yMprim - yTprim)
        YMprime = g+ d + k
        #print(-XMprime,-YMprime,-alfaD)
        return(-XMprime,-YMprime,-alfaD)
        
    def _compute_y1_position(self, y1_user):
        """
        compute x, z translation and rotation
        """
        Y1user = y1_user
        a = 2.7
        OH = 1000.0
        r = 281.6
        b = 119.38
        c = 77.724
        d = 187.96
        e = 1.5
        betaR = m.atan((Y1user - e) / OH)
        betaD = betaR*180.0/m.pi
        u = OH / (Y1user - e)
        v = a - u*e
        delta = 4.0*u*u*v*v - 4.0*(1.0 + u*u)*(v*v - r*r)
        xG = (-2.0*u*v + m.sqrt(delta)) / (2.0*(1.0+u*u))
        yG = u*xG + v - a
        gammaR = m.atan(b/c)
        diag = m.sqrt(b*b+c*c)
        x2 = (diag/2.0) * m.sin(gammaR + betaR)
        y2 = (diag/2.0) * m.cos(gammaR + betaR)
        xM = xG + x2
        yM = yG + y2
        #print(-xM,-yM,betaD)
        return(-xM,-yM,betaD)
        
    def _compute_y2_position(self, y2_user):
        """
        compute x, z translation and rotation
        """
        Y2user = y2_user
        a = 2.7
        OH = 1000.0
        r = 281.6
        b = 119.38
        c = 77.724
        d = 187.96
        e = 1.5
        betaR = m.atan((Y2user - e) / OH)
        betaD = betaR*180.0/m.pi
        u = OH / (Y2user - e)
        v = a - u*e
        delta = 4.0*u*u*v*v - 4.0*(1.0 + u*u)*(v*v - r*r)
        xG = (-2.0*u*v + m.sqrt(delta)) / (2.0*(1.0+u*u))
        yG = u*xG + v - a
        gammaR = m.atan(b/c)
        diag = m.sqrt(b*b+c*c)
        x2 = (diag/2.0) * m.sin(gammaR + betaR)
        y2 = (diag/2.0) * m.cos(gammaR + betaR)
        xM = xG + x2
        yM = yG + y2 
        #print(xM,-yM,-betaD)
        return(xM,-yM,-betaD)
    
    def _compute_jaws(self, field):   #field=[x1, x2, y1, y2]
        """
        compute jaws translation and rotation
        """
        new_field=self._define_exact_field_size(field)
        new_x1=self._compute_x1_position(new_field[0])
        new_x2=self._compute_x2_position(new_field[1])
        new_y1=self._compute_y1_position(new_field[2])
        new_y2=self._compute_y2_position(new_field[3])
        return(new_x1,new_x2,new_y1,new_y2)
        
    def _compute_gantry_rot(self, gant_rot_user):
        #For clinical gantry rotation of x
        #set rotation to -x
        #set translation at
        #x = 1000.sin(x)
        #y = 1000.cos(x)
        gantRot = -gant_rot_user #**
        #gantRot = gant_rot_user
        gantX = 1000*m.sin(-gantRot*m.pi/180.0)
        gantY = 1000*m.cos(-gantRot*m.pi/180.0)
        #print(gantRot,gantX,gantY)
        if self._get_split_type() == 'dyn':
            a = -gantRot
        if self._get_split_type() == 'stat':
            a = gantRot
        return(a,gantX,gantY)
            
    def _compute_colli_position(self, colli_user):
        #Change collimator rotation here:
        #For clinical collimator rotation of x
        #Set rotation to x
        #to be checked !!!!!!
        colli = colli_user
        colli = (colli + 180.0)
        if (colli >= 360.0):
            colli = colli -360.0
        return colli               
    

    # To do modify code C to send .dat file in a temp  directory spcific to the study
    def _compute_mlc_position_fromC(self, file):
        root = os.getcwd()
        shutil.copyfile(root+'/utils/C/bin/makeMLC', root+'/makeMLC')

        # used to fix permission errors with git
        os.system('chmod 755 makeMLC')

        proc = subprocess.Popen(["./makeMLC", file])
        proc.wait()

    def _create_mlc_file(self, beam):
        root = os.getcwd()
        #for cpi in range(0, self._get_nb_index()):
        for cpi in range(0, self._get_beam_nb_cpi()):
            with open(root+ '/temp/'+str(cpi)+'-'+self._get_beam_name()+'_mlc.mlc', 'w') as mlc_file:
                mlc_file.write('File Rev = H ' + '\n')
                mlc_file.write('Treatment = ' + 'DYNAMIC' + '\n')
                mlc_file.write('Last Name = ' + self._get_beam_name() + '\n')
                mlc_file.write('First Name = ' + '\n')
                mlc_file.write('Patient ID = ' + self._get_beam_name() + '\n')
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
                        posa=round(((leafs_/10.0)*-1), 4)
                        mlc_file.write('Leaf ' + str(ii + 1) + 'A = ' + str(posa) + '\n')
                        #listB.append(leafs_)
                        #print('Leaf ' + str(ii + 1) + 'A = ' + str((leafs_/10.0)*-1) + '\n')
                    else:
                        #listA.append(leafs_)
                        posb=round((leafs_/10.0), 4)
                        mlc_file.write('Leaf ' + str(ii - 59) + 'B = ' + str(posb) + '\n')
                        #print('Leaf ' + str(ii - 59) + 'B = ' + str(leafs_/10.0) + '\n')                  
                    ii=ii+1                

                mlc_file.write('Note = 0' + '\n')
                mlc_file.write('Shape = 0' + '\n')
                mlc_file.write('Magnification  = 1.00' + '\n' + '\n')            
                
                #print(mlc_file_name + ' --> created')    
                mlc_file.close()

