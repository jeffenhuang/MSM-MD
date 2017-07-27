%
% File name: MSM
%
% Description: This is the matlab code script for run the MSM prediction with the input file
% 'dislocation_energy.mat', this file is get by dataplot from lammps output dislocation energy
% logfile.
%
% HISTORY
% DATE        AUTHOR          DESCRIPTION
% 27/07/2017  Jianfeng Huang  First submit to Github
%

filename='dislocation_energy.mat';

load(filename);

j=6;
k=8;

xval = aveenergy(40:length(aveenergy))-1;
yval = xval<-400;
outlier = AnomalyDetection(aveenergy, xval, yval);
p=probability(j,k, aveenergy, outlier);

x=[1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0];

istart = 1;
iend = 400;
iter = 100;
result = 1:1:400;
result = result';
for i = 1:1

    pos = msmpredict(x, p, istart, iend, iter);

    result=[result, pos];
    
    %path in ubuntu platform
    %path='/home/jianfeng/MD/md/Ubuntu/msm4/data_0.04_873_29_4_14_6/output';
    %path in windows platform
    path='C:\Users\jhuang201\Documents\md\archie-west\MSMdatagen_parallel_small_model_1\data_0.004_873_299_24_149_24\output';
    figure;
    postprocess(pos,aveenergy, path);
end

filename='result.txt';
fileID = fopen(filename,'w');A1 = zeros(10,10); 

fprintf(fileID, '%3s %2s %2s %2s %2s %2s %2s %2s %2s %2s %2s\r\n', 'ID', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10');
fprintf(fileID, '%3i %2i %2i %2i %2i %2i %2i %2i %2i %2i %2i\r\n', result');
fclose(fileID);
