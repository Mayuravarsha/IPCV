function [ir, vis] = load_scene(dataset, name)
%LOAD_SCENE Read the IR and visible images of one scene as 400x400 grayscale.
folder = fullfile(data_dir(), name);
ir  = im2gray(imresize(imread(fullfile(folder, dataset.(name).IR)),  [400, 400]));
vis = im2gray(imresize(imread(fullfile(folder, dataset.(name).VIS)), [400, 400]));
end
