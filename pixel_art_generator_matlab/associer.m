% Retourne l'index pour classifier le vecteur selon la plus proche valeur du dictionnaire
function [index_of_lowest_distance] = associer(vect, codebook)
  dist = zeros(4, 1);
  for i = 1:height(codebook)
    dist(i) = sqrt(sum((vect - codebook(i,:)) .^2));
  end
  
  [minimum, index_of_lowest_distance] = min(dist);
end