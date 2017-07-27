%MSM model prediction for Molecular Dynamics Simulation of fatigue of
%Nickel alloy.
%   Input: xinit is the initial state vector specified the first start state. 
%          p is the probability matrix calculated by probability.m
%          istart is the start number to predict the future state
%          iend is the end number to predict the future state
%          iter is the Montcarlo method iteration setting to get the positon
%   Return: pos vector
%
%   Date          Author              Description
%   19/06/2017    Jianfeng Huang      Initilize

function [pos] = msmpredict(xinit, p,istart,iend, iter)
    %initilize the output
    pos=zeros(iend,1);
    pos(1)=1;
    
    %Process prediction for each state
    for i = istart:iend
        xi=p^(i-1)*xinit';

        l=zeros(size(xinit,2),1);
        for j = 2:size(xinit,2)
            l(j)=l(j-1)+xi(j);
        end

        dotnum=zeros(size(xinit,2),1);

        for k=1:iter
            dot=max(l)*rand();
            dotpos=find(l>dot,1);
            dotnum(dotpos)=dotnum(dotpos)+1;
        end

        pos(i)=find(dotnum==max(dotnum),1);
    end
%function end
end