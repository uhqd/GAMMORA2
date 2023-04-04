
#!/usr/bin/env python

import pydicom as dcm
import os
import numpy as np
import math as m
import shutil
import fileinput
import copy
import pandas as pd
import matplotlib.pyplot as plt
from math import *

class Patient():
    
    def __init__(self, dcm_rt_plan):
          
        rt_plan=dcm.read_file(dcm_rt_plan)
        self.PatientName=dcm.read_file(dcm_rt_plan).PatientName
        self.PatientID=dcm.read_file(dcm_rt_plan).PatientID
        self.Beam=[]
        
        i=0
        for beam_ in rt_plan.BeamSequence:
            if beam_.TreatmentDeliveryType == 'TREATMENT':
                self.Beam.append(Beam(rt_plan, beam_, i)) # automatic naming
                i=i+1
        
        tot_mu=0.0
        for beam in self.Beam: 
            tot_mu+=beam.MU
        self.Tot_MU=tot_mu
              
    def _get_nb_beam(self):
        nb_beam=len(self.Beam)
        return nb_beam

    def _get_patient_id(self):
        return(self.PatientID)

    def _get_patient_name(self):
        return(self.PatientName)
    
    
    def _create_rt_plan_report(self):
        with open('output/'+str(self.PatientName)+'/rt_plan_report.txt', 'w') as report:
            report.write("*********************** RT PLAN SUMARY ******************************"+'\n') 
            report.write('\n')
            report.write('\n')
            report.write("GENERAL INFORMATION :"  + '\n' + '\n')
            report.write("     PATIENT Name : " + str(self.PatientName) + '\n')                       #Write  patient name
            report.write("     PATIENT ID : " + str(self.PatientID) + '\n')                    #write patient I
            report.write("TECHNICAL INFORMATION :"  + '\n' + '\n')
            report.write("     Number of Treatment Beams : " + str(self._get_nb_beam()) + '\n' + '\n')
            for beam in self.Beam:
                report.write("     Beams ID : " + str(beam.BeamID) + '\n')
                report.write("     Beams Name : " + str(beam.BeamName) + '\n')
                report.write("          Beams Type : " + str(beam.BeamType) + '\n')
                report.write("          Radiation Type : " + str(beam.BeamRadiationType) + '\n')
                report.write("          Nominal Energy : " + str(beam.BeamEnergy ) + '\n')
                report.write("          Isocenter position : " + str(beam.IsocenterPosition) + '\n')
                report.write("          Gantry Rotation Direction : " + str(beam.DirRotGant) + '\n')
                report.write("          Collimator Rotation Direction : " + str(beam.DirRotColli) + '\n')
                report.write("          Collimator Rotation Angle : " + str(beam.RotColli) + '\n')
                if str(beam.BeamRadiationType)=='ELECTRON':
                    report.write("          Applicator ID : " + str(beam.ApplicatorID) + '\n')
                    report.write("          Applicator type : " + str(beam.Applicator_type) + '\n')
                    report.write("          INSERT : " + str(beam.Insert) + '\n')
                    report.write("          DSP : " + str(beam.SSD) + '\n')
                if str(beam.BeamType)=='STATIC':
                    report.write("          Gantry Angle : " + str(beam.ControlPointSequence[0]['GantryAngle']) + '\n')
                if str(beam.BeamType)=='DYNAMIC':   
                    report.write("          Number of Control Point index  : " + str(beam._get_nb_cpi()) + '\n')
                    report.write("          Initial Gantry Angle : " + str(beam.ControlPointSequence[0]['GantryAngle']) + '\n')
                    report.write("          Final Gantry Angle : " + str(beam.ControlPointSequence[int(beam._get_nb_cpi()-1)]['GantryAngle']) + '\n')
                    
                report.write(  '\n'  + '\n' + '\n' + '\n')
                report.write(" ===== Beams Name : " + beam.BeamID + ' ======\n' + '\n')
                i=0
                for cpi in beam.ControlPointSequence:
                    report.write("   *** Control Point Index : " + str(i) + ' \n')
                    report.write("      -> X Jaws : " + str(beam.ControlPointSequence[cpi]['x_jaw']) + ' \n')
                    report.write("      -> Y Jaws : " + str(beam.ControlPointSequence[cpi]['y_jaw']) + ' \n')
                    report.write("      -> Gantry Angle : " + str(beam.ControlPointSequence[cpi]['GantryAngle']) + ' \n')

                    if beam.BeamType =='DYNAMIC':        
                        report.write("      -> MLCx : " + str(beam.ControlPointSequence[cpi]['mlc']) + ' \n')
                        report.write("      -> Cumul Dose Coeff : " + str(beam.ControlPointSequence[cpi]['DoseRate']) + ' \n' + ' \n')
                    i=i+1
    
    def _resample_rt_plan(self, OverSamplingFactor):
        new_patient=copy.deepcopy(self)
        beam_index=0
        for beam in self.Beam:
            #if beam.BeamType == 'DYNAMIC':
            mlc=[]
            x_jaw=[]
            y_jaw=[]
            
            for i in range(2):
                x_jaw.append(np.zeros(beam._get_nb_cpi()))
                y_jaw.append(np.zeros(beam._get_nb_cpi()))
                j=0
                for cpi in beam.ControlPointSequence:
                    x_jaw[i][j]=beam.ControlPointSequence[cpi]['x_jaw'][i]
                    y_jaw[i][j]=beam.ControlPointSequence[cpi]['y_jaw'][i]
                    j=j+1
                    
            for i in range(0, 120):
                mlc.append(np.zeros(beam._get_nb_cpi()))
                j=0
                for cpi in beam.ControlPointSequence:
                    mlc[i][j]=beam.ControlPointSequence[cpi]['mlc'][i]
                    j=j+1
            
            gantry_angle=beam._create_gantry_angle()
            dose_rate=np.zeros(beam._get_nb_cpi())            
            i=0
            for cpi in beam.ControlPointSequence:
                dose_rate[i]=beam.ControlPointSequence[cpi]['DoseRate']
                i=i+1
            control_point_index=np.arange(beam._get_nb_cpi())
            control_point_index_new=np.linspace(control_point_index.min(), control_point_index.max(), beam._get_nb_cpi()*OverSamplingFactor)

            mlc_new=[]
            x_jaw_new=[]
            y_jaw_new=[]
            
            for i in range(0, 120):
                mlc_new.append(np.interp(control_point_index_new, control_point_index, mlc[i]))
            for i in range(0, 2):
                x_jaw_new.append(np.interp(control_point_index_new, control_point_index, x_jaw[i]))
                y_jaw_new.append(np.interp(control_point_index_new, control_point_index, y_jaw[i]))
                
            gantry_angle_new=np.interp(control_point_index_new, control_point_index, gantry_angle)
            dose_rate_new=np.interp(control_point_index_new, control_point_index, dose_rate)
            
            mlc_new_bis=[]
            x_jaw_new_bis=[]
            y_jaw_new_bis=[]
    
            for i in range(0, len(control_point_index_new)):
                mlc_new_bis.append(np.zeros(120))
                for j in range(0, 120):
                    mlc_new_bis[i][j]=mlc_new[j][i]
            
            for i in range(0, len(control_point_index_new)):
                x_jaw_new_bis.append(np.zeros(2))
                y_jaw_new_bis.append(np.zeros(2))
                for j in range(0, 2):
                    x_jaw_new_bis[i][j]=x_jaw_new[j][i]
                    y_jaw_new_bis[i][j]=y_jaw_new[j][i]
            
            new_patient.ControlPointSequence={}
            
            for i in range(0, len(control_point_index_new)):
                new_patient.Beam[beam_index].ControlPointSequence[i]={}
                new_patient.Beam[beam_index].ControlPointSequence[i]['GantryAngle']=round(float(gantry_angle_new[i]), 3)
                new_patient.Beam[beam_index].ControlPointSequence[i]['DoseRate']=float(dose_rate_new[i])
                new_patient.Beam[beam_index].ControlPointSequence[i]['mlc']=mlc_new_bis[i]
                new_patient.Beam[beam_index].ControlPointSequence[i]['x_jaw']=x_jaw_new_bis[i]
                new_patient.Beam[beam_index].ControlPointSequence[i]['y_jaw']=y_jaw_new_bis[i]
                
            beam_index=beam_index+1
        return(new_patient)

    def _compute_plan_complexity(self):
        sas_plan = 0.0
        cls_plan = 0.0
        mfa_plan = 0.0
        mfa_norm_plan = 0.0
        mad_plan = 0.0
        mcs_plan = 0.0
        lsv_plan = 0.0
        aav_plan = 0.0
    
        for beam in self.Beam:
            print(self.PatientName)
            sas_beam = beam._compute_sas(5)
            cls_beam = beam._compute_cls()
            mfa_beam = beam._compute_mfa()
            mfa_norm_beam = beam._compute_mfa_norm()
            mad_beam = beam._compute_mad()
            mcs_beam = beam._compute_mcs()[0]
            lsv_beam = beam._compute_mcs()[1] 
            aav_beam = beam._compute_mcs()[2]

            sas_plan += sas_beam*(beam.MU/self.Tot_MU)
            cls_plan += cls_beam*(beam.MU/self.Tot_MU)
            mfa_plan += mfa_beam*(beam.MU/self.Tot_MU)
            mfa_norm_plan += mfa_norm_beam*(beam.MU/self.Tot_MU)
            mad_plan += mad_beam*(beam.MU/self.Tot_MU)
            mcs_plan += mcs_beam*(beam.MU/self.Tot_MU)
            lsv_plan += lsv_beam*(beam.MU/self.Tot_MU)
            aav_plan += aav_beam*(beam.MU/self.Tot_MU)

        return(sas_plan, cls_plan, mfa_plan, mfa_norm_plan, mad_plan, mcs_plan, lsv_plan, aav_plan)
            
