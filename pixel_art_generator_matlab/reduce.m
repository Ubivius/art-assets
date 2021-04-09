function [I_reduced] = reduce(I_source,LIGNES,COLONNES)

% PETIT TEST UNITAIRE
% clear all
% close all
% clc
% I_source = [65 76 86 89;
%            48 69 128 189;
%            90 180 190 200;
%            140 80 200 190;];

L1 = size(I_source, 1);
C1 = size(I_source, 2);
% L2 = 3; % Pour test unitaire
% C2 = 3; % Pour test unitaire
L2 = LIGNES;
C2 = COLONNES;

for l = 1:L2
  for c = 1:C2
    l_min = floor(l * L1/L2);
    if l_min == 0 % Eviter les divisions par zero
      l_min = 1;
    end
    l_max = ceil(l * L1/L2);
    
    c_min = floor(c * C1/C2);
    if c_min == 0 % Eviter les divisions par zero
      c_min = 1;
    end
    
    c_max = ceil(c * C1/C2);
    
    dl = (l * L1/L2) - l_min;
    cl = (c * C1/C2) - c_min;
    
    A = I_source(l_min, c_min);
    B = I_source(l_min, c_max);
    C = I_source(l_max, c_min);
    D = I_source(l_max, c_max);
    
    X1 = A * (1 - cl) + B * cl;
    X2 = C * (1 - cl) + D * cl;
    X = X1 * (1 - dl) + X2 * dl;
    
    I_reduced(l, c) = round(X);
  end
end
