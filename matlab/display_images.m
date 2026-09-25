function display_images(ir, vis, recoloured, fig)
%DISPLAY_IMAGES Show IR, visible and recoloured images side by side.
imgs = {ir, vis, recoloured};
names = ["IR", "VIS", "Recoloured"];
tlo = tiledlayout(fig, 1, 3, 'TileSpacing', 'none');
for i = 1:3
    ax = nexttile(tlo);
    imshow(imgs{i}, 'Parent', ax);
    title(ax, names(i));
end
end
