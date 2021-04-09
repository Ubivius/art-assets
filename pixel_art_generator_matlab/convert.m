function I_source = convert(I_source)
if length(size(I_source)) == 3
    % gray = 0.2989 * R + 0.5870 * G + 0.1140 * B
    I_source = 0.2989 .* I_source(:,:,1) + 0.5870 .* I_source(:,:,2) + 0.1140 .* I_source(:,:,3);
    I_source = I_source .* 255;
end
