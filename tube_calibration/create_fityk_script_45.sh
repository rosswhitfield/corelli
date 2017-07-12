#!/bin/bash

b=45
for t in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 16;
do
    cat <<EOF
@0 < '/SNS/users/rwp/corelli/tube_calibration/COR_47301_${b}_${t}.txt'
@0: A = a and not (-1 < x and x < 12.5)
@0: A = a and not (242.5 < x and x < 256)
F += Lorentzian(height=~100, center=~15.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~30.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~46.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~60.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~75.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~90.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~106.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~120.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~134.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~150.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~164.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~180.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~195.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~210.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~225.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~240.0, hwhm=~1.28083)
\$_hwhm = ~1.28083
%*.hwhm = \$_hwhm
@0: guess Quadratic
@0: fit
@0: info peaks > '/SNS/users/rwp/corelli/tube_calibration/COR_47301_${b}_${t}.peaks'
delete %_*
EOF
done
