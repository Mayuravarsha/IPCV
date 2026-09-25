function execute_indi(name)
%EXECUTE_INDI Recolour a single scene, e.g. execute_indi('House').
[rgbnames, dataset] = get_filenames();
[ir, vis] = load_scene(dataset, name);
recoloured = enhance(ir, vis, rgbnames);
display_images(ir, vis, recoloured, figure());
end
