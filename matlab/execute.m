function execute(save, disp_count)
%EXECUTE Recolour every scene in the dataset.
%   execute(save, disp_count)
%   save       - 1 writes enhanced.png next to each scene's images
%   disp_count - how many results to show in figures
%   Example: execute(1, 3) saves all results and displays the first three.
[rgbnames, dataset] = get_filenames();
scenes = fieldnames(dataset);
fig_no = 1;
for k = 1:numel(scenes)
    [ir, vis] = load_scene(dataset, scenes{k});
    recoloured = enhance(ir, vis, rgbnames);
    if save
        imwrite(recoloured, fullfile(data_dir(), scenes{k}, 'enhanced.png'));
    end
    if disp_count > 0
        display_images(ir, vis, recoloured, figure(fig_no));
        disp_count = disp_count - 1;
        fig_no = fig_no + 1;
    end
    if ~save && disp_count == 0
        break;
    end
end
end
