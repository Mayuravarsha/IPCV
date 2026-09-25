function out = color_transfer(S, T)
%COLOR_TRANSFER: transfer color from source image (S) into target image (T)
%using:
% Reinhard, Erik, et al. "Color transfer between images." IEEE Computer 
% graphics and applications 21.5 (2001): 34-41.
%author: Mahmoud Afifi - York university
cT=makecform('srgb2lab') ;
S=applycform(S,cT); T=applycform(T,cT);
Ls=S(:,:,1); Ls=Ls(:); Lt=T(:,:,1); Lt=Lt(:);
as=S(:,:,2); as=as(:); at=T(:,:,2); at=at(:);
bs=S(:,:,3); bs=bs(:); bt=T(:,:,3); bt=bt(:);
mLS=mean(Ls); mLT=mean(Lt);
maS=mean(as); maT=mean(at);
mbS=mean(bs); mbT=mean(bt); 
s_Lsource=std(Ls,0); s_Ltarget=std(Lt,0);
s_asource=std(as,0); s_atarget=std(at,0);
s_bsource=std(bs,0); s_btarget=std(bt,0);
T(:,:,1)=((T(:,:,1)-mLT).*(s_Lsource/s_Ltarget))+mLS;
T(:,:,2)=((T(:,:,2)-maT).*(s_asource/s_atarget))+maS;
T(:,:,3)=((T(:,:,3)-mbT).*(s_bsource/s_btarget))+mbS;
cT=makecform('lab2srgb') ;
out=    applycform(T,cT);
end