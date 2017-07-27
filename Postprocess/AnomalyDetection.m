%Anomaly detection for the result
%   Input: i, j, k, data
%          i is the irreversible state number.
%          j is the state number in the same strain state
%          k is the different strain rate state number
%          data is energy data list for each state
%   Return: p matrix
%
%   Data          Author              Description
%   24/07/2017    Jianfeng Huang      Initilize

function outliers = AnomalyDetection(X, Xval, yval)
plot(X, 'bx');

%  Estimate my and sigma2
[mu sigma2] = estimateGaussian(X);

%  Returns the density of the multivariate normal at each data point (row) 
%  of X
p = multivariateGaussian(X, mu, sigma2);

visualizeFit(X,  mu, sigma2);

pval = multivariateGaussian(Xval, mu, sigma2);

[epsilon F1] = selectThreshold(yval, pval);

outliers = find(p < epsilon);
hold on
plot(outliers, X(outliers), 'ro', 'LineWidth', 2, 'MarkerSize', 10);
hold off
