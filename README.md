# CFM
Repository related to the paper "CFM: a convolutional neural network for first-motion polarity classification of seismic records in volcanic and tectonic areas".

The folder 'dataset B test set (Mt. Pollino area)' contains two files. The first file contains the vertical components of the seismic waveforms used (hdf5 file), and the second file contains the metadata related to the specific waveform (csv).
The waveforms are centered on P-phase arrivals, demeaned, and normalized, as explained in the paper.

The folder 'Network_CFM' contains the networks we trained (CFM and CFM_with_timeshift in two .hdf5 files), along with plots illustrating their respective accuracies and losses. Note: the training accuracy of the network with timeshift is lower due to the random shift applied to the training waveforms.

The networks have been developed with python 3.8 and tensorflow version 2.9.1



To use the network:
## 1. Set up the environment:
- Install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Install the "CFMenvironment" virtual envirionment
```bash
conda env update -f=env.yml -n base
conda env create -f env.yml
conda activate phasenet
```

## 2. Start to predict the polarities:

The built-in script currently supports the data formats: mseed, sac. If you need to 


- Example of usage:
```
python /predict.py --model=model/190703-214543 --data_list=test_data/mseed.csv --data_dir=test_data/mseed --format=mseed --amplitude --response_xml=test_data/stations.xml --batch_size=1 --sampling_rate=100 --plot_figure
```


Notes: 


Optional arguments:
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
