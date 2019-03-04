# Kyuukimon
1.Overview
===
This is a project for the simulation of Chemkin. As a project of my master degree thesis in Shanghai Jiao Tong University in China,
the project contains the knowledge in the following domain:chemistry,mathematics,software development,and algorithm of optimasation etc.
The main task is to optimize the parameters of overall reaction coefficients of SNCR(Selective Non-Catalytic Reduction) reaction.

In order to simplify the chemical reaction mechanism of SNCR, based on Chemkin-Pro, the program interface of Chemkin and Python was
built in this project. The simulation with the SNCR overall reaction and the detailed reaction mechanism is carried out. The Arrhenius
coefficients of the SNCR overall reaction is optimized by genetic algorithm with Python script. The value of the solution is analyzed
and verified. The results show that the SNCR overall reaction can describe well the process of SNCR reaction. And the error analysis 
shows that the main source of relative error is during the initial reaction period, and the reaction can be described very accurately 
after 0.3s. The overall reaction coefficients of SNCR reaction in an interval of temperature are also calculated, and the correction 
of the coefficients is calculated for different additives, so that the overall reaction can predict the left shift of the SNCR reaction
temperature window with the presence of additives.

2.ARCHITECTURE
===
![Architecture of the algorithm](https://github.com/kyle662606957/Kyuukimon/blob/master/imageForReadme/softwarestructure.PNG)

3.How to run it
===
(1)This program is depvolopped based on the software Chemkin-Pro, so the user has to install Chemkin-Pro in his or her Windows machine with default installation path of Chemkin. 
(2)Download the program and run ChemkinGA.py to calculate the Arrhenius coefficients for a temperature interval. You can also run ChemkinGAInLoop.py to calculate the coefficients of specific temperature.

6.Usage
===
The user can get the interface of Chemkin-Python with the file Python_Chemkin_ToolBox.py, to construct his or her own evalution function
, the user can check the evaluationFunction.py. The ChemkinGA.py is for the optimasation with genetic algorithm.


5.Result
===
Here are some results of the overall reactions represented in 3D which compare the overall reaction and detailed caculation of the concetration of NO and NH3. 
![Result of NH3](https://github.com/kyle662606957/Kyuukimon/blob/master/ImageResult/NH3_3d_1100K_1200K.png)
![Result of NO](https://github.com/kyle662606957/Kyuukimon/blob/master/ImageResult/NO_Tranparent_3d_1400K.png)
For more results, the user can go to https://github.com/kyle662606957/Kyuukimon/tree/master/ImageResult

6.Feedback
===
If you have any comments or questions, feel free to contact me:jiangjindong@hotmail.com


