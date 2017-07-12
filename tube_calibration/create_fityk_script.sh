#!/bin/bash

for b in 33 45 57;
do
    for t in `seq 1 16`;
    do
	cat <<EOF
@0 < '/SNS/users/rwp/corelli/tube_calibration/COR_47301_${b}_${t}.txt'
@0: A = a and not (-1 < x and x < 12.5)
@0: A = a and not (242.5 < x and x < 256)
F += Lorentzian(height=~100, center=~15.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~30.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~45.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~61.5, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~75.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~90.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~104.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~120.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~135.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~150.0, hwhm=~1.28083)
F += Lorentzian(height=~100, center=~165.0, hwhm=~1.28083)
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
done