class Beam():
    def __init__(self, rt_plan, beam_, i):
        self.BeamID='beam_'+str(i)  # automatic naming
        self.BeamName=beam_.BeamName   # name given on eclipse
        self.BeamRadiationType=beam_.RadiationType  # electron or photon 
        self.BeamType=beam_.BeamType   # Dynamic or static

        Evalue=str(beam_.ControlPointSequence[0].NominalBeamEnergy) # To check if it alaways 0 if more than one beam
        if self.BeamRadiationType == 'ELECTRON':
            fluence_mode='E'             
        else:
            if beam_.PrimaryFluenceModeSequence[0].FluenceMode == 'NON_STANDARD':  # To check if it alaways 0 if more than one beam
                fluence_mode='FFF'
            elif beam_.PrimaryFluenceModeSequence[0].FluenceMode == 'STANDARD':
                fluence_mode='X'
            else :
                print('ERROR ENERGY')
                raise ValueError 

        # energy type of beam
        self.BeamEnergy=Evalue+fluence_mode

        #try:
            #self.Dose = float(rt_plan.DoseReferenceSequence[0].DeliveryMaximumDose)  # in Gy (total of treatment)
        #    self.MU = float(rt_plan.FractionGroupSequence[0].ReferencedBeamSequence[beam_.BeamNumber-1].BeamMeterset) # Get Monitor unit for this beam
            #self.FractionPlanned = float(rt_plan.FractionGroupSequence[0].NumberofFractionsPlanned) # get number of fraction for this beam
        #except AttributeError:
        #    self.MU = float(rt_plan.FractionGroupSequence[0].ReferencedBeamSequence[beam_.BeamNumber].BeamMeterset)

        for i in range(0, len(rt_plan.FractionGroupSequence[0].ReferencedBeamSequence)):
            if rt_plan.FractionGroupSequence[0].ReferencedBeamSequence[i].ReferencedBeamNumber == beam_.BeamNumber:
                #d=rt_plan.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamDose
                self.MU=rt_plan.FractionGroupSequence[0].ReferencedBeamSequence[i].BeamMeterset

        #isocenter position 
        self.IsocenterPosition=[float(val) for val in beam_.ControlPointSequence[0].IsocenterPosition]
        self.IsocenterPosition[1]=self.IsocenterPosition[1]*-1  #because rotation (x axis) in GATE
        self.IsocenterPosition[2]=self.IsocenterPosition[2]*-1  #because rotation (x axis) in GATE

        self.DirRotColli= beam_.ControlPointSequence[0].BeamLimitingDeviceRotationDirection
        self.RotColli = float(beam_.ControlPointSequence[0].BeamLimitingDeviceAngle)
        self.DirRotGant=beam_.ControlPointSequence[0].GantryRotationDirection

        #self.NbCpi=(len(rt_plan_file['Beam'][beam_name]['ControlPointSequence']))

        if self.BeamRadiationType == 'ELECTRON':
            self.ApplicatorID = beam_.ApplicatorSequence[0].ApplicatorID
            self.Applicator_type = beam_.ApplicatorSequence[0].ApplicatorType
            self.SSD = beam_.SourceAxisDistance
            self.Insert = beam_.BlockSequence[0].BlockName

        if self.BeamType == 'DYNAMIC':
            
            self.ControlPointSequence={}
            for cps in beam_.ControlPointSequence:
                cpi=cps.ControlPointIndex
                self.ControlPointSequence[cpi]={}

                self.ControlPointSequence[cpi]['GantryAngle']=round(float(cps.GantryAngle), 3)
                self.ControlPointSequence[cpi]['DoseRate']=round(float(cps.ReferencedDoseReferenceSequence[0].CumulativeDoseReferenceCoefficient), 4)

                if len(cps.BeamLimitingDevicePositionSequence)== 3:
                    self.ControlPointSequence[cpi]['mlc'] = [float(val) for val in cps.BeamLimitingDevicePositionSequence[2].LeafJawPositions]
                    self.ControlPointSequence[cpi]['x_jaw'] = [float(val) for val in cps.BeamLimitingDevicePositionSequence[0].LeafJawPositions]
                    self.ControlPointSequence[cpi]['y_jaw']= [float(val) for val in cps.BeamLimitingDevicePositionSequence[1].LeafJawPositions]
                else:
                    self.ControlPointSequence[cpi]['mlc'] = [float(val) for val in cps.BeamLimitingDevicePositionSequence[0].LeafJawPositions]
                    self.ControlPointSequence[cpi]['x_jaw'] = self.ControlPointSequence[0]['x_jaw']
                    self.ControlPointSequence[cpi]['y_jaw']= self.ControlPointSequence[0]['y_jaw']

        if self.BeamType == 'STATIC':
            cps=beam_.ControlPointSequence[0]
            self.ControlPointSequence={}
            self.ControlPointSequence[0]={}
            self.ControlPointSequence[0]['GantryAngle']=round(float(cps.GantryAngle), 3)
            self.ControlPointSequence[0]['x_jaw'] = [float(val) for val in cps.BeamLimitingDevicePositionSequence[0].LeafJawPositions]
            self.ControlPointSequence[0]['y_jaw']= [float(val) for val in cps.BeamLimitingDevicePositionSequence[1].LeafJawPositions]

            if len(cps.BeamLimitingDevicePositionSequence) > 2:
                self.ControlPointSequence[0]['mlc'] = [float(val) for val in cps.BeamLimitingDevicePositionSequence[2].LeafJawPositions]
        return
                        
    def _get_nb_cpi(self):
        nb_cpi=len(self.ControlPointSequence)
        return nb_cpi

    def _get_gantry_angle(self):
        a = []
        for i in range(0, self._get_nb_cpi()):
            a.append(self.ControlPointSequence[i]['GantryAngle'])
        return(a)

    def _get_colli_angle(self):
        return(self.RotColli)

    def _get_x1(self):
        a = []
        for i in range(0, self._get_nb_cpi()):
            a.append(self.ControlPointSequence[i]['x_jaw'][0])
        return(a)
    
    def _get_x2(self):
        a = []
        for i in range(0, self._get_nb_cpi()):
            a.append(self.ControlPointSequence[i]['x_jaw'][1])
        return(a)

    def _get_y1(self):
        a = []
        for i in range(0, self._get_nb_cpi()):
            a.append(self.ControlPointSequence[i]['y_jaw'][0])
        return(a)
    
    def _get_y2(self):
        a = []
        for i in range(0, self._get_nb_cpi()):
            a.append(self.ControlPointSequence[i]['y_jaw'][1])
        return(a)

    def _get_mlc(self):
        a = []
        for i in range(0, self._get_nb_cpi()):
            a.append(self.ControlPointSequence[i]['mlc'])
        return(a)
    def _get_isocenter(self):
        return(self.IsocenterPosition)
    
    def _get_energy(self):
        return(self.BeamEnergy)


    def _create_dose_rate(self):
        dose_rate_list=np.zeros(self._get_nb_cpi())
        for i in range(self._get_nb_cpi()):
            #print(i)
            #print(self.ControlPointSequence[i]['DoseRate'])
            if i !=0:
                n=(self.ControlPointSequence[i]['DoseRate']-self.ControlPointSequence[i-1]['DoseRate'])
                dose_rate_list[i-1]=n
        dose_rate_list=dose_rate_list*len(dose_rate_list)
        dose_rate_list[-1]=1.0
        #print('lst' , dose_rate_list)
        #print('sum' , dose_rate_list.sum())
        return dose_rate_list
    
    def _print_dose_rate(self, dose_rate_list):
        cpi=list(range(0, self._get_nb_cpi()-1))
        dose_rate=list(dose_rate_list)
        del dose_rate[-1]
        fig, (ax) =  plt.subplots(1,1)
        ax.fill_between(cpi,1,dose_rate)
        ax.set(ylim=(0.5, 1.5))
        ax.set_xlabel('Control Point Index')
        ax.set_ylabel('Relative Dose Rate')
        ax.set_title('Dose Rate', fontweight='bold', fontsize='18')
    
    def _create_gantry_angle(self):
        gantry_angle_list=np.zeros(self._get_nb_cpi())
        for i in range(self._get_nb_cpi()):
            angle=self.ControlPointSequence[i]['GantryAngle']
            gantry_angle_list[i]=angle
        return gantry_angle_list
    
    def _print_gantry_angle(self, angle):
        radius=np.zeros_like(angle)+1
        angle=angle*np.pi/180
        ax = plt.axes([0.0,0.0,1,1], polar=True)
        ax.set_title('GANTRY', fontweight='bold', fontsize='18')
        fig = plt.scatter(angle,radius, label='Gantry Position', c = 'black', s =20, cmap=plt.cm.prism, alpha=0.75)
        ax.set_theta_offset(np.pi/2)
        ax.set_rticks([])
        ax= plt.text(0,0,'PATIENT', horizontalalignment= 'center', verticalalignment='center', color = 'black', fontsize='15')
        plt.legend()
    
    def _compute_time_from_rt_plan(self):
        MU=self.MU
        dose_rate=np.zeros(self._get_nb_cpi())
        for i in range(0,self._get_nb_cpi()):
            dose_rate[i]=self.ControlPointSequence[i]['DoseRate']   
            
        MU_rate=dose_rate*MU
        diffMU=np.zeros(self._get_nb_cpi())
        
        for i in range(0, self._get_nb_cpi()-1):
            diffMU[i]=MU_rate[i+1]-MU_rate[i]
            
        if str(self.BeamEnergy)=='6FFF':
            nominal_dose_rate=1400/60
        if str(self.BeamEnergy)=='6X':
            nominal_dose_rate=600/60
            
        time_cp=np.zeros(self._get_nb_cpi())
        
        for i in range(0,self._get_nb_cpi()):
            if diffMU[i] < 6.24:
                time_cp[i]=1.607/6.0
            else:
                time_cp[i]=diffMU[i]/nominal_dose_rate
                
        time=np.zeros(self._get_nb_cpi())
        for i in range(0, self._get_nb_cpi()):
            time[i]=time_cp[i]+time[i-1]
            
        return(time)

    def _resample_beam(self, OverSamplingFactor):
        new_beam=copy.deepcopy(self)

        mlc=[]
        x_jaw=[]
        y_jaw=[]
        
        for i in range(2):
            x_jaw.append(np.zeros(self._get_nb_cpi()))
            y_jaw.append(np.zeros(self._get_nb_cpi()))
            j=0
            for cpi in self.ControlPointSequence:
                x_jaw[i][j]=self.ControlPointSequence[cpi]['x_jaw'][i]
                y_jaw[i][j]=self.ControlPointSequence[cpi]['y_jaw'][i]
                j=j+1
                
        for i in range(0, 120):
            mlc.append(np.zeros(self._get_nb_cpi()))
            j=0
            for cpi in self.ControlPointSequence:
                mlc[i][j]=self.ControlPointSequence[cpi]['mlc'][i]
                j=j+1
            
            gantry_angle=self._create_gantry_angle()
            dose_rate=np.zeros(self._get_nb_cpi())            
            i=0
            for cpi in self.ControlPointSequence:
                dose_rate[i]=self.ControlPointSequence[cpi]['DoseRate']
                i=i+1
            control_point_index=np.arange(self._get_nb_cpi())
            control_point_index_new=np.linspace(control_point_index.min(), control_point_index.max(), self._get_nb_cpi()*OverSamplingFactor)

            mlc_new=[]
            x_jaw_new=[]
            y_jaw_new=[]
            
            for i in range(0, 120):
                mlc_new.append(np.interp(control_point_index_new, control_point_index, mlc[i]))
            for i in range(0, 2):
                x_jaw_new.append(np.interp(control_point_index_new, control_point_index, x_jaw[i]))
                y_jaw_new.append(np.interp(control_point_index_new, control_point_index, y_jaw[i]))
                
            gantry_angle_new=np.interp(control_point_index_new, control_point_index, gantry_angle)
            dose_rate_new=np.interp(control_point_index_new, control_point_index, dose_rate)
            
            mlc_new_bis=[]
            x_jaw_new_bis=[]
            y_jaw_new_bis=[]
    
            for i in range(0, len(control_point_index_new)):
                mlc_new_bis.append(np.zeros(120))
                for j in range(0, 120):
                    mlc_new_bis[i][j]=mlc_new[j][i]
            
            for i in range(0, len(control_point_index_new)):
                x_jaw_new_bis.append(np.zeros(2))
                y_jaw_new_bis.append(np.zeros(2))
                for j in range(0, 2):
                    x_jaw_new_bis[i][j]=x_jaw_new[j][i]
                    y_jaw_new_bis[i][j]=y_jaw_new[j][i]

            
            for i in range(0, len(control_point_index_new)):
                self.ControlPointSequence[i]={}
                self.ControlPointSequence[i]['GantryAngle']=round(float(gantry_angle_new[i]), 3)
                self.ControlPointSequence[i]['DoseRate']=float(dose_rate_new[i])
                self.ControlPointSequence[i]['mlc']=mlc_new_bis[i]
                self.ControlPointSequence[i]['x_jaw']=x_jaw_new_bis[i]
                self.ControlPointSequence[i]['y_jaw']=y_jaw_new_bis[i]
        return(new_beam)

    def _compute_leaves_limit(self):
        leaves_limit=[]
        for cpi in self.ControlPointSequence:
            a=abs(self.ControlPointSequence[cpi]['y_jaw'][0])
            b=abs(self.ControlPointSequence[cpi]['y_jaw'][1])
            OL=2
            HL=26
            QL=32
            #epaisseur en mm
            epaisseur_OL=7
            epaisseur_HL=5
            epaisseur_QL=2.5
            nb_of_QL_a=ceil(a/epaisseur_QL)
            nb_of_QL_b=ceil(b/epaisseur_QL)
            if nb_of_QL_a > (QL/2):   
                nb_QLa=QL/2
                nb_of_HL_a=ceil((a-((QL/2)*epaisseur_QL))/5)
                if nb_of_HL_a > (HL/2):  
                    nb_HLa=HL/2
                    nb_of_OL_a=ceil((a-(((QL/2)*epaisseur_QL)+((HL/2)*epaisseur_HL)))/7)  
                else:
                    nb_HLa=nb_of_HL_a        
            else:    
                nb_QLa=nb_of_QL_a
                nb_HLa=0

            if nb_of_QL_b > (QL/2):   
                nb_QLb=QL/2
                nb_of_HL_b=ceil((b-((QL/2)*epaisseur_QL))/5)
                if nb_of_HL_b > (HL/2):  
                    nb_HLb=HL/2
                    nb_of_OL_b=ceil((b-(((QL/2)*epaisseur_QL)+((HL/2)*epaisseur_HL)))/7)  
                else:
                    nb_HLb=nb_of_HL_b       
            else:    
                nb_QLb=nb_of_QL_b
                nb_HLb=0

            debut_champ=(30-nb_QLa-nb_HLa)#-1 #to fit vectror indexing
            fin_champ=(30+nb_QLb+nb_HLb)#-1 #to fit vectror indexing
            leaves_limit.append([int(debut_champ), int(fin_champ)])
        return(leaves_limit)


    def _compute_sas(self, *sas_crit):
        sas_beam=0.0
        dose_rate_list=self._create_dose_rate()
        dose_rate_list=dose_rate_list/self._get_nb_cpi()
        leaves_limit=self._compute_leaves_limit()
        sas=[]
        for crit in sas_crit:
            for cpi in self.ControlPointSequence: 
                mlc=self.ControlPointSequence[cpi]['mlc']
        
                nb_small_aperture_cpi=0
                nb_aperture_more_than_zero_cpi=0
                sas_cpi=0.0

                for i in range(leaves_limit[cpi][0],leaves_limit[cpi][1]):       
                    aperture=(mlc[i+60]-mlc[i])
                    if  aperture > 0.0:
                        nb_aperture_more_than_zero_cpi += 1
                        if  aperture < crit:
                            nb_small_aperture_cpi += +1
                    if self.BeamType == 'DYNAMIC':
                        dose_ratio=dose_rate_list[cpi]
                    else:
                        dose_ratio=1.0
                sas_cpi=(nb_small_aperture_cpi/nb_aperture_more_than_zero_cpi)*dose_ratio
                sas_beam += sas_cpi
            sas.append(sas_beam)
            #sas_plan += sas_beam*(self.MU/1)   #normaement diviser par la dose detout le plan 'pondération des beams)
        return sas_beam

    def _compute_cls(self):
        dose_rate_list=self._create_dose_rate()
        dose_rate_list=dose_rate_list/self._get_nb_cpi()
        leaves_limit=self._compute_leaves_limit()
        cls_beam=0.0
        
        for cpi in self.ControlPointSequence:
            mlc=self.ControlPointSequence[cpi]['mlc']
            nb_leaves_field=((leaves_limit[cpi][1]-leaves_limit[cpi][0]))+1
            nb_aperture_equal_zero_cpi=0
            cls_cpi=0.0
            for i in range(leaves_limit[cpi][0],leaves_limit[cpi][1]):       
                aperture=(mlc[i+60]-mlc[i])
                if  aperture == 0.0:
                    nb_aperture_equal_zero_cpi += +1
                if self.BeamType == 'DYNAMIC':
                    dose_ratio=dose_rate_list[cpi]
                else:
                    dose_ratio=1.0
            cls_cpi=(nb_aperture_equal_zero_cpi/nb_leaves_field)*dose_ratio
            cls_beam += cls_cpi
            #print('cls beam', cls_beam)
        #sas_plan += sas_beam*(self.MU/1)   #normaement diviser par la dose detout le plan 'pondération des beams)
        return cls_beam

    def _compute_mfa(self):
        dose_rate_list=self._create_dose_rate()
        dose_rate_list=dose_rate_list/self._get_nb_cpi()
        leaves_limit=self._compute_leaves_limit()
        mfa_beam=0.0
        for cpi in self.ControlPointSequence:
            area_cpi1=0.0
            area_cpi2=0.0
            mlc=self.ControlPointSequence[cpi]['mlc']
            #nb_leaves_field=((leaves_limit[cpi][1]-leaves_limit[cpi][0]))+1
            for i in range(leaves_limit[cpi][0],leaves_limit[cpi][1]):
                aperture=(mlc[i+60]-mlc[i])
                if i == 0 and i ==  59: # Outboard Leaves
                    leaves_width=7
                if 13 < i < 46:
                    leaves_width=2.5  # Quater Leaves
                else:
                    leaves_width=5  # Half Leaves  

                leaves_pair_area = aperture*leaves_width
                area_cpi1 += leaves_pair_area

                if self.BeamType == 'DYNAMIC':
                    dose_ratio=dose_rate_list[cpi]
                else:
                    dose_ratio=1.0

            area_cpi2=area_cpi1*dose_ratio
            mfa_beam += area_cpi2

        return(mfa_beam)

    def _compute_mfa_norm(self):
        dose_rate_list=self._create_dose_rate()
        dose_rate_list=dose_rate_list/self._get_nb_cpi()
        leaves_limit=self._compute_leaves_limit()
        mfa_beam_norm=0.0

        for cpi in self.ControlPointSequence: 
            area_cpi1=0.0
            mlc=self.ControlPointSequence[cpi]['mlc']
            f_x_size=self.ControlPointSequence[cpi]['x_jaw'][1]-self.ControlPointSequence[cpi]['x_jaw'][0]
            f_y_size=self.ControlPointSequence[cpi]['y_jaw'][1]-self.ControlPointSequence[cpi]['y_jaw'][0]
            field_size=f_x_size*f_y_size

            for i in range(leaves_limit[cpi][0],leaves_limit[cpi][1]):
                aperture=(mlc[i+60]-mlc[i])
                if i == 0 and i ==  59: # Outboard Leaves
                    leaves_width=7
                if 13 < i < 46:
                    leaves_width=2.5  # Quater Leaves
                else:
                    leaves_width=5  # Half Leaves
                
                leaves_pair_area = aperture*leaves_width
                area_cpi1 += leaves_pair_area
                if self.BeamType == 'DYNAMIC':
                    dose_ratio=dose_rate_list[cpi]
                else:
                    dose_ratio=1.0      
            area_cpi2=area_cpi1*dose_ratio/field_size
            mfa_beam_norm = mfa_beam_norm+area_cpi2
        return( mfa_beam_norm)
        
    def _compute_mad(self):
        dose_rate_list=self._create_dose_rate()
        dose_rate_list=dose_rate_list/self._get_nb_cpi()
        leaves_limit=self._compute_leaves_limit()
        mad_beam=0.0
        for cpi in self.ControlPointSequence:
            mad_cpi=0.0
            mlc=self.ControlPointSequence[cpi]['mlc']
            for i in range(leaves_limit[cpi][0],leaves_limit[cpi][1]):
                aperture=(mlc[i+60]-mlc[i])
                if  aperture > 0.0:
                    midle=(aperture/2)
                    mad_cpi += abs(mlc[i]+midle)
                if self.BeamType == 'DYNAMIC':
                    dose_ratio=dose_rate_list[cpi]
                else:
                    dose_ratio=1.0
            mad_cpi=mad_cpi*dose_ratio
            mad_beam += mad_cpi
        return(mad_beam)

    def _compute_mcs(self):
        dose_rate_list=self._create_dose_rate()
        dose_rate_list=dose_rate_list/self._get_nb_cpi()
        leaves_limit=self._compute_leaves_limit()
        mcs_beam=0.0
        lsv_beam=0.0
        aav_beam=0.0

        # monving leafs
        mask_move=np.zeros_like(self.ControlPointSequence[0]['mlc'], dtype=bool)
        for cpi in range(0, self._get_nb_cpi()-1):
            a=np.asarray(self.ControlPointSequence[cpi]['mlc'])
            b=np.asarray(self.ControlPointSequence[cpi+1]['mlc'])
            mlc_move_test=b-a
            for i in range(0, len(mlc_move_test)):
                if mlc_move_test[i] !=0:
                    mask_move[i]=True
            
        N_moving=mask_move.sum()

        for cpi in self.ControlPointSequence:
            LSV_cpi=np.zeros(self._get_nb_cpi())
            AAV_cpi=np.zeros(self._get_nb_cpi())
            mlc=self.ControlPointSequence[cpi]['mlc']
            mlc=mlc*mask_move
            mlc_left_bank=(mlc[leaves_limit[cpi][0]:leaves_limit[cpi][1]])
            mlc_right_bank=(mlc[leaves_limit[cpi][0]+60:leaves_limit[cpi][1]+60])
            pos_max_left=abs(max(mlc_left_bank)-min(mlc_left_bank))
            pos_max_right=abs(max(mlc_right_bank)-min(mlc_right_bank))
            LSV_left_1=0.0
            LSV_right_1=0.0
            LSV_left_2=0.0
            LSV_right_2=0.0
            AAV_1=0.0

            aperture_area_cpi=np.zeros(len(mlc_left_bank))
            for n in range(0, len(mlc_left_bank)-1):
                aperture_between_opposite_leaves=mlc_right_bank[n]-mlc_left_bank[n]
                l=n+leaves_limit[cpi][0]
                if l == 0 and l ==  59: # Outboard Leaves
                    leaves_width=7
                if 14 < l < 46:
                    leaves_width=2.5  # Quater Leaves
                else:
                    leaves_width=5  # Half Leaves
                aperture_area_cpi[n]=aperture_between_opposite_leaves*leaves_width
                AAV_1 += aperture_area_cpi[n]

                if mlc_left_bank[n] != 0 and mlc_right_bank[n] != 0 and aperture_between_opposite_leaves != 0:
                    LSV_left_1 += pos_max_left-(abs(mlc_left_bank[n]-mlc_left_bank[n+1]))
                    LSV_right_1 += pos_max_right-(abs(mlc_right_bank[n]-mlc_right_bank[n+1]))
            
                    LSV_left_2 = LSV_left_1/((N_moving/2)*pos_max_left)
                    LSV_right_2 = LSV_right_1/((N_moving/2)*pos_max_right)

            l2=mlc_right_bank.argmax()+leaves_limit[cpi][0]
            l3=mlc_left_bank.argmin()+leaves_limit[cpi][0]
            
            if l2 == 0 and l2 ==  59: # Outboard Leaves
                leaves_width2=7
            if 14 < l2 < 46:
                leaves_width2=2.5  # Quater Leaves
            else:
                leaves_width2=5  # Half Leaves

            max_area_cpi=max(aperture_area_cpi)
            LSV_cpi[cpi] = LSV_left_2 * LSV_right_2
            AAV_cpi[cpi] = AAV_1/(N_moving*max_area_cpi)  

            mcs_beam += (LSV_cpi[cpi])*(AAV_cpi[cpi])*dose_rate_list[cpi]    
            lsv_beam += LSV_cpi[cpi]*dose_rate_list[cpi]
            aav_beam += AAV_cpi[cpi]*dose_rate_list[cpi]

        return(mcs_beam, lsv_beam, aav_beam)

   