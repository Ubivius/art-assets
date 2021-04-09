BITS = 3;
iteration_time = 5;

I_source = im2double(imread('test_spawn.jpg'))*255;

% Dimensions
WIDTH = 512;
HEIGHT = round(WIDTH * height(I_source) / width(I_source));

figure(1)
imshow(I_source/255);
start_time = tic;

% Convert to grayscale
I_source = convert(I_source/255);

figure(9)
imshow(I_source/255);

% Resize the image
I_reduced = reduce(I_source,HEIGHT,WIDTH);
figure(3)
imshow(I_reduced/255);

initial_codebook = zeros(2^BITS, 2);

% Initial Codebook
for i = 1:2^BITS
    initial_codebook(i, 1) = (256 / 2^BITS) * i;
    initial_codebook(i, 2) = 128;
end

I_source_vectors = reshape(I_reduced', 2, [])';
codebook = initial_codebook;
old_MSE = 0;
break_condition = 1;

fprintf('******* QV Iterations *******\n')
fprintf('Maximum iteration time = %.2f seconds\n', iteration_time)
while break_condition > 0
  new_codebook = zeros(height(initial_codebook), 2);
  new_I_encoded = zeros(height(I_source_vectors), 1);
  
  hit_counter = zeros(height(codebook), 1);
  
  % Iterations
  for i = 1:height(I_source_vectors)
    % Closest element 
    index_of_lowest_distance = associer(I_source_vectors(i,:), codebook);
    new_I_encoded(i) = index_of_lowest_distance;
    hit_counter(index_of_lowest_distance) = hit_counter(index_of_lowest_distance) + 1;
    
    % Sum class
    new_codebook(index_of_lowest_distance, :) = new_codebook(index_of_lowest_distance, :) + I_source_vectors(i,:);
  end

  % New codebook
  for i = 1:height(new_codebook)
    new_codebook(i,1) = round(new_codebook(i,1)/hit_counter(i));
    new_codebook(i,2) = round(new_codebook(i,2)/hit_counter(i));
  end
  
  eq = zeros(height(I_source_vectors), 2);
  
  % MSE
  for i = 1:height(I_source_vectors)
    eq(i,1) = (I_source_vectors(i,1) - new_codebook(new_I_encoded(i), 1))^2;
    eq(i,2) = (I_source_vectors(i,2) - new_codebook(new_I_encoded(i), 2))^2;
  end
  
  MSE = sum(eq(:)) / numel(I_source_vectors);
  disp("New MSE = " + MSE + ", MSE change = " + (MSE - old_MSE) + ", Time = " + toc(start_time));
  
  % End Condition
  if (toc(start_time) >= iteration_time)
    break_condition = 0;
  else
    codebook = new_codebook;  
    old_MSE = MSE;
    I_encoded = new_I_encoded;
  end
end

I_vectors = zeros((HEIGHT * WIDTH) / 2, 2);

% Decoding
for i = 1:height(I_encoded)
    I_vectors(i, 1) = codebook(I_encoded(i), 1);
    I_vectors(i, 2) = codebook(I_encoded(i), 2);
end

% Back to original shape
I_decoded = reshape(I_vectors', WIDTH, HEIGHT)';

figure(2)
imshow(I_decoded/255);
imwrite(I_decoded/255, "output.png")

% End of timer
Time = toc(start_time);
% PSNR
PSNR = computePSNR(I_reduced,I_decoded);
fprintf('********* Resultats *********\n')
fprintf('Time: %.2f s\nPSNR: %.2f dB\n\n', Time, PSNR)
fprintf('*****************************\n')

