%MSM model probability calculation. Performs probability matrix formation
%   Input: i, j, k, data
%          i is the irreversible state number.
%          j is the state number in the same strain state
%          k is the different strain rate state number
%          data is energy data list for each state
%   Return: p matrix
%
%   Date          Author              Description
%   15/06/2017    Jianfeng Huang      Initilize

function [p] = probability(j,k,data, outlier)

    %initilize the output as j*k X j*k matrix
    p = zeros(j*k);

    %MSM probability
    %define the index
    j=6; %maximum j index number, index j is for different state in same strain rate.
    k=8; %maximum k index number, index k is different strain rate.
    jnx=zeros(k,j);
    for inx = 1:k
        jnx(inx,:)=[inx:k:inx+k*(j-1)];
    end

    for row = 1:1:size(jnx,1)
        for col = 1:1:size(jnx,2)
            if row == size(jnx,1)
                nextRow = 1;
            else
                nextRow = row+1;
            end
            nextState = data(jnx(nextRow,:));
            
            %Remove anomaly element
            for anomaly = outlier
                for index = 1:length(nextState)
                    if nextState(index)== data(anomaly)
                        nextState(index)=[];
                    end
                end
            end
            
            %calculate the total value of square difference between current 
            %node with each state in next strain state.
            total = sum((data(jnx(row, col))-nextState).^2);
            %fprintf('Total value is %f\n',total);
            for pinx = 1:1:size(jnx,2)
                if sum(jnx(nextRow, pinx) == outlier)>0
                    p(jnx(nextRow,pinx), jnx(row,col)) = 0;
                elseif sum(jnx(row, col) == outlier)>0
                    p(jnx(nextRow,pinx), jnx(row,col)) = 0;
                else
                    %fprintf('Data is %f\n',(data(jnx(row, col))-data(jnx(nextRow,pinx)))^2);
                    p(jnx(nextRow,pinx), jnx(row,col)) = 1-(data(jnx(row, col))-data(jnx(nextRow,pinx)))^2/total; 
                end
            end
        end
    end

%function end
end
