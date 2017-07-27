%
% File name: dataplot
%
% Description: This is the matlab script for dislocation energy data read, plot
%              and save the average result to file as 'dislocation_energy.mat'.
%
% HISTORY
% DATE        AUTHOR          DESCRIPTION
% 27/07/2017  Jianfeng Huang  First submit to Github
%

linespec = {'--or', '-*g', '--.b','-xm', '--+c', '-sk'};
n=6;
datafiles = dir('*_Dislocation_*.dlog');
numfiles = size(datafiles,1);
%mydata = cell(1, numfiles);

for k = 1:numfiles
    filename=datafiles(k).name;
    
    delimiter={'.','_'};
    res=strsplit(filename,delimiter);
    sim=str2double(res(1));
    fea=str2double(res(3));
    
    resultdata(sim,fea) = datafiles(k);
end

aveenergy = zeros(size(resultdata,1),1);
logfileName = 'dataplot.log'; 
logId = fopen(logfileName);

for k=1:size(resultdata,1)
    nk = 0;
    for j=1:size(resultdata,2)
        filename=resultdata(k,j).name;
        if strfind(filename,'Dislocation')
            delimiterIn=',';
            headerlinesIn = 1;
            [mydata, delimiterOut, headerlinesOut] = importdata(filename, delimiterIn, headerlinesIn);
            
            try
                data=mydata.data;
                textdata=mydata.textdata;
                len = data(:,1);
                energy = data(:,2);
                step = str2double(textdata(2:end,2));
                aveenergy(k) = aveenergy(k) + mean(energy);
                nk = nk + 1;
                fprintf(logId, 'Reading file %s successfully with %d th node %d th dislocation.\n',filename,k,nk);
            catch ME
                switch ME.identifier
                    case 'MATLAB:assertion:LogicalScalar'
                        disp(filename);
                    case 'MATLAB:structRefFromNonStruct'
                        fprintf(logId, 'Error during read %s\n', filename);
                    otherwise
                        fprintf(logId, ME.identifier);  
                end
            end
        else
            continue;
        end
    end
    aveenergy(k) = aveenergy(k)/nk;
    xlabel('Time(ps)');
    
    ylabel('Energy(eV)');
end
%plot(aveenergy);

outputFileName='dislocation_energy.mat';
fprintf(logId, 'Writing Data to file %s', outputFileName);
save(outputFileName);
fclose('all');




