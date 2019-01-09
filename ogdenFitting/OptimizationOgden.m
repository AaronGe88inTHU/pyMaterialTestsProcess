function [x,fval,exitflag,output] = OptimizationOgden(x0)
%% This is an auto generated MATLAB file from Optimization Tool.

%% Start with the default options
options = saoptimset;
%% Modify options setting
options = saoptimset(options,'Display', 'iter');
options = saoptimset(options,'HybridInterval', 'end');
options = saoptimset(options,'PlotFcns', {  @saplotbestx @saplotx @saplotf });
[x,fval,exitflag,output] = ...
simulannealbnd(@FunOgdenFitting_combine,x0,[],[],options);
