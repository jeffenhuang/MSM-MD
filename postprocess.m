% Post process function MSM model prediction for Molecular Dynamics 
% Simulation of fatigue of Nickel alloy.
%   Input: xinit is the initial state vector specified the first start state. 
%          p is the probability matrix calculated by probability.m
%          istart is the start number to predict the future state
%          iend is the end number to predict the future state
%          iter is the Montcarlo method iteration setting to get the positon
%   Return: pos vector
%
%   Date          Author              Description
%   26/06/2017    Jianfeng Huang      Initilize

function postprocess(result, aveenergy, path)

linespec = {'--or', '-*g', '--.b','-xm', '--+c', '-sk'};
n=size(result,1);%number of microstate
oldpath=cd(path);
datafiles=dir('stress_strain_load*.txt');%the result data file pattern
numfiles = length(datafiles);
mydata = cell(1, n);
newenergy = ones(1,n);
strain = ones(1,n);
stress = ones(1,n);
r = cell(1, n);
x = cell(1, n);

for k = 1:n
  name=sprintf('stress_strain_load%d.txt',result(k,1));
  mydata{k} = importdata(name);
  if(k==1)
    strain(k)=0;
  elseif (k<4)
    strain(k)=strain(k-1)+0.005;
  else
    r{k}=rem(k-4,4);
    x{k}=(k-4-r{k})/4;
    
    strain(k)=strain(k-1)+(-1)^(x{k}+1)*0.005;
  end
  temp=mydata{1,k}.data(:,3);
  stress(k)=temp(length(temp));
  newenergy(k)=aveenergy(result(k,1));
end

figure;

try
    plot(strain(1:3),stress(1:3),linespec{4}),hold on
    for i=0:(n/8-1)
        startnum=i*8+3;
        endnum = i*8+11;
        if endnum > n
            endnum = n;
        end
        plot(strain(startnum:endnum), stress(startnum:endnum),linespec{mod(i,6)+1}), hold on
    end
catch ME
   switch ME.identifier
       case 'MATLAB:badsubscript'
           fprintf('i is %d and n is %d\n',i,n);
       otherwise
           disp(ME.identifier);
   end
end
figure;
plot(newenergy,linespec{1});
cd(oldpath);

end