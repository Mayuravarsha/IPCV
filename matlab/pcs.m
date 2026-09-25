function output = pcs(image, x1, x2, y1, y2)
%PCS Piecewise-linear contrast stretching.
%   Maps [0,x1) -> [0,y1), [x1,x2) -> [y1,y2) and [x2,255] -> [y2,255].
m1 = y1 / x1;
m2 = (y2 - y1) / (x2 - x1);
m3 = (255 - y2) / (255 - x2);
img = double(image);
out = m1 * img;
mid = img >= x1 & img < x2;
high = img >= x2;
out(mid)  = m2 * (img(mid) - x1) + y1;
out(high) = m3 * (img(high) - x2) + y2;
output = cast(out, 'like', image);
end
