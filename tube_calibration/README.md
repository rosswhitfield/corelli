# To create calibration

```
python2 fityk.py
./create_fityk_script2.sh > gen.fit
cfitky gen.fit
./get_centers.sh
python2 create_calibration.py
```

# To apply calibrtion

```
python2 test_calib.py
```
