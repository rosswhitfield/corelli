print '<?xml version="1.0" encoding="UTF-8" ?>'
print '<detector-grouping>'
number=4
for i in range(91*16*254/number):
    print "<group name='",i,"'> <detids val='",i*number,"-",(i+1)*number-1,"'/></group>"
print '</detector-grouping>'
