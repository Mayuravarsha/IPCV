function image = he(image)
%HE Histogram equalisation applied to every channel independently.
for c = 1:size(image, 3)
    image(:, :, c) = histeq(image(:, :, c));
end
end
