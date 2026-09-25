function [rgbnames, dataset] = get_filenames()
%GET_FILENAMES Read data/dataset.json.
%   dataset  - struct keyed by scene name with IR, VIS and RGB file names
%   rgbnames - "scene/file" paths of every daylight reference photo, used
%              as the colour database. Scenes without a photo are skipped.
dataset = jsondecode(fileread(fullfile(data_dir(), 'dataset.json')));
scenes = fieldnames(dataset);
rgbnames = {};
for k = 1:numel(scenes)
    rgb = dataset.(scenes{k}).RGB;
    if ~isempty(rgb)
        rgbnames{end+1} = scenes{k} + "/" + rgb; %#ok<AGROW>
    end
end
end
