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

# or just run

```
./run.py 47301 33 200 calib.txt
./run.py 47301 45 200 calib.txt
./run.py 47301 57 200 calib.txt
```

or

```
./run.py 47301-47304 33 1000 calib.txt
./run.py 47301-47304 45 1000 calib.txt
./run.py 47301-47304 57 1000 calib.txt
```
