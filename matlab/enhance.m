function night_vision = enhance(IR, VIS, filenames)
%ENHANCE Fuse an IR/visible pair and give it natural daytime colours.
%   1. Stretch the IR contrast and equalise the visible image.
%   2. Fuse them with a single-level wavelet transform.
%   3. Build a false-colour image: fused+IR in red, visible in green/blue.
%   4. Find the most similar daylight photo with SIFT matching.
%   5. Transfer that photo's colour statistics (Reinhard et al., 2001).
r = fuse(pcs(IR, 40, 200, 0, 255), he(VIS));
r = imadd(uint8(IR), uint8(r));
r = imdivide(r, 2);

false_colour = he(cat(3, r, VIS, VIS));
reference = find_rgb(false_colour, filenames);
night_vision = color_transfer(double(reference)/255, double(false_colour)/255);
end
