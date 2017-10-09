"""
P=(B x + C)/(A x + 1)

"""

def make_fityk_cmd(run, bank, tube):
    fityk_cmd = """@0 < 'COR_{0}_{1}_{2}.txt'
@0: A = a and not (-1 < x and x < 12.5)
@0: A = a and not (242.5 < x and x < 256)
$a = ~0.0
$b = ~282.0
$c = ~128.0
F += Lorentzian(height={3}, center=(-0.396*$b+$c)/(-0.396*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.3432*$b+$c)/(-0.3432*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.2904*$b+$c)/(-0.2904*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.2376*$b+$c)/(-0.2376*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.1848*$b+$c)/(-0.1848*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.132*$b+$c)/(-0.132*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.0792*$b+$c)/(-0.0792*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.0264*$b+$c)/(-0.0264*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.0264*$b+$c)/(0.0264*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.0792*$b+$c)/(0.0792*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.132*$b+$c)/(0.132*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.1848*$b+$c)/(0.1848*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.2376*$b+$c)/(0.2376*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.2904*$b+$c)/(0.2904*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.3432*$b+$c)/(0.3432*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.396*$b+$c)/(0.396*$a+1), hwhm=~1.28083)
$_hwhm = ~1.28083
%*.hwhm = $_hwhm
@0: guess Quadratic
@0: fit
%*.height = ~{3}
@0: fit
""".format(run, bank, tube, 2000)
    return fityk_cmd

print(make_fityk_cmd(47320, 37, 8))
