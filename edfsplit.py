# Simple script for cropping EDF file in to two TRC files with Fastwave TRC writer. 
edffile='/data/downstate/testdata/UMCexport.edf'
import mne as mne
from mne.io import read_raw_edf  
from mne.io.meas_info import _empty_info
from mne.io.utils import _create_chs, _mult_cal_one
from mne.io.constants import FIFF
from trcio import write_raw_trc
from mne.utils import verbose, logger

edfdata=read_raw_edf(edffile)
edfdatb=read_raw_edf(edffile)

edfdata.crop(0,300).load_data()   # Enter appropriate intervals for the two files
edfdatb.crop(301,600).load_data()
counter=0
for x in edfdata.ch_names:
    edfdata.ch_names[counter]=x[len(x)-5:len(x)]
    counter=counter+1

counter=0
for x in edfdatb.ch_names:
    edfdatb.ch_names[counter]=x[len(x)-5:len(x)]
    counter=counter+1

write_raw_trc(edfdata,'/data/downstate/testdata/UMCtrcdata.TRC')
write_raw_trc(edfdatb,'/data/downstate/testdata/UMCtrcdatb.TRC')

