function d = data_dir()
%DATA_DIR Absolute path of the data/ folder that holds the scenes.
d = fullfile(fileparts(mfilename('fullpath')), '..', 'data');
end
