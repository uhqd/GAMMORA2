#!/usr/bin/env python

import pydicom as dcm
import os
import numpy as np
import math as m
import shutil
import fileinput
import copy
import pandas as pd
import SimpleITK as sitk
#import myGateSimu


# classe for patient CT
class GammoraCT():
    def __init__(self, GammoraBeam): # To implement mhd (cropped) writting not in __init__ function
        """
        convert dicom ct to mhd and auto crop ct scan 
        """
        self._set_dicom_ct_directory(GammoraBeam._get_patient_ct_name())
        self._set_mhd_ct_directory('input/patient/'+GammoraBeam._get_study_input_name()+'/images/'+GammoraBeam._get_beam_name())
        self._set_cropped(False)
        ct = self._read_dicom_ct()
        voxel_array = self._get_voxel_array(ct)
        new_origin_original=[]
        new_origin_original.append(ct.GetOrigin()[0])
        new_origin_original.append(ct.GetOrigin()[1]*-1)
        new_origin_original.append(ct.GetOrigin()[2]*-1)   
        ct.SetOrigin(new_origin_original)
        
        self._write_original_mhd(ct)

        # for rotation of image in Gate reference frame
        bashCommand = "sed -i -e \"s/1 0 0 0 1 0 0 0 1/1 0 0 0 -1 0 0 0 -1/g\" " +self._get_mhd_ct_directory()+"_original.mhd"
        os.system(bashCommand)

        voxel_array_crop, x1, y1 = self._auto_crop(voxel_array)

        #if crop_error == True:
            #self._set_cropped(False)
        #else:
            #self._set_cropped(True)

        #if self._is_cropped() == True:
        ct_crop = sitk.GetImageFromArray(voxel_array_crop)

        crop_val=[x1, y1, 0]
        new_origin=[]

        for val1, cropval, space in zip(ct.GetOrigin(),crop_val , ct.GetSpacing()):
            new_origin.append(val1+(cropval*space))

        #for gate simulation frame
        new_origin[1]=new_origin[1]*-1
        new_origin[2]=new_origin[2]*-1
        ct_crop.SetOrigin(new_origin)
        ct_crop.SetSpacing(ct.GetSpacing())

        sitk.WriteImage(ct_crop, self._get_mhd_ct_directory()+'.mhd')
        
        # for rotation of image in Gate reference frame
        bashCommand = "sed -i -e \"s/1 0 0 0 1 0 0 0 1/1 0 0 0 -1 0 0 0 -1/g\" " +self._get_mhd_ct_directory()+".mhd"
        os.system(bashCommand)

        #else:
        #    ct2 = sitk.GetImageFromArray(voxel_array)
        #    new_origin=[]
        #    
        #    for val in ct.GetOrigin():
        #        new_origin.append(val)
        #    print(new_origin)
#
        #    #for gate simulation frame
        #    new_origin[1]=new_origin[1]*-1
        #    new_origin[2]=new_origin[2]*-1
        #    ct2.SetOrigin(new_origin)
        #    ct2.SetSpacing(ct.GetSpacing())
#
        #    sitk.WriteImage(ct2, self._get_mhd_ct_directory()+'.mhd')

   
#getteur and setteur    
    def _set_dicom_ct_directory(self, a):
        if type(a) != str:
            raise TypeError
        self.DicomCtDirectory = a

    def _get_dicom_ct_directory(self):
        return(self.DicomCtDirectory)

    def _set_mhd_ct_directory(self, a):
        if type(a) != str:
            raise TypeError
        self.MhdCtDirectory = a

    def _get_mhd_ct_directory(self):
        return(self.MhdCtDirectory)

    def _get_mhd_ct_name(self):
        return(self._get_mhd_ct_directory().split('^')[0])

    def _set_cropped(self, a): # not useful is just one class
        if type(a) != bool:
            raise TypeError
        self.Cropped = a

    def _is_cropped(self):
        return(self.Cropped)
    
    def _read_dicom_ct(self):
        #read dcm directory and compte ONE sitk 3D image object
        reader=sitk.ImageSeriesReader()
        dicom_name=reader.GetGDCMSeriesFileNames(self._get_dicom_ct_directory())
        reader.SetFileNames(dicom_name)
        ct_image = reader.Execute()
        return(ct_image)
    
    def _get_voxel_array(self, image):
        voxel_array=sitk.GetArrayFromImage(image) #Get numpy n-d array from sitk object to plot it
        return(voxel_array)

    def _write_original_mhd(self, image):
        sitk.WriteImage(image, self._get_mhd_ct_directory()+'_original.mhd')
    
    def _auto_crop(self, voxel_array):
        """
        auto cropping based on stacked HU unit allong x and y axis
        cropping is not performed on z axis
        """

        slice_sum=voxel_array.sum(axis=0)
        x=slice_sum.sum(axis=0)
        y=slice_sum.sum(axis=1)

        x=x-min(x)
        y=y-min(y)


        #crop_error=False
        #try:
        # create HU threshold for cropping
        for i in range(int(slice_sum.shape[0]/2), 0, -1):
            if x[i] < max(x)*0.12:
                x1_auto=i
                break
            #else:
            #    print('ee')
            #    x1_auto=0
            #    crop_error=True
        for i in range(int(slice_sum.shape[0]/2), int(slice_sum.shape[0]), 1):
            if x[i] < max(x)*0.12:
                x2_auto=i
                break
            #else:
            #    x2_auto = voxel_array.shape[2]
            #    crop_error=True
        for i in range(int(slice_sum.shape[1]/2), 0, -1):
            if y[i] < max(y)*0.12:
                y1_auto=i-15
                break
            #else:
                #y1_auto=0
                #crop_error=True
        for i in range(int(slice_sum.shape[1]/2), int(slice_sum.shape[1]), 1):
            if y[i] < max(y)*0.12:
                y2_auto=i
                break
            #else:
                #y2_auto=voxel_array.shape[1]
                ####@@crop_error=True

        x2_crop = x2_auto - voxel_array.shape[2]
        y2_crop = y2_auto - voxel_array.shape[1]
        voxel_array_crop = voxel_array[:, y1_auto:y2_crop, x1_auto:x2_crop]
        #print('CACA !!!!!', crop_error)
            #if crop_error != True:
        return(voxel_array_crop,x1_auto, y1_auto)
        #except UnboundLocalError:
        #    crop_error=True
        #    return(voxel_array, 0, 0, crop_error)