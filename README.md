# Atrial-fibrillation-prediction
HRV-based Explainable AI for predicting the risk of atrial fibrillation.
A demo for testing deep neural networks for predicting the risk of atrial fibrillation (AF) using RR intervals during sinus rhythm. Companion code to the paper “HRV-based Explainable AI for predicting the risk of atrial fibrillation”.

Requirement.
This code was tested on Python 3.6 with Tensorflow-gpu 2.0.0 and Keras 2.3.1. In addition, Sklearn 0.0, Numpy 1.16.2 and Pandas 1.1.1 were also used. 

Files.
Demo/data contains part of the test data that were used in the paper. Demo/model contains the trained model. Demo/util contains the scripts of extracting input samples from the test data and the scripts of testing input samples with the trained model. The AURC of the test data will be saved in Demo/output as .csv file. Demo/mian.py is the script for executing all the processes of this code.

Model.
	The model used in the paper is a convolutional, long short-term memory, and fully connected deep neural network, the architecture of the model is shown in Figure 1. The model receives an input tensor with dimension (N, 90, 1), and returns an output tensor with dimension (N, 2), for which N is the batch size. The model presented in Demo/model is a well-trained model and can be directly used to test the data.

![image](https://github.com/hustzp/Atrial-fibrillation-prediction/blob/main/source/Figure1.png)
Figure 1. Architecture of the convolutional, long short-term memory, and fully connected deep neural networks.

Input of the model: shape = (N, 90, 1). The input tensor should contain the 90 points of the RR interval sample. 90 RR interval samples were extracted from the test data. All RR intervals are represented at the scale 1 s, therefore, if the input data are in ms it should be divided by 1000 before feeding it to the neural network model.
Output of the model: shape = (N, 2). The output contains two probabilities of AF and not AF, between 0 and 1, and sum to 1. 

![image](https://github.com/hustzp/Atrial-fibrillation-prediction/blob/main/source/Figure2.png)
Figure 2. One example of the .txt file of a PAF patient.

Test data.
Demo/data contains test data of 200 patients (50 patients for each type, including Normal, NAF, LAF, and PAF) that are randomly selected from the test set of the paper. The data of each patient are stored as a .txt file, and one example of the .txt file of a PAF patient is shown in Figure 2. The .txt files of other types of patients do not have AF episodes and include only information on RR intervals. More testing data are available from the corresponding authors of the paper on reasonable request.

Results.
The AURC of the four types of data are stored in the folder Demo/output as four .csv files with corresponding file name. 

Installation guide for running Demo.
1, Install Python 3.6 with Tensorflow-gpu 2.0.0 and Keras 2.3.1. Then, install the following libraries: Sklearn 0.0, Numpy 1.16.2 and Pandas 1.1.1.
2, Download the Demo.zip file and extract the files from it. Using the command line:
	$ unzip Demo.zip
3, Run the script of main.py, using the command line:
	$ python main.py
After running, there will be four .csv files in the folder Demo/output. Expected run time for the demo on a “normal”desktop computer (CPU: Intel(R) Core(TM) i5-9500 @ 3.00GHz, GPU: NVIDIA GeForce GT 710, 2GB, RAM: 16GB) is approximately 794 s (approximately 4 s for each testing file).

License.
Any data use will be restricted to noncommercial research purposes, and the data will only be made available on execution of appropriate data use agreements. This code is to be used only for educational and research purposes. Any commercial use, including the distribution, sale, lease, license, or other transfer of the code to a third party, is prohibited. 
