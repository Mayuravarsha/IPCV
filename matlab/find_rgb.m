function rgb = find_rgb(rgbImage, filenames)
%FIND_RGB Pick the daylight photo that best matches the scene.
%   Counts SIFT matches (VLFeat) between the false-colour image and every
%   reference photo and returns the one with the most matches.
[~, d] = vl_sift(im2single(rgb2gray(rgbImage)));
best = -1;
rgb = [];
for i = 1:numel(filenames)
    candidate = imresize(imread(fullfile(data_dir(), filenames{i})), [400, 400]);
    [~, d1] = vl_sift(im2single(rgb2gray(candidate)));
    n = size(vl_ubcmatch(d1, d), 2);
    if n > best
        best = n;
        rgb = candidate;
    end
    progressBar(i / numel(filenames));
end
end
