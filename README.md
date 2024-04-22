# CFM
Repository related to the paper "CFM: a convolutional neural network for first-motion polarity classification of seismic records in volcanic and tectonic areas". For any question gmessuti@unisa.it

The folder 'dataset B test set (Mt. Pollino area)' contains two files. The first file contains the vertical components of the seismic waveforms used (hdf5 file), and the second file contains the metadata related to the specific waveform (csv).
The waveforms are centered on P-phase arrivals, demeaned, and normalized, as explained in the paper.

The folder 'Network_CFM' contains the networks we trained (CFM and CFM_with_timeshift in two .hdf5 files), along with plots illustrating their respective accuracies and losses. Note: the training accuracy of the network with timeshift is lower due to the random shift applied to the training waveforms.

The folder 'Test_data' contains some example waveforms along with a csv file where some arrivals are stored.

The networks have been developed with python 3.8 and tensorflow version 2.9.1


If needed, the file 'CFM_env.yml' can be used to recreate the environment required for utilizing the network with the provided scritp ('predict.py')<br>
To this end:

## 1. Set up the environment:
- Install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Download the "CFM_env.yml" file
- Install the "CFMenvironment" virtual envirionment (on command prompt):
```bash
conda update -n base -c defaults conda
conda config --append channels conda-forge
conda env create -f path../CFM_env.yml
```

## 2. Start to predict the polarities:
- Activate the environment (on command prompt):
```bash
conda activate CFMenvironment
```

- Download and Launch the script 'predict.py' (on command prompt):
```
python predict.py --model=folder_model/CFM.hdf5 --data=folder_data/*.sac --format=sac --arrivals=folder_arrivals/csvfile.csv --batch_size=1 --demean=false --normalize=true --results_dir=/home/user/Desktop/...
```


Notes: <br>
- The built-in script ('predict.py') currently supports the input-data formats: mseed, sac. The network and the data (of any custom format) can be also loaded through a custom script, with the data provided as a NumPy array.<br>
- The 'arrivals' optional argument should contain the path to the .csv file where information about the arrival times is stored. If the arrival time information of a trace is also stored in the SAC trace, this information is used, neglecting the info in the .csv file of arrivals.<br>
- We recall the network can operate only on the vertical component.
- The output of the predict script comprises two CSV files. One contains the IDs of waveforms that are deemed "not predictable" for certain reasons, while the other represents the predictions. Each trace ID is associated with a predicted value indicating upward polarity probability. To determine the acceptance of upward or downward polarity, a threshold needs to be set. We recommend accepting upward polarities for outputs above 0.925 and downward polarities for outputs below 0.075.

Arguments:
```
usage: predict.py [-h] [--model MODEL] [--data DATA] [--format FORMAT] [--arrivals ARRIVALS]
                  [--batch_size BATCH_SIZE][--demean DEMEAN] [--normalize NORMALIZE]
                  [--results_dir RESULTS_DIR]

options:
  -h, --help            show this help message and exit
  --model MODEL         REQUIRED: Path of the model used to make the predictions.
  --data DATA           REQUIRED: Path of the input data. Can accept wildcards for sac or mseed formats
  --format FORMAT       REQUIRED: input data file format. Accepted values are 'sac' or 'mseed'
  --arrivals ARRIVALS   Optional: CSV file where P-wave arrivals are specified. The structure must be as follows:
                        trace_id, trace_P_arrival_sample (int), trace_P_arrival_time (UTCDateTime). Only one of the
                        two column, either '...arrival_sample' or '...arrival_time', is required. If both are
                        provided, arrival_sample will be considered.
  --batch_size BATCH_SIZE
                        Optional: batch size (default=1)
  --demean DEMEAN       Optional: if 'true', data will be demeaned. Any other value is interpreted as 'false'.
                        RECOMANDED TO DEMEAN (default='true')
  --normalize NORMALIZE
                        Optional: if 'true', data will be cut and normalized. Any other value is interpreted as
                        'false'. RECOMANDED TO NORMALIZE (default='true')
  --results_dir RESULTS_DIR
                        Optional: Folder where to store the results. If not provided, a folder in the current path is
                        created
```
