function c = fuse(image1, image2)
%FUSE Single-level DWT fusion (db2 wavelet).
%   Approximation coefficients are averaged; detail coefficients use the
%   maximum rule so edges from either image survive.
[a1, h1, v1, d1] = dwt2(image1, 'db2');
[a2, h2, v2, d2] = dwt2(image2, 'db2');
c = idwt2((a1 + a2) / 2, max(h1, h2), max(v1, v2), max(d1, d2), 'db2');
end
