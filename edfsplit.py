# Simple script with example MNE command for cropping EDF file in to two TRC files
# based on intervals, or channel selections with "Fastwave" TRC writer. 
edffile='/data/sweiss/labdata/TJU_io_seeg_data/sleep_edf/IO017J_s1.edf'
#edffile='/data/downstate/testdata/EDFexport.edf'
import mne
import numpy
from mne.io import read_raw_edf  
from trcio import write_raw_trc


edfdata=read_raw_edf(edffile)
edfdatb=read_raw_edf(edffile)

# Enter appropriate intervals for the two files
edfdata.crop(0,300).load_data()   
edfdatb.crop(301,600).load_data()

#'Performing amplitude test to determine scaling value of EDF test')
amptest=numpy.abs(edfdata._data)
med_eeg_val=numpy.median(amptest, axis=1)
med_eeg_val=numpy.median(med_eeg_val)
if med_eeg_val > .1:
    edfdata._data *= 1e-6
    edfdatb._data *= 1e-6
        
# truncate EDF channel names to 5-6 characters, may need to be modified. if the channel names are not unique the file will be
# corrupted. Some manufacturers will not require this step (Quantum?)
counter=0
for x in edfdata.ch_names:
    edfdata.ch_names[counter]=x[len(x)-5:len(x)]#
    counter=counter+1

counter=0
for x in edfdatb.ch_names:
    edfdatb.ch_names[counter]=x[len(x)-5:len(x)]
    counter=counter+1

# Write TRC files
write_raw_trc(edfdata,'/data/downstate/testdata/EDFtrcdata.TRC')
write_raw_trc(edfdatb,'/data/downstate/testdata/EDFtrcdatb.TRC')

# Load new EDF data to split by channel intervals
edfdatc=read_raw_edf(edffile)
edfdatd=read_raw_edf(edffile)

# Select channel intervals for the split
dropchan_list=edfdatc.ch_names[51:len(edfdatc.ch_names)]
edfdatc.drop_channels(dropchan_list).load_data()
dropchan_list=edfdatd.ch_names[1:50]
edfdatd.drop_channels(dropchan_list).load_data()

# apply amplitude test results
if med_eeg_val > .1:
    edfdatc._data *= 1e-6
    edfdatd._data *= 1e-6

# truncate EDF channel names to 5-6 characters, may need to be modified. if the channel names are not unique the file will be
# corrupted. Some manufacturers will not require this step (Quantum?)
counter=0
for x in edfdatc.ch_names:
    edfdatc.ch_names[counter]=x[len(x)-5:len(x)]
    counter=counter+1

counter=0
for x in edfdatd.ch_names:
   edfdatd.ch_names[counter]=x[len(x)-5:len(x)]
   counter=counter+1

# Write TRC files
write_raw_trc(edfdatc,'/data/downstate/testdata/EDFtrcdatc.TRC')
write_raw_trc(edfdatd,'/data/downstate/testdata/EDFtrcdatd.TRC')
