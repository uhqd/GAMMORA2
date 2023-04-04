import shutil
import os
import fileinput
import pandas as pd
import Gammora_beam
import Gammora_patient_beam
import Gammora_patient
import Gammora_images
import Gammora_print

class GammoraSimu():

#=======================
# Constructor 
#======================= 

    def __init__(self):
        pass
#=======================
# Getteur and setteur 
#=======================

#-----------------------
# Directories 
#-----------------------

    def _set_simu_name(self, GammoraBeam):
        self.SimuName = GammoraBeam._get_beam_name()

    def _get_simu_name(self):
        return(self.SimuName)

    def _set_split_type(self, GammoraBeam):
        self.SplitType=GammoraBeam._get_split_type()  
        
    def _get_split_type(self):
        return(self.SplitType)

    def _set_user(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set User must be a user (name used in CALMIP)")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        self.User = a

    def _get_user(self):
        return(self.User)

    def _set_calmip(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Calmip must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == True:
            self._set_apple_cluster(False)
            self._set_local(False)
        self.OnCalmip = a

    def _get_calmip(self):
        return(self.OnCalmip)
    
    def _set_apple_cluster(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Apple Cluster must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == True:
            self._set_calmip(False)
            self._set_local(False)
        self.OnAppleCluster = a

    def _get_apple_cluster(self):
        return(self.OnAppleCluster)

    def _set_head_part_siumulation(self, GammoraBeam):
        self.HeadPartSiumulation = GammoraBeam._get_head_part_siumulation()

    def _get_head_part_siumulation(self):
        return(self.HeadPartSiumulation)

    def _set_patient_part_siumulation(self, GammoraBeam):
        self.PatientPartSimulation = GammoraBeam._get_patient_part_siumulation()

    def _get_patient_part_siumulation(self):
        return(self.PatientPartSimulation)

    def _set_local(self, a):
        if type(a) != bool:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Local must be a bool")
            print('!!!!!!!!!!!!!!!!')
            raise TypeError
        if a == True:
            self._set_calmip(False)
            self._set_apple_cluster(False)
        self.OnLocal = a

    def _get_local(self):
        return(self.OnLocal)

    def _set_input_dir(self, a):
        if type(a) != str:
            print('!!!!!!!!!!!!!!!!!')
            print("ERROR: Set Input dir must be a str")
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
            print("ERROR: Set Local Input dir must be a str")
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

#=======================
# Gate Macros Function 
#=======================

# General
#--------

    def _create_main_mac_file(self, mac_directory):        
        shutil.copyfile(UtilsMac+'Xmain.macX',mac_directory+'/main.mac')
   
    def _add_verbose(self, mac_directory, data_directory, exec_dir):
        with open(mac_directory+'/main.mac', 'a') as file:   
            verbose='/control/execute '+ exec_dir +'/verbose.mac'
            file.write(verbose+"\n")
        shutil.copyfile(UtilsMac+'Xverbose.macX',data_directory+'/verbose.mac')
    
    def _add_visualization(self, mac_directory, data_directory, exec_dir):
        with open(mac_directory+'/main.mac', 'a') as file:
            visu='/control/execute '+exec_dir+'/visu.mac'
            file.write(visu+"\n")
        if self.Beam._get_visualization_mode() == 1:
            shutil.copyfile(UtilsMac+'Xvisu_clinic.macX',data_directory+'/visu.mac')
        if self.Beam._get_visualization_mode() == 2:
            shutil.copyfile(UtilsMac+'Xvisu_mlc.macX',data_directory+'/visu.mac')
            
    def _add_material_tab(self, mac_directory, data_directory, exec_dir):
        with open(mac_directory+'/main.mac', 'a') as file:   
            material='/gate/geometry/setMaterialDatabase '+exec_dir+'/TBMaterials.tb'
            file.write(material+"\n")
        shutil.copyfile('utils/material/'+self.Beam._get_material_name() , data_directory+'/TBMaterials.tb')
                    
    def _add_world_geometry(self, mac_directory, data_directory, exec_dir):
        with open(mac_directory+'/main.mac', 'a') as file:   
            world='/control/execute '+exec_dir+'/world.mac'
            file.write(world+"\n")
        shutil.copyfile(UtilsMac+'Xworld.macX',data_directory+'/world.mac')
        return
    
    def _add_treatment_head(self, mac_directory, data_directory, exec_dir):
        with open(mac_directory+'/main.mac', 'a') as file:   
            treatment_head='/control/execute '+exec_dir+'/treatment_head.mac'
            file.write(treatment_head + "\n")
        shutil.copyfile(UtilsMac+'Xhead.macX',data_directory+'/treatment_head.mac')
        return
    
    def _add_phase_space_volume(self, mac_directory, data_directory, exec_dir):
        with open(mac_directory+'/main.mac', 'a') as file:   
            phase_space='/control/execute '+exec_dir+'/phase_space_volume.mac'
            file.write(phase_space+"\n")
        shutil.copyfile(UtilsMac+'Xphase_space_volume.macX',data_directory+'/phase_space_volume.mac')
        return
    
    def _add_only_cylinder_phase_space_volume(self, mac_directory, data_directory, exec_dir):
        
        with open(mac_directory+'/main.mac', 'a') as file:   
            phase_space='/control/execute '+exec_dir+'/phase_space_volume.mac'
            file.write(phase_space+"\n")
        shutil.copyfile(UtilsMac+'Xcylinder_phase_space_volume.macX',data_directory+'/phase_space_volume.mac')
        return

    def _add_kill_box(self, mac_directory, data_directory, exec_dir):
        
        with open(mac_directory+'/main.mac', 'a') as file:
            kill_box='/control/execute '+exec_dir+'/kill_box.mac'
            file.write(kill_box+"\n")
        shutil.copyfile(UtilsMac+'Xkill_box.macX',data_directory+'/kill_box.mac')
        return
                           
    def _add_initialize_command(self, mac_directory):
        with open(mac_directory, 'a') as file:       
            run='/gate/run/initialize'
            file.write(run+"\n")

    def _add_run_command(self, mac_directory):
        with open(mac_directory, 'a') as file:       
            start='/gate/application/start'
            describe='/gate/application/describe'
            file.write(start+"\n")
            file.write(describe+"\n")

    def _decorate(self, file, string):
        with open(file, 'a') as file:       
            file.write("\n"+"# "+string+" -------------------"+"\n")

# Patient and phantom geometries
#--------
# + Patient CT

    def _add_patient_ct(self, ct_dir, isocenter, mac_directory, data_directory, exec_dir):
        """
        convert dicom into mhd + crop orignal CT to by compliant with GATE geometry
        cropping is automatic (need to be checked before launch simulation)
        """
        print("")
        ct_name=self._get_simu_name()
        shutil.copyfile(UtilsMac+'Xpatient_ct.macX',data_directory+'/patient_ct.mac')
        shutil.copyfile(UtilsMacPhantom+'/ct_tools/iuc_DensitiesTables.txt', data_directory+'/iuc_DensitiesTables.txt')
        shutil.copyfile (UtilsMacPhantom+'/ct_tools/Schneider2000DensitiesTable.txt',data_directory+'/Schneider2000DensitiesTable.txt')
        shutil.copyfile (UtilsMacPhantom+'/ct_tools/Schneider2000MaterialsTable.txt' ,data_directory+'/Schneider2000MaterialsTable.txt')


        Gammora_print._title2("Generating CT 'mhd' image from dicom CT slices ...")
        self.input_image = Gammora_images.GammoraCT(self.Beam)  #deals with dicom CT
        Gammora_print._title2("CT 'mhd' image generated")
        shutil.copyfile(self._get_local_input_dir()+'/images/'+ct_name+'.mhd', data_directory+'/'+ct_name+'.mhd')
        shutil.copyfile(self._get_local_input_dir()+'/images/'+ct_name+'.raw', data_directory+'/'+ct_name+'.raw')
        shutil.copyfile(self._get_local_input_dir()+'/images/'+ct_name+'_original.mhd', data_directory+'/'+ct_name+'_original.mhd')
        shutil.copyfile(self._get_local_input_dir()+'/images/'+ct_name+'_original.raw', data_directory+'/'+ct_name+'_original.raw')
        Gammora_print._title2("CT 'mhd' image copied")
        file=fileinput.FileInput(data_directory+'/patient_ct.mac', inplace=1)
        for line in file:
            line=line.replace("isox", str(isocenter[0]))
            line=line.replace("isoy", str(isocenter[1]))
            line=line.replace("isoz", str(isocenter[2]))
            line=line.replace("PATIENT_CT", ''+exec_dir+'/'+ct_name+'_original.mhd')
            line=line.replace("DATA_DIR", exec_dir)
            print(line)
        file.close()
        with open(mac_directory+'/main.mac', 'a') as file:
            ct='/control/execute '+exec_dir+'/patient_ct.mac'
            file.write(ct+"\n")

# + Phantom
                   
    def _add_phantom(self, phantom_name, mac_directory, data_directory, exec_dir):
        #print(self._get_phantom_name())
        pn=self.Beam._get_phantom_name().split('/')[-1]  
        shutil.copyfile(self.Beam._get_phantom_name(), data_directory+'/'+pn)
        with open(mac_directory+'/main.mac', 'a') as file:
            phantom='/control/execute '+exec_dir+'/'+pn
            file.write(phantom+"\n")

# + Couch

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
            line=line.replace("x_shift", str(self.Beam._get_isocenter_position()[0]*-1))
            line=line.replace("y_shift", str(self.Beam._get_isocenter_position()[1]*-1))
            line=line.replace("z_shift", str(self.Beam._get_isocenter_position()[2]*-1))
            print(line)
 

# Physics
#--------            
    def _add_physics(self, mac_directory, data_directory, exec_dir):
        with open(mac_directory+'/main.mac', 'a') as file:
            physics='/control/execute '+exec_dir+'/physics.mac'
            file.write(physics+"\n")
        shutil.copyfile(self.Beam._get_physics_name(), data_directory+'/physics.mac')
        return

    def _add_physics_cut(self): # To Do**
        pass

# Phsp an patient actors
#--------

    def _add_patient_actor(self, actor, mac_directory, data_directory): # ** To Do: choose for uncertainty
        """
        choose an actor
        """
        
        actor_file=actor.split('/')[-1]

        shutil.copyfile(actor, data_directory+'/'+actor_file)
        file=fileinput.FileInput(data_directory+'/'+actor_file, inplace=1)
        lines = []
        for line in file:
            line=line.replace("x_size", str(self.Beam._get_patient_actor_size()[0]))
            line=line.replace("y_size", str(self.Beam._get_patient_actor_size()[1]))
            line=line.replace("z_size", str(self.Beam._get_patient_actor_size()[2]))
            line=line.replace("x_res", str(self.Beam._get_patient_actor_resolution()[0]))
            line=line.replace("y_res", str(self.Beam._get_patient_actor_resolution()[1]))
            line=line.replace("z_res", str(self.Beam._get_patient_actor_resolution()[2]))

            lines.append(line)
        file.close()

        with open(mac_directory+'/main.mac', 'a') as file:
            for line in lines:
                file.write(line)

    def _add_phsp_actor(self, actor, mac_directory, data_directory): # ** To implement: choose for uncertainty
        """
        choose an actor
        """
        actor_file=actor.split('/')[-1]

        shutil.copyfile(actor, data_directory+'/'+actor_file)
        file=fileinput.FileInput(data_directory+'/'+actor_file, inplace=1)
        lines = []
        for line in file:
            lines.append(line)
        file.close()

        with open(mac_directory+'/main.mac', 'a') as file:
            for line in lines:
                file.write(line)
       
    def _add_counter(self, mac_directory, data_directory):
        """
        Do not delete useful for simulation monitoring in calmip
        """

        shutil.copyfile(UtilsMac+'Xcounter.macX',data_directory+'/counter.mac')
        lines=[]
        file=fileinput.FileInput(data_directory+'/counter.mac', inplace=1)
        for line in file:
            lines.append(line)
        file.close()

        with open(mac_directory+'/main.mac', 'a') as file:
            for line in lines:
                file.write(line)

# Head geometry
#--------

# + Jaws
    def _apply_jaws_stat(self, field, mac_directory):
        """
        apply jaws translation and rotation to the generated macros
        """
        with open(mac_directory, 'a') as file:
            file.write("\n"+"/gate/X1/placement/setTranslation "+str(field[0][0])+" "+str(field[0][1])+" 0.0 mm")
            file.write("\n"+"/gate/X2/placement/setTranslation "+str(field[1][0])+" "+str(field[1][1])+" 0.0 mm") 
            file.write("\n"+"/gate/Y1/placement/setTranslation 0.0 "+str(field[2][1])+" "+str(field[2][0])+" mm")
            file.write("\n"+"/gate/Y2/placement/setTranslation 0.0 "+str(field[3][1])+" "+str(field[3][0])+" mm")
            
            file.write("\n"+"/gate/X1/placement/setRotationAngle "+str(field[0][2])+" deg")
            file.write("\n"+"/gate/X2/placement/setRotationAngle "+str(field[1][2])+" deg")
            file.write("\n"+"/gate/Y1/placement/setRotationAngle "+str(field[2][2])+" deg")
            file.write("\n"+"/gate/Y2/placement/setRotationAngle "+str(field[3][2])+" deg"+"\n")
        file.close()

    def _apply_jaws_dyn(self, mac_directory, data_directory, exec_dir):
        """
        apply jaws translation and rotation to the generated macros
        """
        shutil.copyfile(UtilsPlacements+'x1.placementsXXX',data_directory+'/x1.placements')
        shutil.copyfile(UtilsPlacements+'x2.placementsXXX',data_directory+'/x2.placements')
        shutil.copyfile(UtilsPlacements+'y1.placementsXXX',data_directory+'/y1.placements')
        shutil.copyfile(UtilsPlacements+'y2.placementsXXX',data_directory+'/y2.placements')
        with open(mac_directory, 'a') as file:
            file.write("\n"+"/gate/X1/moves/insert genericMove")
            file.write("\n"+"/gate/X1/genericMove/setPlacementsFilename "+exec_dir+"/x1.placements")
            file.write("\n"+"/gate/X2/moves/insert genericMove")
            file.write("\n"+"/gate/X2/genericMove/setPlacementsFilename "+exec_dir+"/x2.placements")
            file.write("\n"+"/gate/Y1/moves/insert genericMove")
            file.write("\n"+"/gate/Y1/genericMove/setPlacementsFilename "+exec_dir+"/y1.placements")
            file.write("\n"+"/gate/Y2/moves/insert genericMove")
            file.write("\n"+"/gate/Y2/genericMove/setPlacementsFilename "+exec_dir+"/y2.placements")   
        file.close()
        with open(data_directory+'/x1.placements', 'a') as fx1, open(data_directory+'/x2.placements', 'a') as fx2, open(data_directory+'/y1.placements', 'a') as fy1, open(data_directory+'/y2.placements', 'a') as fy2:
            for i in range(0, self.Beam._get_beam_nb_cpi()):
                pos=self.Beam._compute_jaws([self.Beam._get_x1()[i], self.Beam._get_x2()[i], self.Beam._get_y1()[i], self.Beam._get_y2()[i]])
                #print(pos)
                # Bug in GATE : we temporarily put a minus sign for the angle
                # Setplacement file 
                fx1.write(str(float(i)) + ' ' + str(-pos[0][2]) + ' ' + '0 0 1 ' + str(pos[0][0]) + ' ' + str(pos[0][1]) + ' 0.0' )
                fx2.write(str(float(i)) + ' ' + str(-pos[1][2]) + ' ' + '0 0 1 ' + str(pos[1][0]) + ' ' + str(pos[1][1]) + ' 0.0' )
                fy1.write(str(float(i)) + ' ' + str(-pos[2][2]) + ' ' + '1 0 0 ' + '0.0 ' + str(pos[2][1]) + ' ' + str(pos[2][0])) #**
                fy2.write(str(float(i)) + ' ' + str(-pos[3][2]) + ' ' + '1 0 0 ' + '0.0 ' + str(pos[3][1]) + ' ' + str(pos[3][0])) #**
                fx1.write("\n")
                fx2.write("\n")
                fy1.write("\n")
                fy2.write("\n")

# + Gantry
    
    def _apply_gantry_rot_stat(self, gantValues, mac_directory):
        with open(mac_directory, 'a') as file:
            file.write("\n"+"/gate/mylinac/placement/setRotationAngle "+str(gantValues[0])+" deg")
            #file.write("\n"+"/gate/mylinac/placement/setTranslation "+str(gantValues[1])+" "+str(gantValues[2])+" 0.0 mm")
            file.write("\n"+"/gate/mylinac/placement/setTranslation "+str(gantValues[1])+" "+str(gantValues[2])+" 0.0 mm"+"\n")

    def _apply_gantry_rot_dyn(self, mac_directory, data_directory, exec_dir):
        shutil.copyfile(UtilsPlacements+'gantryMovement.placementsXXX',data_directory+'/gantryMovement.placements')
        with open(mac_directory, 'a') as file:
            file.write("\n"+"/gate/mylinac/moves/insert genericMove")
            file.write("\n"+"/gate/mylinac/genericMove/setPlacementsFilename "+exec_dir+"/gantryMovement.placements")
        with open(data_directory+'/gantryMovement.placements', 'a') as f:
            for i in range(0,  self.Beam._get_beam_nb_cpi()):
                g=self.Beam._compute_gantry_rot(self.Beam._get_gantry_angle()[i])
                f.write(str(float(i)) + ' ' + str(g[0]) + ' ' + '0 0 1 ' + str(g[1]) + ' ' + str(g[2]) + ' 0.0' )
                f.write("\n")
# + Collimator

    def _apply_colli_rot(self, colliRot,mac_directory):
        with open(mac_directory, 'a') as file:
            file.write("\n"+"/gate/myLinacHead/placement/setRotationAngle "+str(colliRot)+" deg"+"\n")

# + MLC

# ++ MLC : static splitting
    def _add_mlc_stat(self, mac_directory, data_directory, exec_dir, index):
        root = os.getcwd()
        list_file=['QLT_SUP', 'QLI_SUP', 'QLT_INF', 'QLI_INF', 'HLT_SUP', 'HLI_SUP', 'HLT_INF', 'HLI_INF', 
                   'QLT_SUP180', 'QLI_SUP180', 'QLT_INF180', 'QLI_INF180', 'HLT_SUP180', 'HLI_SUP180', 'HLT_INF180', 'HLI_INF180']
        
        list_mac_file=['QLT', 'QLI', 'HLT', 'HLI', 'QLT180', 'QLI180', 'HLT180', 'HLI180', 'outboard', 'outboard60', 'outboard_180', 'outboard60_180']  
            
        shutil.copyfile(UtilsMac+'Xmlc.macX',data_directory+'/mlc.mac')
        #fileToWrite=fileinput.FileInput(data_directory+'/mlc.mac', inplace=1)
        with open(data_directory+'/mlc.mac', 'a') as file:
            for mac_file in list_mac_file:
                file.write("\n"+" /control/execute "+ exec_dir + "/" + mac_file + ".mac"+"\n")


        shutil.copyfile(UtilsMac+'outboard.mac',data_directory+'/outboard.mac')
        shutil.copyfile(UtilsMac+'outboard60.mac',data_directory+'/outboard60.mac')
        shutil.copyfile(UtilsMac+'outboard_180.mac',data_directory+'/outboard_180.mac')
        shutil.copyfile(UtilsMac+'outboard60_180.mac',data_directory+'/outboard60_180.mac')
        
        for mac_file in list_mac_file:
            shutil.copyfile(UtilsMac+mac_file+'.mac',data_directory+'/'+mac_file+'.mac')
            fileToWrite=fileinput.FileInput(data_directory+'/'+mac_file+'.mac', inplace=1)
            for line in fileToWrite:
                line=line.replace("DIR", exec_dir)
                print(line)
            fileToWrite.close()

        with open(mac_directory+'/main.mac', 'a') as file:
            file.write("/control/execute " + exec_dir + "/mlc.mac"+"\n")

        for file in list_file:
                shutil.copyfile(UtilsPlacements+'precise_'+file+'.placementsXXX',data_directory+'/precise_'+file+'.placements')
            
        #for i in range(0, self._get_nb_index()):
        self.Beam._compute_mlc_position_fromC(root+ '/temp/'+str(index)+'-'+self._get_simu_name()+'_mlc.mlc')
        Gammora_print._display_working_state("Computing MLC positions "+str(index)+"/"+str(self.Beam._get_beam_nb_cpi()-1))
        for file in list_file:
            shutil.copyfile(UtilsPlacements+'precise_'+file+'.placementsXXX',data_directory+'/precise_'+file+'.placements')
            with open(data_directory+'/precise_'+file+'.placements', 'a') as f, open(root+'/'+file+'.dat', 'r') as data :
                    d=data.readlines()
                    for dd in d:
                    #print('len', len(d))
                    #print(type(d))
                        f.write(str(dd))
                        #f.write('\n')
# ++ MLC : dynamic splitting

    def _add_mlc_dyn(self, mac_directory, data_directory, exec_dir):
        root = os.getcwd()
        list_file=['QLT_SUP', 'QLI_SUP', 'QLT_INF', 'QLI_INF', 'HLT_SUP', 'HLI_SUP', 'HLT_INF', 'HLI_INF', 
                   'QLT_SUP180', 'QLI_SUP180', 'QLT_INF180', 'QLI_INF180', 'HLT_SUP180', 'HLI_SUP180', 'HLT_INF180', 'HLI_INF180']
        
        list_mac_file=['QLT', 'QLI', 'HLT', 'HLI', 'QLT180', 'QLI180', 'HLT180', 'HLI180', 'outboard', 'outboard60', 'outboard_180', 'outboard60_180']  
            
        shutil.copyfile(UtilsMac+'Xmlc.macX',data_directory+'/mlc.mac')
        #fileToWrite=fileinput.FileInput(data_directory+'/mlc.mac', inplace=1)
        with open(data_directory+'/mlc.mac', 'a') as file:
            for mac_file in list_mac_file:
                file.write("\n"+" /control/execute "+ exec_dir + "/" + mac_file + ".mac"+"\n")


        shutil.copyfile(UtilsMac+'outboard.mac',data_directory+'/outboard.mac')
        shutil.copyfile(UtilsMac+'outboard60.mac',data_directory+'/outboard60.mac')
        shutil.copyfile(UtilsMac+'outboard_180.mac',data_directory+'/outboard_180.mac')
        shutil.copyfile(UtilsMac+'outboard60_180.mac',data_directory+'/outboard60_180.mac')
        
        
        for mac_file in list_mac_file:
            shutil.copyfile(UtilsMac+mac_file+'.mac',data_directory+'/'+mac_file+'.mac')
            fileToWrite=fileinput.FileInput(data_directory+'/'+mac_file+'.mac', inplace=1)
            for line in fileToWrite:
                line=line.replace("DIR", exec_dir)
                print(line)
            fileToWrite.close()

        with open(mac_directory, 'a') as file:
            file.write("/control/execute " + exec_dir + "/mlc.mac"+"\n")

        for file in list_file:
                shutil.copyfile(UtilsPlacements+'precise_'+file+'.placementsXXX',data_directory+'/precise_'+file+'.placements')

        shutil.copyfile(UtilsPlacements+'precise_'+file+'.placementsXXX',data_directory+'/precise_'+file+'.placements')   
        for i in range(0, self.Beam._get_beam_nb_cpi()):
            Gammora_print._display_working_state("Computing MLC positions "+str(i)+"/"+str(self.Beam._get_beam_nb_cpi()-1))
            self.Beam._compute_mlc_position_fromC(root+'/temp/'+str(i)+'-'+self._get_simu_name()+'_mlc.mlc')
            for file in list_file:
                
                with open(data_directory+'/precise_'+file+'.placements', 'a') as f, open(root+'/'+file+'.dat', 'r') as data :
                    d=data.readlines()
                    for dd in d:
                        ddd=dd.split(' ')
                        ddd[0]=str(float(i))
                        for val in ddd:
                            f.write(val + ' ')
                    f.write('\n')
        print("")

# Source
#--------

# + IAEA phsp (Varian)
    def _add_varian_phase_space_source_stat_split(self, cpi, mac_directory, data_directory, exec_dir):
        """
        add varian phase space source for phsp simulation
        The total number of particle for one energy is divided by the number of control index modulated to the dose rate
        """
        root = os.getcwd()
        data_phsp=pd.read_csv(root+'/utils/source/data_varian_phsp.csv')

        if self.Beam._get_manual_nb_part() == True:
            total_number_of_primaries=self.Beam._get_iaea_nb_part()
            #print(total_number_of_primaries)
            number_of_phsp_file=data_phsp['index'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[-1]
            i = cpi % (number_of_phsp_file+1)
            number_of_primaries=int(int(total_number_of_primaries/self.Beam._get_nb_index())*self.Beam._get_dose_rate()[cpi])
        else:
            total_number_of_primaries=data_phsp['total_nb_part_energy'].loc[data_phsp['energy'] == self.Beam._get_energy()].to_numpy()[0]
            #print(total_number_of_primaries)
            number_of_phsp_file=data_phsp['index'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[-1]
            i = cpi % (number_of_phsp_file+1)

            if self.Beam._get_nb_index() <= number_of_phsp_file:
                number_of_primaries = data_phsp['nb_part_phsp'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[i]*self.Beam._get_dose_rate()[cpi]

            if self.Beam._get_nb_index() > number_of_phsp_file:
                number_of_primaries=int(int(total_number_of_primaries/self.Beam._get_nb_index())*self.Beam._get_dose_rate()[cpi])
        
        with open(mac_directory, 'a') as file:                 
            source1='/gate/source/addSource MyBeam phaseSpace'
            file.write("\n"+source1)
                
        phsp_name=data_phsp['file_name'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[i]

        if self._get_calmip() == True:
            dir_phsp = self._get_phsp_dir1()

        if self._get_local() == True:
            dir_phsp = data_directory

        with open(mac_directory, 'a') as file:
            source2='/gate/source/MyBeam/addPhaseSpaceFile '+dir_phsp+'/'+phsp_name
            file.write("\n"+source2)

        with open(mac_directory, 'a') as file:    
            primaries='/gate/application/setTotalNumberOfPrimaries '+ str(int(number_of_primaries))
            file.write("\n"+primaries+"\n")
                
        with open(mac_directory, 'a') as file:       
            attach='/gate/source/MyBeam/attachTo inPhSpVarian'          
            file.write(attach+"\n")
        with open(mac_directory, 'a') as file:       
            generator='/gate/random/setEngineName MersenneTwister'
            file.write(generator+"\n")
            seed='/gate/random/setEngineSeed auto'
            file.write(seed+"\n")


    def _add_varian_phase_space_source_dyn_split(self, cpi, mac_directory, data_directory, exec_dir):
        """
        add varian phase space source for phsp simulation
        The total number of particle for one energy is divided by the number of control index modulated to the dose rate
        """
        root = os.getcwd()
        data_phsp=pd.read_csv(root+'/utils/source/data_varian_phsp.csv')

        #total_number_of_primaries=data_phsp['total_nb_part_energy'].loc[data_phsp['energy'] == self._get_energy()].to_numpy()[0]
        number_of_phsp_file=data_phsp['index'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[-1]
            
        with open(mac_directory, 'a') as file:                 
            source1='/gate/source/addSource MyBeam phaseSpace'
            file.write("\n"+source1)
            
        i = cpi % (number_of_phsp_file+1)
        phsp_name=data_phsp['file_name'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[i]

        if self._get_calmip() == True:
            dir_phsp = self._get_phsp_dir1()

        if self._get_local() == True:
            dir_phsp = data_directory

        with open(mac_directory, 'a') as file:
            source2='/gate/source/MyBeam/addPhaseSpaceFile '+dir_phsp+'/'+phsp_name
            file.write("\n"+source2)
            line='/gate/application/readTimeSlicesIn '+exec_dir+'/myTime.timeslices'
            file.write("\n"+line)

        with open(mac_directory, 'a') as file:  
            primaries='/gate/application/readNumberOfPrimariesInAFile '+exec_dir+'/primary.dat'
            file.write("\n"+primaries+"\n")                    

            with open(mac_directory, 'a') as file:       
                attach='/gate/source/MyBeam/attachTo inPhSpVarian'          
                file.write("\n"+attach+"\n")
            with open(mac_directory, 'a') as file:       
                generator='/gate/random/setEngineName MersenneTwister'
                file.write(generator+"\n")
                seed='/gate/random/setEngineSeed auto'
                file.write(seed+"\n")
# + GAGA phsp
    def _add_gaga_phase_space_source(self, cpi, mac_directory, data_directory, exec_dir):
            """
            add a gaga source see: https://github.com/OpenGATE/GateContrib/tree/master/dosimetry/gaga-phsp
            To use with Gate v9.0
            The source is obtained with a trained Generative Adversial Network (GAN) for 6X, 6FFF, 10X, 10FFF
            Particle are stored just above the jaws
            """
            root = os.getcwd()
            shutil.copyfile(root+'/utils/source/gaga/'+self.Beam._get_energy()+'.json', data_directory+'/'+self.Beam._get_energy()+'.json')
            shutil.copyfile(root+'/utils/source/gaga/'+self.Beam._get_energy()+'.pt', data_directory+'/'+self.Beam._get_energy()+'.pt')
            if self._get_split_type() == 'stat':
                nb_primaries=int((self.Beam._get_gaga_nb_part()/self.Beam._get_nb_index())*self.Beam._get_dose_rate()[cpi])

            elif self._get_split_type() == 'dyn':   # for the moment -> to fix nb part must be fix with primary.dat file (not working at the moment with gaga)
                nb_primaries=int(self.Beam._get_gaga_nb_part()/self.Beam._get_nb_index())
                #print(self._get_dose_rate()[cpi])

            if self._get_local() == True:
                self._set_phsp_dir1(data_directory)
                dir_phsp = data_directory

            if self._get_calmip() == True:
                dir_phsp = self._get_phsp_dir1()

            with open(mac_directory, 'a') as file:                 
                source1='/gate/source/addSource MyBeam phaseSpace'
                source2='/gate/source/MyBeam/addPhaseSpaceFile '+dir_phsp+'/'+self.Beam._get_energy()+'.pt'
                source3='/gate/source/MyBeam/setParticleType gamma'
                source4='/gate/source/MyBeam/setPytorchParams '+dir_phsp+'/'+self.Beam._get_energy()+'.json'
                source5='/gate/source/MyBeam/setPytorchBatchSize 1000000'
                source6='/gate/source/MyBeam/attachTo gaga_vol'
                source7='/gate/source/MyBeam/useRandomSymmetry true'
                source8='/gate/source/MyBeam/ignoreWeight true'
                generator='/gate/random/setEngineName MersenneTwister'
                seed='/gate/random/setEngineSeed auto'
                if self._get_split_type() == 'stat':
                    part='/gate/application/setTotalNumberOfPrimaries '+str(nb_primaries)
    
                if self._get_split_type() == 'dyn':
                    part='/gate/application/setTotalNumberOfPrimaries '+str(nb_primaries)
                    #part='/gate/application/readNumberOfPrimariesInAFile '+exec_dir+'/primary.dat' # To fix (gaga do not work with read in a file, necessary to modulate dose rate)
                    line='/gate/application/readTimeSlicesIn '+exec_dir+'/myTime.timeslices'
                
                file.write("\n"+source1+"\n")
                file.write(source2+"\n")
                file.write(source3+"\n")
                file.write(source4+"\n")
                file.write(source5+"\n")
                file.write(source6+"\n")
                file.write(source7+"\n")
                file.write(source8+"\n")
                file.write(generator+"\n")
                file.write(seed+"\n")
                if self._get_split_type() == 'dyn':
                    file.write(line+"\n")
                file.write(part+"\n")

# + Primary.dat file # To Do TO CHECK

    def _create_primary_file(self, data_directory):
        root = os.getcwd()
        

        if self.Beam._get_manual_nb_part() == True:

            data_phsp=pd.read_csv(root+'/utils/source/data_varian_phsp.csv')

            if self.Beam._get_source_iaea() == True:
                total_number_of_primaries=self.Beam._get_iaea_nb_part()
            if self.Beam._get_source_gaga() == True:
                total_number_of_primaries=self.Beam._get_gaga_nb_part()

            number_of_phsp_file=data_phsp['index'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[-1]
            primaries_per_simu=total_number_of_primaries/self.Beam._get_nb_index()

            with open(data_directory+'/primary.dat', 'a') as file:
                file.write("#Number of part per run"+"\n")
                for cpi in range(0,self.Beam._get_beam_nb_cpi()):
                    i = cpi % (number_of_phsp_file+1)
                    if self.Study._get_from_patient() == True and self.Beam._get_source_iaea() == True:
                        if primaries_per_simu >= data_phsp['nb_part_phsp'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[i]:
                            Gammora_print._error_config('Number of Index', str(self.Beam._get_nb_index()), ['auto', 'at least ' + str(self.Beam._get_beam_nb_cpi()-1)])
                            exit()        
                        #raise ValueError

                    elif self.Study._get_from_scratch() == True and self.Beam._get_source_iaea() == True:
                        nb_part_in_this_phsp=data_phsp['nb_part_phsp'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[i]
                        if primaries_per_simu >= nb_part_in_this_phsp:
                            #Gammora_print._warning('Number of particule per Simu is too important')
                            #Gammora_print._error_config('Number of particule per Simu is too important', str(self.Beam._get_nb_index()), ['Increase Number of Index', 'Define manually number of particule'])
                            number_of_primaries=int(int(nb_part_in_this_phsp/self.Beam._get_beam_nb_cpi())*self.Beam._get_dose_rate()[cpi])
                        else:
                            number_of_primaries=int(int(primaries_per_simu/self.Beam._get_beam_nb_cpi())*self.Beam._get_dose_rate()[cpi])
                    else:
                        number_of_primaries=int(int(primaries_per_simu/self.Beam._get_beam_nb_cpi())*self.Beam._get_dose_rate()[cpi])
                    if cpi == self.Beam._get_beam_nb_cpi()-1:
                        file.write(str(int(number_of_primaries)))
                    else:
                        file.write(str(int(number_of_primaries))+"\n")


        else:    
            
            data_phsp=pd.read_csv(root+'/utils/source/data_varian_phsp.csv')
            total_number_of_primaries=data_phsp['total_nb_part_energy'].loc[data_phsp['energy'] == self.Beam._get_energy()].to_numpy()[0]
            number_of_phsp_file=data_phsp['index'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[-1]
            primaries_per_simu=total_number_of_primaries/self.Beam._get_nb_index()

            with open(data_directory+'/primary.dat', 'a') as file:
                file.write("#Number of part per run"+"\n")
                for cpi in range(0,self.Beam._get_beam_nb_cpi()):
                    i = cpi % (number_of_phsp_file+1)
                    if self.Study._get_from_patient() == True and self.Beam._get_source_iaea() == True:

                        if primaries_per_simu >= data_phsp['nb_part_phsp'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[i]:
                            Gammora_print._error_config('Number of Index', str(self.Beam._get_nb_index()), ['auto', 'at least ' + str(self.Beam._get_beam_nb_cpi()-1)])
                            exit()
                        else:
                            number_of_primaries=int(int(primaries_per_simu/self.Beam._get_beam_nb_cpi())*self.Beam._get_dose_rate()[cpi])        

                    elif self.Study._get_from_scratch() == True and self.Beam._get_source_iaea() == True:
                        nb_part_in_this_phsp=data_phsp['nb_part_phsp'].loc[data_phsp['energy']==self.Beam._get_energy()].to_numpy()[i]
                        if primaries_per_simu >= nb_part_in_this_phsp:
                            Gammora_print._warning('Number of particule per Simu is too important', [])
                            Gammora_print._error_config('Number of particule per Simu is too important :', str(primaries_per_simu), ['Increase Number of Index', 'Define manually number of particle'])
                            exit()
                            #number_of_primaries=int(int(nb_part_in_this_phsp/self.Beam._get_beam_nb_cpi())*self.Beam._get_dose_rate()[cpi])
                        else: 
                            number_of_primaries=int(int(primaries_per_simu/self.Beam._get_beam_nb_cpi())*self.Beam._get_dose_rate()[cpi])
                    else:
                        number_of_primaries=int(int(primaries_per_simu/self.Beam._get_beam_nb_cpi())*self.Beam._get_dose_rate()[cpi])

                    if cpi == self.Beam._get_beam_nb_cpi()-1:
                        file.write(str(int(number_of_primaries)))
                    else:
                        file.write(str(int(number_of_primaries))+"\n")

# + Reduced phase space source
    def _add_reduced_phase_space_source(self, cpi, mac_directory, data_directory):
        """
        add reduce phase space source for clinic simulation 
        """
        if self._get_calmip() == True:
            dir_phsp = self._get_phsp_dir1()+'/'+self._get_simu_name()
        if self._get_local() == True:
            dir_phsp = root+'/output/'+self.Study._get_study_name()+'/'+self._get_simu_name()+'/phsp/output/'+str(cpi)
        #phsp_name = str(cpi)+'-'+self._get_simu_name()+'.IAEAphsp'
        
        #number_of_primaries=N*recycling
        with open(mac_directory, 'a') as file:                 
            source1='/gate/source/addSource MyBeam phaseSpace'
            file.write("\n"+source1)
        with open(mac_directory, 'a') as file:
            if self._get_calmip() == True:
                if self._get_split_type() == 'stat':
                    #source2='/gate/source/MyBeam/addPhaseSpaceFile '+'/tmpdir/' +self._get_user()+'/input/'+self.Study._get_study_name()+'/'+self._get_simu_name()+'/phsp/output/'+str(cpi)+'/myIAEA.IAEAphsp'
                    source2='/gate/source/MyBeam/addPhaseSpaceFile '+'/tmpdir/' +self._get_user()+'/input/'+self.Study._get_study_name()+'/'+self._get_simu_name()+'/phsp/output/'+str(cpi)+'/myIAEA.root'
                if self._get_split_type() == 'dyn':
                    source2='/gate/source/MyBeam/addPhaseSpaceFile '+'/tmpdir/' +self._get_user()+'/input/'+self.Study._get_study_name()+'/'+self._get_simu_name()+'/phsp/output/'+str(cpi)+'/myIAEA.root'
            if self._get_local() == True:
                #source2='/gate/source/MyBeam/addPhaseSpaceFile '+dir_phsp+'/'+phsp_name
                source2='/gate/source/MyBeam/addPhaseSpaceFile '+dir_phsp+'/myIAEA.root'
            file.write("\n"+source2)
        with open(mac_directory, 'a') as file:       
            primaries='/gate/application/setTotalNumberOfPrimaries NB_PRIM'          
            file.write("\n"+primaries+"\n")
        with open(mac_directory, 'a') as file:       
            attach='/gate/source/MyBeam/attachTo outPhSpCylinder'          
            file.write(attach+"\n")
        with open(mac_directory, 'a') as file:       
            generator='/gate/random/setEngineName MersenneTwister'
            file.write(generator+"\n")
            seed='/gate/random/setEngineSeed auto'
            file.write(seed+"\n")


# + Time slice

    def _create_time_slice_file(self, data_directory):

        with open(data_directory+'/myTime.timeslices', 'a') as file:
            file.write("Time s"+"\n")
            for i in range(0, self.Beam._get_beam_nb_cpi()+1):
                file.write(str(float(i))+"\n")
            #file.write("\n")

  
#=======================
# # Functions for GammoraSimu Object
#=======================

# Display info on simulation
#--------
    def _show_info(self):
        print()
        print()
        print("***************************")
        print()
        print("* Simulation name: ", self._get_simu_name())
        print("* Find macros in: ", self._get_local_output_dir())
        if self._get_local() == True:
            print("* Local Simulation")
        if self._get_calmip() == True:
            print("* CALMIP Simulation")
            print(" *   Automatic Sending: ", self._get_sending())
            print(" *   Automatic Launching: ", self._get_launching())
            print(" *   Calmip User: ", self._get_user())
            print(" *   Input Directory: ", self._get_input_dir())
            print(" *   PHSP Directory: ", self._get_phsp_dir1())
            print(" *   Output Directory: ", self._get_output_dir())
            
        print()
        print("------ Settings ------------")
        print()
        print("* Visualization: ", self._get_visualization())
        if self._get_visualization() == True:
            if self._get_visualization_mode() == 1:
                print("* Visualization Mode: LINAC")
                print("* Visualization Mode: MLC")
        print("* Material: ", self._get_material())
        if self._get_material() == True:
            print("* Material File: ", self._get_material_name())
        print("* Physics: ", self._get_physics())
        if self._get_physics() == True:
            print("* Physics File: ", self._get_physics_name().split('/')[-1])
        print("* Number of Index: ", self._get_nb_index())
        print("* Treatment Head simulation: ", self._get_head_part_siumulation())
        if self._get_head_part_siumulation() == True:
            print(" *   Head Geometry: ")
            print("     *   Gantry Angle:", self._get_gantry_angle(), "°")
            print("     *   Collimator Angle: ", self._get_colli_angle(), "°")
            print("     *   X1 position: ", self._get_x1(), "mm")
            print("     *   X2 position: ", self._get_x2(), "mm")
            print("     *   Y1 position: ", self._get_y1(), "mm")
            print("     *   Y2 position: ", self._get_y2(), "mm")
            print("     *   MLC: ", self._get_mlc())
        print("* Patient/Phantom simulation: ", self._get_patient_part_siumulation())
        if self._get_patient_part_siumulation()== True:
            print("     *   Phantom: ", self._get_phantom())
            if self._get_phantom() == True:
                print("     * Phantom Name: ", self._get_phantom_name())
                #print("     * Phantom Motion: ", self._get_phantom_motion(), " DO NOT WORK YET")
                #if self._get_phantom_motion() == True:
                    #print("     *   Phantom Motion File: ", self._get_phantom_motion_name(), " DO NOT WORK YET")
            print("     *   Patient CT: ", self._get_patient_ct())
            if self._get_patient_ct() == True:
                print("     * Patient CT Name: ", self._get_patient_ct_name())
        print("* Actor: ")
        if self._get_head_part_siumulation() == True:
            print(" *   PHSP Actor: ", self._get_phsp_actor())
            if self._get_phsp_actor() == True:
                print(" *   PHSP Actor File name: ", self._get_phsp_actor_name())
        if self._get_patient_part_siumulation() == True:
            print(" *   Patient Actor: ", self._get_patient_actor())
            if self._get_patient_actor() == True:
                print(" *   Patient Actor File name: ", self._get_patient_actor_name())
        print("* Source: ", self._get_source())
        if self._get_source() == True:
            if self._get_head_part_siumulation() == True:
                if self._get_source_iaea() == True:
                    print(" *   Source Type: IAEA phase space")
                print(" *   Energy: ", self._get_energy())
            if self._get_patient_part_siumulation() == True:
                print(" *   Using of Reduce Phase space: True")
                print(" *   Reduced Phase Space Base Filename: ", self._get_reduced_source_name())
                print(" *   Recycling: ", self._get_recycling())
                
        print()
        print("***************************")
        print()



# For cluster computation
#--------

# + Launcher CALMIP
    def _create_launcher_calmip(self, directory, out):
        root = os.getcwd()

        if out == 'phsp':
            shutil.copyfile(root+'/utils/template/Xlaunch_gate_phsp.bashX', directory+'/launch_gate.bash')
        elif out == 'clinic':
            shutil.copyfile(root+'/utils/template/Xlaunch_gate_clinic.bashX', directory+'/launch_gate.bash')
        else : 
            print("please precise type 'phsp' or 'clinic' for create calmip launcher")
            raise TypeError


        file=fileinput.FileInput(directory+'/launch_gate.bash', inplace=1)
        for line in file:
            line=line.replace("job_name_tag", str(self._get_simu_name()))
            line=line.replace("job_out_dir", str(out))
            line=line.replace("n_core_tag", str(self.Beam._get_nb_index()+1))
            line=line.replace("n_node_tag",str(int((self.Beam._get_nb_index()/36))+1))
            if self._get_head_part_siumulation() == True and  self.Beam._get_source() ==True:
                if self.Beam._get_source_iaea()  == True:
                    tot_part=self.Beam._get_nb_part_tot_varian()[0]
                if self.Beam._get_source_gaga() == True:
                    tot_part=self.Beam._get_gaga_nb_part()
                line=line.replace("tot_part_tag", str(tot_part))
                line=line.replace("time_tag",str(int(tot_part/(8500*3600*self.Beam._get_nb_index()))+1))
            else:
                line=line.replace("time_tag","08")
            line=line.replace("user_tag", str(self._get_user()))
            if self._get_head_part_siumulation() == True and  self.Beam._get_source() ==True:
                line=line.replace("tot_part_tag", str(tot_part))
            print(line)

# +  Bash script to set number of particle of patient part simulation 
    def _create_macros_set_nb_part_reduced(self, directory, the_dir):
        root = os.getcwd()
        shutil.copyfile(root+'/utils/template/Xset_nb_part_reduced_phsp.bashX', directory+'/set_nb_reducued_phsp.bash')
        file=fileinput.FileInput(directory+'/set_nb_reducued_phsp.bash', inplace=1)
        for line in file:
            line=line.replace("ReCyCl", str(self.Beam._get_recycling()))
            line=line.replace("the_dir", the_dir)
            print(line)

    def _create_macros_set_nb_part_reduced_from_root(self, directory, the_dir):
        root = os.getcwd()

        if self._get_calmip() == True:
            shutil.copyfile(root+'/utils/template/Xset_nb_part_reduced_phsp_from_root_calmip.bashX', directory+'/set_nb_reducued_phsp.bash')
        if self._get_local() == True:
            shutil.copyfile(root+'/utils/template/Xset_nb_part_reduced_phsp_from_root_local.bashX', directory+'/set_nb_reducued_phsp.bash')

        shutil.copyfile(root+'/utils/source/read_root.py', directory+'/read_root.py')
        file=fileinput.FileInput(directory+'/set_nb_reducued_phsp.bash', inplace=1)
        for line in file:
            line=line.replace("ReCyCl", str(self.Beam._get_recycling()))
            line=line.replace("the_dir", the_dir)
            line=line.replace("Nsimu", str(self.Beam._get_nb_index()))
            print(line)


class GammoraPatientSimu(GammoraSimu):

# Declaration of paths    
    global root
    global UtilsMac
    global UtilsPlacements
    global UtilsMacActor
    global UtilsMacPhantom
    
    root = os.getcwd()
    UtilsPlacements=root+'/utils/placement_template/'
    UtilsMac=root+'/utils/mac/mac_template/'
    UtilsMacActor=root+'/utils/mac/actor/'
    UtilsMacPhantom=root+'/utils/mac/phantom/'

# Initialisation

    def __init__(self, config, GammoraBeam, GammoraStudy):
        
# Declaration of general attibut

        self.Beam = GammoraBeam 
        self.Study = GammoraStudy
        self._set_simu_name(GammoraBeam)
        self._set_split_type(GammoraBeam)
        self._set_head_part_siumulation(GammoraBeam)
        self._set_patient_part_siumulation(GammoraBeam)

# Define local input/output direcories 
        self._set_local_output_dir(root+'/output/'+str(self.Study._get_study_name())+'/'+self._get_simu_name())
        if GammoraStudy._get_from_patient() == True:
            self._set_local_input_dir(root+'/input/patient/'+str(GammoraStudy._get_study_input_name()))



# Computing choice 
        Gammora_print._separator2()
        Gammora_print._title("Computing")
        if config['EXECUTE_ON_CLUSTER'] == '0':
            self._set_local(True)
            Gammora_print._title2("Local simulation")
        if config['EXECUTE_ON_CLUSTER'] == '3':
            self._set_calmip(True)
            Gammora_print._title2("CALMIP simulation")

        if self._get_calmip() == True:

            # Default config computation
            config_default_patient = {} # To do : repeated in GammoraPatientBeam (config_default)

            config_default_patient['CALMIP_USER']='leste'
            config_default_patient['AUTO_SENDING']=False
            config_default_patient['AUTO_LAUNCHING']=False

            self._set_user(config_default_patient['CALMIP_USER'])
            #self._set_sending(config_default_patient['AUTO_SENDING']) # To do not workin yet
            #self._set_launching(config_default_patient['AUTO_LAUNCHING'])  # To do not workin ye
            self._set_input_dir('/tmpdir/'+self._get_user()+'/input/'+str(GammoraStudy._get_study_name())+'/'+self._get_simu_name())
            self._set_output_dir('/tmpdir/'+self._get_user()+'/input/'+str(GammoraStudy._get_study_name())+'/'+self._get_simu_name()+'/output')
            self._set_phsp_dir1('/tmpdir/'+self._get_user()+'/phsp')
            Gammora_print._title2("CALMIP user: "+ str(self._get_user()))
            
        if self._get_local() == True:
            self._set_input_dir(self._get_local_output_dir())
        
# Create main simulations arrchitecture
 
# Create study dir in output       

        try:
            os.makedirs(self._get_local_output_dir())
        except FileExistsError:
            shutil.rmtree(self._get_local_output_dir())
            os.makedirs(self._get_local_output_dir())
            pass

# Create dir for Head Part Simulation

        if self._get_head_part_siumulation() == True:
            try: 
                self._set_phsp_dir(self._get_local_output_dir()+'/phsp')
                self._set_phsp_data_dir(self._get_phsp_dir()+'/data')
                self._set_phsp_mac_dir(self._get_phsp_dir()+'/mac')
                os.mkdir(self._get_phsp_dir())
                os.mkdir(self._get_phsp_mac_dir())
                os.mkdir(self._get_phsp_data_dir())
                if self._get_local() == True:
                    os.mkdir(self._get_phsp_dir()+'/output')
            except FileExistsError:
                exit()

# Create dir for Patient Part Simulation

        if self._get_patient_part_siumulation() == True:

            try:
                self._set_clinic_dir(self._get_local_output_dir()+'/clinic')
                self._set_clinic_data_dir(self._get_clinic_dir()+'/data')
                self._set_clinic_mac_dir(self._get_clinic_dir()+'/mac')
                os.mkdir(self._get_clinic_dir())
                os.mkdir(self._get_clinic_mac_dir())
                os.mkdir(self._get_clinic_data_dir())
                if self._get_local() == True:
                    os.mkdir(self._get_clinic_dir()+'/output')
            except FileExistsError:
                pass

# Main Macros Generator
 
    def _generate_macros(self):

        if self._get_split_type() == 'stat':
            self._generate_macros_stat_split()

        if self._get_split_type() == 'dyn':
            self._generate_macros_dyn_split()
        
# Dynamic splitting Macro Generator
    def _generate_macros_dyn_split(self):
        """
        generate gate macros from rt plan simulations
        One simulation for the all the geometry configuration
        use time slice for gate
        """

        Gammora_print._title2('Generating Gate Macros for : ' + self._get_simu_name())
        print("")
        
# Generate PHSP macros
        
        if self._get_head_part_siumulation() == True:


            # define path to be written in GATE macros 
            if self._get_calmip() == True:
                exec_dir='/tmpdir/'+self._get_user()+'/input/'+self.Study._get_study_name()+'/'+self._get_simu_name()+'/phsp/data'
            
            if self._get_local() == True:
                exec_dir=self._get_phsp_data_dir()

# + General
# ++ Create main.mac file
            self._create_main_mac_file(self._get_phsp_mac_dir())
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Verbose')
# ++ Verbose
            self._add_verbose(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

# ++ Visualization
            if self.Beam._get_visualization() == True:
                    self._add_visualization(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
# ++ Material
            if self.Beam._get_material() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Material')
                self._add_material_tab(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

# + Geometry 1 : Definition of initial geometry 

# ++ World, treatment head and killBox

            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Geometry 1')
            self._add_world_geometry(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._add_treatment_head(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._add_kill_box(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

# ++ Phase Space volumes
            self._add_phase_space_volume(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            
# + Counter           
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Counter')
            self._add_counter(self._get_phsp_mac_dir(), self._get_phsp_data_dir())

# + Physics
            if self.Beam._get_physics() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Physics List')
                self._add_physics(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

# + PHSP actor

            if self.Beam._get_phsp_actor() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Actor')
                self._add_phsp_actor(self.Beam._get_phsp_actor_name(), self._get_phsp_mac_dir(), self._get_phsp_data_dir())

# + Geometry 2 : Definition of Position of Head Component

# + Gantry
            self._apply_gantry_rot_dyn(self._get_phsp_mac_dir()+'/main.mac', self._get_phsp_data_dir(), exec_dir)

# + Colli            
            self._apply_colli_rot(self.Beam._compute_colli_position(self.Beam._get_colli_angle()[0]),  self._get_phsp_mac_dir()+'/main.mac')
            #jaws_data=self._compute_jaws([self._get_x1()[i], self._get_x2()[i], self._get_y1()[i], self._get_y2()[i]])
# + Jaws            
            self._apply_jaws_dyn(self._get_phsp_mac_dir()+'/main.mac', self._get_phsp_data_dir(), exec_dir)
# + MLC
            if self.Beam._get_mlc() == True:                                    
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'MLC position: ')
                self._add_mlc_dyn(self._get_phsp_mac_dir()+'/main.mac', self._get_phsp_data_dir(), exec_dir)

# + Time Slice file
            self._create_time_slice_file(self._get_phsp_data_dir())

            print("")
            print("")

# + Create index architecture for job splitting 

            for i in range(0, self.Beam._get_nb_index()):
                try:
                    mac_cpi=self._get_phsp_mac_dir()+'/'+str(i)
                    os.mkdir(mac_cpi)
                    if self._get_local() == True:
                        os.mkdir(self._get_phsp_dir()+'/output/'+str(i))
                except FileExistsError:
                    pass

                if self._get_calmip() == True:
                    exec_dir_cpi='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/phsp/data/'+str(i)
        
                if self._get_local() == True:
                    exec_dir_cpi=self._get_phsp_data_dir()+'/'+str(i)

                shutil.copyfile(self._get_phsp_mac_dir()+'/main.mac', mac_cpi+'/main.mac')

# + Display                
                Gammora_print._display_working_state("Creating TrueBeam head simualtion "+str(i)+"/"+str(self.Beam._get_nb_index()-1))

# + Initialization command
            
                self._decorate(mac_cpi+'/main.mac', 'Initialize')
                self._add_initialize_command(mac_cpi+'/main.mac')

# + Source
                if self.Beam._get_source() == True:
                    self._decorate(mac_cpi+'/main.mac', 'Source')
                    if self.Beam._get_source_iaea() == True:
                        self._add_varian_phase_space_source_dyn_split(i, mac_cpi+'/main.mac', self._get_phsp_data_dir(), exec_dir)
                        if i == 0:
                            self._create_primary_file(self._get_phsp_data_dir())
                    if self.Beam._get_source_gaga() == True:
                        if i == 0:
                            self._create_primary_file(self._get_phsp_data_dir())
                        self._add_gaga_phase_space_source(i, mac_cpi+'/main.mac', self._get_phsp_data_dir(), exec_dir)

# + Start Command
                self._decorate(mac_cpi+'/main.mac', 'Start Gate')
                self._add_run_command(mac_cpi+'/main.mac')
            print("")
# + Create Launcher
            if self._get_calmip() == True:
                self._create_launcher_calmip(self._get_phsp_dir(), 'phsp')    
            
            os.remove(self._get_phsp_mac_dir()+'/main.mac')

# No Head Part Simulation            
        else:
            Gammora_print._title2("Head part simulated is disabled")

        
# Generate CLINIC macros

        if self._get_patient_part_siumulation() == True:

# + General
            if self._get_calmip() == True:
                exec_dir='/tmpdir/'+self._get_user()+'/input/'+self.Study._get_study_name()+'/'+self._get_simu_name()+'/clinic/data'
            
            if self._get_local() == True:
                exec_dir=self._get_clinic_data_dir()
# ++ Main.mac file
            self._create_main_mac_file(self._get_clinic_mac_dir())
# ++ Verbose
            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Verbose')
            self._add_verbose(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# ++ Visualization
            if self.Beam._get_visualization() == True:
                    self._add_visualization(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# ++ Materail
            if self.Beam._get_material() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Material')
                self._add_material_tab(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Geometry 1 : Definition of initial geometry 
            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Geometry 1')
            self._add_world_geometry(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
            self._add_only_cylinder_phase_space_volume(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Patient CT
            if self.Study._get_from_patient() == True:
                if self.Beam._get_patient_ct()== True:
                    self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Patient CT')
                    self._add_patient_ct(self.Beam._get_patient_ct_name(), self.Beam._get_isocenter_position(), self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Treatment Couch
                if self.Beam._get_couch() == True:
                    self._add_stl_couch(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
                
# + Phantom            
            if self.Beam._get_phantom() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Phantom')
                self._add_phantom(self.Beam._get_phantom_name(), self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Physics            
            if self.Beam._get_physics() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Physics List')
                self._add_physics(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)


# + Counter
            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Counter')          
            self._add_counter(self._get_clinic_mac_dir(), self._get_clinic_data_dir())

# + Patient Actor
            if self.Beam._get_patient_actor() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Actor')   
                self._add_patient_actor(self.Beam._get_patient_actor_name(), self._get_clinic_mac_dir(), self._get_clinic_data_dir())
            print("")
            
# + Create index architecture for job splitting
            for i in range(0, self.Beam._get_nb_index()):

                try:
                    data_cpi=self._get_clinic_data_dir()+'/'+str(i)
                    mac_cpi=self._get_clinic_mac_dir()+'/'+str(i)
                    os.mkdir(data_cpi)
                    os.mkdir(mac_cpi)
                    if self._get_local() == True:
                        os.mkdir(self._get_clinic_dir()+'/output/'+str(i))
                except FileExistsError:
                    pass
                
                
                Gammora_print._display_working_state("Creating Patient simualtion "+str(i)+"/"+str(self.Beam._get_nb_index()-1))
                shutil.copyfile(self._get_clinic_mac_dir()+'/main.mac', mac_cpi+'/main.mac')

# + Initialize Command
                self._decorate(mac_cpi+'/main.mac','Initialize')                
                self._add_initialize_command(mac_cpi+'/main.mac')

# + Soure (Reduced Phase Space)
                self._decorate(mac_cpi+'/main.mac', 'Source')
                self._add_reduced_phase_space_source(i, mac_cpi+'/main.mac', data_cpi)
# + Run Gate Command                
                self._decorate(mac_cpi+'/main.mac', 'Start Gate')
                self._add_run_command(mac_cpi+'/main.mac')

# + Create Launcher
            if self._get_calmip() == True:
                self._create_launcher_calmip(self._get_clinic_dir(), 'clinic')

            self._create_macros_set_nb_part_reduced_from_root(self._get_clinic_dir(), self._get_input_dir())
        
            os.remove(self._get_clinic_mac_dir()+'/main.mac')
            print("")
# + No CLINIC Part Simulation        
        else:
            Gammora_print._title2("Patient part simulated is disabled")        
            print("")

# Static splitting Macro Generator

    def _generate_macros_stat_split(self):
        """
        generate gate macros from rt plan simulations
        One simulation for one geometry configuration
        use linear interpolation
        """
# Declaration of paths    

        root = os.getcwd()
        global UtilsMac
        global UtilsPlacements
        global UtilsMacActor
        global UtilsMacPhantom
        UtilsPlacements=root+'/utils/placement_template/'
        UtilsMac=root+'/utils/mac/mac_template/'
        UtilsMacActor=root+'/utils/mac/actor/'
        UtilsMacPhantom=root+'/utils/mac/phantom/'
        
# Generate PHSP Macros       
        if self._get_head_part_siumulation() == True:

# + General
            if self._get_calmip() == True:
                exec_dir='/tmpdir/'+self._get_user()+'/input/'+self.Study._get_study_name()+'/'+self._get_simu_name()+'/phsp/data'
            
            if self._get_local() == True:
                exec_dir=self._get_phsp_data_dir() 

# ++ Create main.mac file        

            self._create_main_mac_file(self._get_phsp_mac_dir())
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Verbose')
# ++ Verbose
            self._add_verbose(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
# ++ Visualization
 
            if self.Beam._get_visualization() == True:
                    self._add_visualization(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
# ++ Material
            if self.Beam._get_material() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Material')
                self._add_material_tab(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

# + Geometry 1 : Definition of initial geometry
# ++ World, treatment head and killBox
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Geometry 1')
            self._add_world_geometry(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._add_treatment_head(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._add_kill_box(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
# ++ Phase Space volumes
            self._add_phase_space_volume(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
# + Counter            
            
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Counter')
            self._add_counter(self._get_phsp_mac_dir(), self._get_phsp_data_dir())
# + Physiscs
            if self.Beam._get_physics() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Physics List')
                self._add_physics(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
# + PHSP Actor
            if self.Beam._get_phsp_actor() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Actor')
                self._add_phsp_actor(self.Beam._get_phsp_actor_name(), self._get_phsp_mac_dir(), self._get_phsp_data_dir())

# + Create index architecture for job splitting

            for i in range(0, self.Beam._get_nb_index()):
                try:
                    data_cpi=self._get_phsp_data_dir()+'/'+str(i)
                    mac_cpi=self._get_phsp_mac_dir()+'/'+str(i)
                    os.mkdir(data_cpi)
                    os.mkdir(mac_cpi)
                    if self._get_local() == True:
                        os.mkdir(self._get_phsp_dir()+'/output/'+str(i))
                except FileExistsError:
                    pass

                if self._get_calmip() == True:
                    exec_dir_cpi='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/phsp/data/'+str(i)
        
                if self._get_local() == True:
                    exec_dir_cpi=self._get_phsp_data_dir()+'/'+str(i)
# + Display                
                Gammora_print._display_working_state("Creating TrueBeam head simualtion "+str(i)+"/"+str(self.Beam._get_nb_index()-1))
                shutil.copyfile(self._get_phsp_mac_dir()+'/main.mac', mac_cpi+'/main.mac')

# + Geometry                
                self._decorate(mac_cpi+'/main.mac', 'Geometry 2')
# ++ Gantry
                GantRot = self.Beam._compute_gantry_rot(self.Beam._get_gantry_angle()[i])
                self._apply_gantry_rot_stat(GantRot, mac_cpi+'/main.mac')
# ++ Colli
                self._apply_colli_rot(self.Beam._compute_colli_position(self.Beam._get_colli_angle()[i]),  mac_cpi+'/main.mac')
# ++ Jaws
                jaws_data=self.Beam._compute_jaws([self.Beam._get_x1()[i], self.Beam._get_x2()[i], self.Beam._get_y1()[i], self.Beam._get_y2()[i]])
                self._apply_jaws_stat(jaws_data, mac_cpi+'/main.mac')
# ++ MLC
                if self.Beam._get_mlc() == True:                                    
                    self._decorate(mac_cpi+'/main.mac', 'MLC position index: '+ str(i))
                    self._add_mlc_stat(mac_cpi, data_cpi, exec_dir_cpi, i)
# + Initialize Command                                   
                self._decorate(mac_cpi+'/main.mac', 'Initialize')
                self._add_initialize_command(mac_cpi+'/main.mac')
# + Source
                if self.Beam._get_source() == True:
                    self._decorate(mac_cpi+'/main.mac', 'Source')
                    if self.Beam._get_source_iaea() == True:
                        self._add_varian_phase_space_source_stat_split(i, mac_cpi+'/main.mac', data_cpi, exec_dir)
                    if self.Beam._get_source_gaga() == True:
                        self._add_gaga_phase_space_source(i, mac_cpi+'/main.mac', data_cpi, exec_dir)
# + Start Command
                self._decorate(mac_cpi+'/main.mac', 'Start Gate')
                self._add_run_command(mac_cpi+'/main.mac')
# + Create Launcher
            if self._get_calmip() == True:
                self._create_launcher_calmip(self._get_phsp_dir(), 'phsp')    
            
            os.remove(self._get_phsp_mac_dir()+'/main.mac')

# No Head Part Simulation
        else:
            Gammora_print._title2("Head part simulated is disabled")

# Generate CLINIC simulation
# General
        if self._get_patient_part_siumulation() == True:

            if self._get_calmip() == True:
                exec_dir='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/clinic/data'
            
            if self._get_local() == True:
                exec_dir=self._get_clinic_data_dir()

# + main.mac file                        
            self._create_main_mac_file(self._get_clinic_mac_dir())
# + Verbose
            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Verbose')
            self._add_verbose(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Visualization
            if self.Beam._get_visualization() == True:
                    self._add_visualization(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Material
            if self.Beam._get_material() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Material')
                self._add_material_tab(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Geometry 1 
# ++ World, Treatmend Head, 
            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Geometry 1')
            self._add_world_geometry(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# ++ Phase Space
            self._add_only_cylinder_phase_space_volume(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

# + Patient CT
            if self.Study._get_from_patient() == True:
                if self.Beam._get_patient_ct()== True:
                    self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Patient CT')
                    self._add_patient_ct(self.Beam._get_patient_ct_name(), self.Beam._get_isocenter_position(), self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
    # +  Couch
                    if self.Beam._get_couch() == True:
                        self._add_stl_couch(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Phantom            
            if self.Beam._get_phantom() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Phantom')
                self._add_phantom(self.Beam._get_phantom_name(), self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Physics            
            if self.Beam._get_physics() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Physics List')
                self._add_physics(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
# + Counter
            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Counter')          
            self._add_counter(self._get_clinic_mac_dir(), self._get_clinic_data_dir())
# + Patient Actor
            if self.Beam._get_patient_actor() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Actor')   
                self._add_patient_actor(self.Beam._get_patient_actor_name(), self._get_clinic_mac_dir(), self._get_clinic_data_dir())

# + Create index architecture for job splitting

            print("")
            for i in range(0, self.Beam._get_nb_index()):

                try:
                    data_cpi=self._get_clinic_data_dir()+'/'+str(i)
                    mac_cpi=self._get_clinic_mac_dir()+'/'+str(i)
                    os.mkdir(data_cpi)
                    os.mkdir(mac_cpi)
                    if self._get_local() == True:
                        os.mkdir(self._get_clinic_dir()+'/output/'+str(i))
                        pass
                except FileExistsError:
                    pass
                
# + Display                
                Gammora_print._display_working_state("Creating Patient simualtion "+str(i)+"/"+str(self.Beam._get_nb_index()-1))
                shutil.copyfile(self._get_clinic_mac_dir()+'/main.mac', mac_cpi+'/main.mac')
# + Main.mac
                self._decorate(mac_cpi+'/main.mac','Initialize')

# + initialize Command                
                self._add_initialize_command(mac_cpi+'/main.mac')
# + Source (Reduced Phase Space)  
                self._decorate(mac_cpi+'/main.mac', 'Source')
                self._add_reduced_phase_space_source(i, mac_cpi+'/main.mac', data_cpi)
# + Run Command
                self._decorate(mac_cpi+'/main.mac', 'Start Gate')
                self._add_run_command(mac_cpi+'/main.mac')
# + Create Launcher
            if self._get_calmip() == True:
                self._create_launcher_calmip(self._get_clinic_dir(), 'clinic')

            self._create_macros_set_nb_part_reduced_from_root(self._get_clinic_dir(), self._get_input_dir())

            os.remove(self._get_clinic_mac_dir()+'/main.mac')

# No Patient Part Simulation        
        else:
            print("Patient part simulated is disabled")

class GammoraManualSimu(GammoraSimu):
    def __init__(self):
        pass

# Main Macro Generator
    def _generate_macros(self):

        if self._get_split_type() == 'stat':
            self._generate_macros_stat_split()

        if self._get_split_type() == 'dyn':
            self._generate_macros_dyn_split()
        
    def _generate_macros_dyn_split(self):
        """
        generate gate macros from rt plan simulations
        One simulation for the all the geometry configuration
        use time slice for gate
        """
        root = os.getcwd()
        global UtilsMac
        global UtilsPlacements
        global UtilsMacActor
        global UtilsMacPhantom
        global config_default_scratch
        UtilsPlacements=root+'/utils/placement_template/'
        UtilsMac=root+'/utils/mac/mac_template/'
        UtilsMacActor=root+'/utils/mac/actor/'
        UtilsMacPhantom=root+'/utils/mac/phantom/'
        config_default_scratch = {}
        
        print("-----------------")
        print("     "+self._get_simu_name())
        print("-----------------")
       # phsp simulation
        #try:
        #    os.mkdir(self._get_local_output_dir())
        #except FileExistsError:
        #    shutil.rmtree(self._get_local_output_dir())
        #    os.mkdir(self._get_local_output_dir())
        #    pass

        if self._get_head_part_siumulation() == True:
            try: 
                self._set_phsp_dir(self._get_local_output_dir()+'/phsp')
                self._set_phsp_data_dir(self._get_phsp_dir()+'/data')
                self._set_phsp_mac_dir(self._get_phsp_dir()+'/mac')
                os.mkdir(self._get_phsp_dir())
                os.mkdir(self._get_phsp_mac_dir())
                os.mkdir(self._get_phsp_data_dir())
                if self._get_local() == True:
                    os.mkdir(self._get_phsp_dir()+'/output')
            except FileExistsError:
                pass

            if self._get_calmip() == True:
                exec_dir='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/phsp/data'
            if self._get_local() == True:
                exec_dir=self._get_phsp_data_dir()
                
            self._create_main_mac_file(self._get_phsp_mac_dir())
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Verbose')
            self._add_verbose(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            #if self._get_visualization() == True:
            #    if self._get_visualization_mode() == 1:
            #        pass
            #    if self._get_visualization_mode() ==2:
            #        pass
            if self._get_visualization() == True:
                    self._add_visualization(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

            if self._get_material() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Material')
                self._add_material_tab(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Geometry 1')
            self._add_world_geometry(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._add_treatment_head(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._add_kill_box(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

            self._add_phase_space_volume(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            
            
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Counter')
            self._add_counter(self._get_phsp_mac_dir(), self._get_phsp_data_dir())

            if self._get_physics() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Physics List')
                self._add_physics(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

            if self._get_phsp_actor() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Actor')
                self._add_phsp_actor(self._get_phsp_actor_name(), self._get_phsp_mac_dir(), self._get_phsp_data_dir())

            #self._decorate(mac_cpi+'/main.mac', 'Geometry 2')
            #GantRot = self._compute_gantry_rot(self._get_gantry_angle()[i])
            self._apply_gantry_rot_dyn(self._get_phsp_mac_dir()+'/main.mac', self._get_phsp_data_dir(), exec_dir)
            self._apply_colli_rot(self._get_colli_angle()[0],  self._get_phsp_mac_dir()+'/main.mac')
            #jaws_data=self._compute_jaws([self._get_x1()[i], self._get_x2()[i], self._get_y1()[i], self._get_y2()[i]])
            self._apply_jaws_dyn(self._get_phsp_mac_dir()+'/main.mac', self._get_phsp_data_dir(), exec_dir)

            if self._get_mlc() == True:                                    
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'MLC position: ')
                self._add_mlc_dyn(self._get_phsp_mac_dir()+'/main.mac', self._get_phsp_data_dir(), exec_dir)
                #self._create_time_slice_file(self._get_phsp_data_dir())
            print("")

            self._create_time_slice_file(self._get_phsp_data_dir())

            for i in range(0, self._get_nb_index()):
                try:
                    mac_cpi=self._get_phsp_mac_dir()+'/'+str(i)
                    os.mkdir(mac_cpi)
                    if self._get_local() == True:
                        os.mkdir(self._get_phsp_dir()+'/output/'+str(i))
                except FileExistsError:
                    pass

                if self._get_calmip() == True:
                    exec_dir_cpi='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/phsp/data/'+str(i)
        
                if self._get_local() == True:
                    exec_dir_cpi=self._get_phsp_data_dir()+'/'+str(i)
                
                self._display_working_state("Creating TrueBeam head simualtion "+str(i)+"/"+str(self._get_nb_index()-1))
                
                shutil.copyfile(self._get_phsp_mac_dir()+'/main.mac', mac_cpi+'/main.mac')

                self._decorate(mac_cpi+'/main.mac', 'Initialize')
                self._add_initialize_command(mac_cpi+'/main.mac')

                if self._get_source() == True:
                    self._decorate(mac_cpi+'/main.mac', 'Source')
                    if self._get_source_iaea() == True:
                        self._add_varian_phase_space_source_dyn_split(i, mac_cpi+'/main.mac', self._get_phsp_data_dir(), exec_dir)
                        if i == 0:
                            self._create_primary_file(self._get_phsp_data_dir())
                    if self._get_source_gaga() == True:
                        if i == 0:
                            self._create_primary_file(self._get_phsp_data_dir())
                        self._add_gaga_phase_space_source(i, mac_cpi+'/main.mac', self._get_phsp_data_dir(), exec_dir)

                self._decorate(mac_cpi+'/main.mac', 'Start Gate')
                self._add_run_command(mac_cpi+'/main.mac')

            if self._get_calmip() == True:
                self._create_launcher_calmip(self._get_phsp_dir(), 'phsp')    
            
            os.remove(self._get_phsp_mac_dir()+'/main.mac')
        else:
            print("Head part simulated is disabled")

        # clinic simulation
        if self._get_patient_part_siumulation() == True:
            try:
                self._set_clinic_dir(self._get_local_output_dir()+'/clinic')
                self._set_clinic_data_dir(self._get_clinic_dir()+'/data')
                self._set_clinic_mac_dir(self._get_clinic_dir()+'/mac')
                os.mkdir(self._get_clinic_dir())
                os.mkdir(self._get_clinic_mac_dir())
                os.mkdir(self._get_clinic_data_dir())
                if self._get_local() == True:
                    os.mkdir(self._get_clinic_dir()+'/output')
            except FileExistsError:
                pass

            if self._get_calmip() == True:
                exec_dir='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/clinic/data'
            
            if self._get_local() == True:
                exec_dir=self._get_clinic_data_dir()
            
            
            self._create_main_mac_file(self._get_clinic_mac_dir())
            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Verbose')
            self._add_verbose(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            if self._get_visualization() == True:
                    self._add_visualization(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            if self._get_material() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Material')
                self._add_material_tab(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Geometry 1')
            self._add_world_geometry(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
            self._add_only_cylinder_phase_space_volume(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            #if self._get_patient_ct()== True:
            #    print('BONSS')
            #    self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Patient CT')
            #    self._add_patient_ct(self._get_patient_ct_name(), self._get_isocenter_position(), self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
            #    if self._get_couch() == True:
            #        self._add_stl_couch(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
                
            
            if self._get_phantom() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Phantom')
                self._add_phantom(self._get_phantom_name(), self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
            
            if self._get_physics() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Physics List')
                self._add_physics(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Counter')          
            self._add_counter(self._get_clinic_mac_dir(), self._get_clinic_data_dir())

            if self._get_patient_actor() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Actor')   
                self._add_patient_actor(self._get_patient_actor_name(), self._get_clinic_mac_dir(), self._get_clinic_data_dir())

            print("")
            for i in range(0, self._get_nb_index()):

                try:
                    data_cpi=self._get_clinic_data_dir()+'/'+str(i)
                    mac_cpi=self._get_clinic_mac_dir()+'/'+str(i)
                    os.mkdir(data_cpi)
                    os.mkdir(mac_cpi)
                    if self._get_local() == True:
                        os.mkdir(self._get_phsp_dir()+'/output/'+str(i))
                except FileExistsError:
                    pass
                
                
                self._display_working_state("Creating Patient simualtion "+str(i)+"/"+str(self._get_nb_index()-1))
                shutil.copyfile(self._get_clinic_mac_dir()+'/main.mac', mac_cpi+'/main.mac')

                self._decorate(mac_cpi+'/main.mac','Initialize')
                
                self._add_initialize_command(mac_cpi+'/main.mac')
                self._decorate(mac_cpi+'/main.mac', 'Source')
                self._add_reduced_phase_space_source(i, mac_cpi+'/main.mac', data_cpi)
                self._decorate(mac_cpi+'/main.mac', 'Start Gate')
                self._add_run_command(mac_cpi+'/main.mac')

            if self._get_calmip() == True:
                self._create_launcher_calmip(self._get_clinic_dir(), 'clinic')

            self._create_macros_set_nb_part_reduced_from_root(self._get_clinic_dir(), self._get_input_dir())
        
            os.remove(self._get_clinic_mac_dir()+'/main.mac')
            print("")
        
        else:
            print("Patient part simulated is disabled")

                
            print("")


    def _generate_macros_stat_split(self):
        """
        generate gate macros from rt plan simulations
        One simulation for one geometry configuration
        use linear interpolation
        """
        root = os.getcwd()
        global UtilsMac
        global UtilsPlacements
        global UtilsMacActor
        global UtilsMacPhantom
        global config_default_scratch
        UtilsPlacements=root+'/utils/placement_template/'
        UtilsMac=root+'/utils/mac/mac_template/'
        UtilsMacActor=root+'/utils/mac/actor/'
        UtilsMacPhantom=root+'/utils/mac/phantom/'
        config_default_scratch = {}
        
       # phsp simulation
        #try:
        #    os.mkdir(self._get_local_output_dir())
        #except FileExistsError:
        #    shutil.rmtree(self._get_local_output_dir())
        #    os.mkdir(self._get_local_output_dir())
        #    pass

        if self._get_head_part_siumulation() == True:

            if self._get_calmip() == True:
                exec_dir='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/phsp/data'
        
            if self._get_local() == True:
                exec_dir=self._get_phsp_data_dir()
                
            self._create_main_mac_file(self._get_phsp_mac_dir())
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Verbose')
            self._add_verbose(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            #if self._get_visualization() == True:
            #    if self._get_visualization_mode() == 1:
            #        pass
            #    if self._get_visualization_mode() ==2:
            #        pass
            if self._get_visualization() == True:
                    self._add_visualization(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

            if self._get_material() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Material')
                self._add_material_tab(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Geometry 1')
            self._add_world_geometry(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._add_treatment_head(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            self._add_kill_box(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

            self._add_phase_space_volume(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)
            
            
            self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Counter')
            self._add_counter(self._get_phsp_mac_dir(), self._get_phsp_data_dir())

            if self._get_physics() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Physics List')
                self._add_physics(self._get_phsp_mac_dir(), self._get_phsp_data_dir(), exec_dir)

            if self._get_phsp_actor() == True:
                self._decorate(self._get_phsp_mac_dir()+'/main.mac', 'Actor')
                self._add_phsp_actor(self._get_phsp_actor_name(), self._get_phsp_mac_dir(), self._get_phsp_data_dir())


            for i in range(0, self._get_nb_index()):
                try:
                    data_cpi=self._get_phsp_data_dir()+'/'+str(i)
                    mac_cpi=self._get_phsp_mac_dir()+'/'+str(i)
                    os.mkdir(data_cpi)
                    os.mkdir(mac_cpi)
                    if self._get_local() == True:
                        os.mkdir(self._get_phsp_dir()+'/output/'+str(i))
                except FileExistsError:
                    pass

                if self._get_calmip() == True:
                    exec_dir_cpi='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/phsp/data/'+str(i)
        
                if self._get_local() == True:
                    exec_dir_cpi=self._get_phsp_data_dir()+'/'+str(i)
                
                self._display_working_state("Creating TrueBeam head simualtion "+str(i)+"/"+str(self._get_nb_index()-1))
                shutil.copyfile(self._get_phsp_mac_dir()+'/main.mac', mac_cpi+'/main.mac')

                
                self._decorate(mac_cpi+'/main.mac', 'Geometry 2')
                GantRot = self._compute_gantry_rot(self._get_gantry_angle()[i])
                self._apply_gantry_rot_stat(GantRot, mac_cpi+'/main.mac')
                self._apply_colli_rot(self._get_colli_angle()[i],  mac_cpi+'/main.mac')
                jaws_data=self._compute_jaws([self._get_x1()[i], self._get_x2()[i], self._get_y1()[i], self._get_y2()[i]])
                self._apply_jaws_stat(jaws_data, mac_cpi+'/main.mac')

                if self._get_mlc() == True:                                    
                    self._decorate(mac_cpi+'/main.mac', 'MLC position index: '+ str(i))
                    self._add_mlc_stat(mac_cpi, data_cpi, exec_dir_cpi, i)
                    
                
                self._decorate(mac_cpi+'/main.mac', 'Initialize')
                self._add_initialize_command(mac_cpi+'/main.mac')

                if self._get_source() == True:
                    self._decorate(mac_cpi+'/main.mac', 'Source')
                    if self._get_source_iaea() == True:
                        self._add_varian_phase_space_source_stat_split(i, mac_cpi+'/main.mac', data_cpi, exec_dir)
                    if self._get_source_gaga() == True:
                        self._add_gaga_phase_space_source(i, mac_cpi+'/main.mac', data_cpi, exec_dir)

                self._decorate(mac_cpi+'/main.mac', 'Start Gate')
                self._add_run_command(mac_cpi+'/main.mac')

            if self._get_calmip() == True:
                self._create_launcher_calmip(self._get_phsp_dir(), 'phsp')    
            
            os.remove(self._get_phsp_mac_dir()+'/main.mac')

        else:
            print("Head part simulated is disabled")

        # clinic simulation
        if self._get_patient_part_siumulation() == True:
            try:
                self._set_clinic_dir(self._get_local_output_dir()+'/clinic')
                self._set_clinic_data_dir(self._get_clinic_dir()+'/data')
                self._set_clinic_mac_dir(self._get_clinic_dir()+'/mac')
                os.mkdir(self._get_clinic_dir())
                os.mkdir(self._get_clinic_mac_dir())
                os.mkdir(self._get_clinic_data_dir())
                if self._get_local() == True:
                    os.mkdir(self._get_clinic_dir()+'/output')
            except FileExistsError:
                pass

            if self._get_calmip() == True:
                exec_dir='/tmpdir/'+self._get_user()+'/input/'+self._get_simu_name()+'/clinic/data'
            
            if self._get_local() == True:
                exec_dir=self._get_clinic_data_dir()
            
            
            self._create_main_mac_file(self._get_clinic_mac_dir())
            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Verbose')
            self._add_verbose(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            if self._get_visualization() == True:
                    self._add_visualization(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            if self._get_material() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Material')
                self._add_material_tab(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Geometry 1')
            self._add_world_geometry(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
            self._add_only_cylinder_phase_space_volume(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            #if self._get_patient_ct()== True:
            #    self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Patient CT')
            #    self._add_patient_ct(self._get_patient_ct_name(), self._get_isocenter_position(), self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
            #    if self._get_couch() == True:
            #        self._add_stl_couch(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
            
            if self._get_phantom() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Phantom')
                self._add_phantom(self._get_phantom_name(), self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)
            
            if self._get_physics() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Physics List')
                self._add_physics(self._get_clinic_mac_dir(), self._get_clinic_data_dir(), exec_dir)

            self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Counter')          
            self._add_counter(self._get_clinic_mac_dir(), self._get_clinic_data_dir())

            if self._get_patient_actor() == True:
                self._decorate(self._get_clinic_mac_dir()+'/main.mac', 'Actor')   
                self._add_patient_actor(self._get_patient_actor_name(), self._get_clinic_mac_dir(), self._get_clinic_data_dir())

            print("")
            for i in range(0, self._get_nb_index()):

                try:
                    data_cpi=self._get_clinic_data_dir()+'/'+str(i)
                    mac_cpi=self._get_clinic_mac_dir()+'/'+str(i)
                    os.mkdir(data_cpi)
                    os.mkdir(mac_cpi)
                    if self._get_local() == True:
                        #####os.mkdir(self._get_clinic_dir()+'/output/'+str(i))
                        pass
                except FileExistsError:
                    pass
                
                
                self._display_working_state("Creating Patient simualtion "+str(i)+"/"+str(self._get_nb_index()-1))
                shutil.copyfile(self._get_clinic_mac_dir()+'/main.mac', mac_cpi+'/main.mac')

                self._decorate(mac_cpi+'/main.mac','Initialize')
                
                self._add_initialize_command(mac_cpi+'/main.mac')
                self._decorate(mac_cpi+'/main.mac', 'Source')
                self._add_reduced_phase_space_source(i, mac_cpi+'/main.mac', data_cpi)
                self._decorate(mac_cpi+'/main.mac', 'Start Gate')
                self._add_run_command(mac_cpi+'/main.mac')

            if self._get_calmip() == True:
                self._create_launcher_calmip(self._get_clinic_dir(), 'clinic')

            self._create_macros_set_nb_part_reduced_from_root(self._get_clinic_dir(), self._get_input_dir())
        
            os.remove(self._get_clinic_mac_dir()+'/main.mac')
        
        else:
            print("Patient part simulated is disabled")