# Kyuukimon
1.INTRODUCTION
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

2.SOFTWARE ARCHITECTURE
===
