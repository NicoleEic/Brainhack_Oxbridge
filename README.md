# Automatization of sulcal labeling

# Contact
nicole.eichert@psy.ox.ac.uk

# Project description
FreeSurfer-based brain surface reconstruction automatically assigns surface labels, which are useful in many ways. If more detailed labels are required, for example for different sub-segments of a sulcus, the labels have to be drawn manually, which is laborious and less reproducible. The main idea of this project is to train a classifier based on manually defined sulcal labels to automatize the process. First, we'd have to scan the literature about which algorithms and softwares could be used. Then we'd have to decide on which input features to use (sulcal depth maps, myelin maps, geometric surface information, etc.). And then we can start the actual work, i.e. writing code using machine learning toolboxes such as nilearn and Keras to train a classifier.


# If your project uses data - what data is it? Where can it be obtained? Is it open access?

We will work on open access data from the HCP database, which the participants would need to download themselves. I can provide some manually labelled ROIs for these subjects as training set or we can draw some ourselves.


# Skills required to participate

Some programming experience and maybe a bit of machine learning? If no experience, no problem, we can work together in pairs.


# What different types of people could contribute?

Everyone who thinks this is interesting and who wants to learn about machine learning in neuroimaging (this includes myself).


# Integration

How would your project integrate a neuroimager/clinician/psychologist/computational scientist/maker/artist as collaborator?

* Neuroimager: knows the tools to process the surface features

* Clinician: knows which sulci would be worth studying

* Computational scientist: Knows how to program the classifier


# Milestones

* 1) Make sure everyone can access the data and the training dataset

* 2) read in data and bring it into a format that can be fed into a classifier

* 3) build the architecture for the algorithm

* 4) Tune hyperparameters to improve accuracy

* 5) if time: See if a clustering algorithm would come up with the same sulcal segments


# Preparation material

## HCP data
* Download data for 10 subjects of the HCP database
* Important: accept Open access Terms and Conditions of data usage
* https://db.humanconnectome.org
* First 10 subjects from the Q2 release of the 1200 Subjects package)
* 10.8 GB
* Subject IDs: 100307, 103414, 105115, 110411, 111312, 113619, 115320, 117122, 118730, 118932
* Further instructions for downloading from HCP: https://wiki.humanconnectome.org/display/PublicData/How+to+Access+Data+on+ConnectomeDB

Contact me, if you need help with downloading.


## Sulcal labels

... will follow in this GitHub directory ...


# Link GitHub repo:

https://github.com/NicoleEic/Brainhack_Oxbridge
