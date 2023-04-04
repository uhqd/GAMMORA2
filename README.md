
<img src="logo1.png" width="500" align="right">


# GAMMORA REPOSITORY

**GAMMORA** : **GA**te **M**onte-Carlo **MO**del for **RA**diotherapy

 

A full Varian TrueBeam STx Model for [Gate v9.0](https://github.com/OpenGATE/Gate)/[Geant4](https://github.com/Geant4/geant4) with the following features:
- conversion DICOM RT PLAN to GATE macros (including dynamic plans such as VMAT, DCA...)
- the particle gun is a *GAN* (neural network) trained using the data provided by [myVarian](https://www.myvarian.com/) (i.e. IAEAphsp files based on [Constantin *et al.*](https://pubmed.ncbi.nlm.nih.gov/21858999/)) . These GANs are created using [gaga](https://github.com/dsarrut/gaga)
- full geometry (MLC, jaws...). As the real geometry is confidential, the proposed model is slightly different than the real machine (but same dosmetric properties) 

Please, read the [user guide](https://github.com/uhqd/GAMMORA/blob/main/doc/userGuide/GAMMORA_USERGuide2__noVM_.pdf) for installation, getting started and simple examples. 


## Authors

**Jeremy Leste<sup>1</sup>, Maxime Chauvin<sup>1</sup>, Tony Younes<sup>1</sup>, Sara Beilla<sup>1</sup>, Luc Simon<sup>1,2</sup>**

(1)[CRCT](https://www.crct-inserm.fr/), Toulouse, France

(2)[IUCT-Oncopole](https://www.iuct-oncopole.fr/), Toulouse, France

## Validation

**Jeremy Leste<sup>1</sup>, Alexia Delbaere<sup>1</sup>, Imene Medjahed<sup>2</sup>, Maxime Chauvin<sup>1</sup>, Tony Younes<sup>1</sup>, Sara Beilla<sup>1</sup>, Luc Simon<sup>1,2</sup>**

(1)[CRCT](https://www.crct-inserm.fr/), Toulouse, France

(2)[IUCT-Oncopole](https://www.iuct-oncopole.fr/), Toulouse, France





## Publications

Reference paper:
 - Jeremy Leste, Tony Younes, Maxime Chauvin, Xavier Franceries, Alexia Delbaere, Laure Vieillevigne, Regis Ferrand, Manuel Bardies, Luc Simon, *[Technical note: GAMMORA, a free, open-source, and validated GATE-based model for Monte-Carlo simulations of the Varian TrueBeam](https://doi.org/10.1016/j.ejmp.2021.07.037)*, **Physica Medica** 89 (2021) 211–218, 

The following studies were made using GAMMORA:
 - J. Leste, I. Medjahed, M. Chauvin, T. Younes, L. Vieillevigne, R. Ferrand, X. Franceries, M. Bardies, L. Simon. *[A study of the interplay effect in Radiation Therapy using a Monte-Carlo model](https://doi.org/10.1016/j.ejmp.2021.05.019)*, **Physica Medica** 87, 73-82 (2021)  

- T. Younes, M. Chauvin, A. Delbaere, J. Labour, V. Fonteny, L. Simon, G. Fares, and L. Vieillevigne, *Towards the standardization of the absorbed dose report mode in high energy photon beams*, **Physics in Medicine and Biology** 66 (2021).

- R. Barbeiro, L. Parent, L. Vieillevigne, R. Ferrand, and X. Franceries, *Dosimetric performance of continuous EPID imaging in stereotactic treatment conditions*, **Physica Medica** 78, 117–122 (2020)

 - A. Delbaere, T. Younes, and L. Vieillevigne, *On the conversion from dose-to-medium to dose-to-water in heterogeneous phantoms with Acuros XB and Monte Carlo calculations*, **Physics in Medicine and Biology** 64 (2019).

- J. Leste, T. Younes, M. Chauvin, L. Vieillevigne, M. Bardies, X. Franceries, J. Nalis and L. Simon, *36 Monte Carlo simulation of absorbed dose distribution for electron beam using GATE/GEANT4*, **Physica Medica** 56, 21 (2018)

 - S. Beilla, T. Younes, L. Vieillevigne, M. Bardies, X. Franceries, and L. Simon, *Monte-Carlo dose calculation in presence of low-density media: Application to lung SBRT treated during DIBH*, **Physica Medica** 41, 46–52 (2017).



## PhD Thesis

The subjects of these PhD thesis were to implement, improve, validate or use GAMMORA:


- J. Leste [Implementation and clinic application of a Monte Carlo model of an external radiotherapy linear accelerator](https://tel.archives-ouvertes.fr/tel-03209752/document), PhD Thesis, Universite de Toulouse. Ph.D. thesis; Universite de Toulouse; 2020

- T. Younes [Methodologie pour la determination de la dose absorbee dans le cas des petits champs avec et sans heterogeneites pour des faisceaux de photons de haute energie](https://tel.archives-ouvertes.fr/tel-02484750/document), PhD Thesis, Universite de Toulouse.Ph.D. thesis; Universite de Toulouse; 2018

 - S. Beilla [Modelisation Monte-Carlo d’un accelerateur lineaire pour la prise en compte des densites pulmonaires dans le calcul de la dose absorbee en Radiotherapie Stereotaxique](https://hal.archives-ouvertes.fr/tel-01383148/file/THESE_BEILLA_SARA_2016_nv.pdf), PhD Thesis, Universite deToulouse. Ph.D. thesis; Universite de Toulouse; 2016



## Acknowledgements:

 - This  work  is  granted  access  to  the  HPC  resources  of  [CALMIP](https://www.calmip.univ-toulouse.fr/)  supercomputing  center under the allocation 2016-P19001.
 
 - This work was supported by the French National Cancer Institute (INCa) within the framework of the 2016 Physics Cancer Project:  STEREPID
 
 
 This repository is the last version of GAMMORA. Please read the [user guide](https://github.com/uhqd/GAMMORA/blob/main/doc/userGuide/GAMMORA_User_guide.pdf) to start (this manual should be improved soon).


Next release will include absolute dose scaling, example with job splitting, example with target motion for interplay effect assessment and a easy to use GUI. 











