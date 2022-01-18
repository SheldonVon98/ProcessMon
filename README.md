# ProcessMon
 Process monitoring python script which needs no extra dependencies.

## Installation
```
git clone https://github.com/SheldonVon98/ProcessMon.git
```
## Usage
To monitor a specific process with known PID
```
python3 processMon.py --pid $PID
```
If you do not know the PID, just use keyword with the process name. Note that it is not necessary to type the whole name as long as it is not duplicated with the name of other process.
```
python3 processMon.py --keyword $ProcessName
```
The above command will monitor the process till the user exit with `crtl+c`.

Now if you want to take `10` samples with interval of `2` seconds:
```
python3 processMon.py --keyword $ProcessName --interval 2 --samples 10
```
This script will automatically save all sample data to `mon.log`.

Further, to plot the data (provided `matplotlib` is installed):
```
python3 processMon.py --keyword $ProcessName --plot
```
Figures will be automatically saved. To show it:
```
python3 processMon.py --keyword $ProcessName --plot --show
```