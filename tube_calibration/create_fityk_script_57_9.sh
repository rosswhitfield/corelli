#!/bin/bash

b=57
for t in 9;
do
    cat <<EOF
@0 < '/SNS/users/rwp/corelli/tube_calibration/COR_47301_${b}_${t}.txt'
@0: A = a and not (-1 < x and x < 12.5)
@0: A = a and not (242.5 < x and x < 256)
F += Lorentzian(height=~100, center=~16.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~31.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~46.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~61.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~76.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~91.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~106.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~121.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~137.5, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~151.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~166.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~181.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~196.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~211.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~226.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~241.0, hwhm=~1.28083)
\$_hwhm = ~1.28083
%*.hwhm = \$_hwhm
@0: guess Quadratic
@0: fit
@0: info peaks > '/SNS/users/rwp/corelli/tube_calibration/COR_47301_${b}_${t}.peaks'
delete %_*
EOF
done
