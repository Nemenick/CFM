# CFM
Repository related to the paper "CFM: a convolutional neural network for first-motion polarity classification of seismic records in volcanic and tectonic areas" [[1]](#1) and subsequent studies [[2]](#2),[[3]](#3). For any questions, gmessuti@unisa.it, oamoroso@unisa.it, sscarpetta@unisa.it.

The folder 'dataset B test set (Mt. Pollino area)' contains two files. The first file contains the vertical components of the seismic waveforms used (hdf5 file), and the second file contains the metadata related to the specific waveform (csv).
The waveforms are centered on P-phase arrivals, demeaned, and normalized, as explained in the paper.

The folder 'Network_CFM' contains the networks we trained (CFM and CFM_with_timeshift in two .hdf5 files), along with plots illustrating their respective accuracies and losses. Note: The training accuracy of the network with timeshift is lower due to the random shift applied to the training waveforms. Note: Despite the slightly lower accuracy, we suggest using the 'CFM_with_timeshift.hdf5' network, as it is more robust to minor inaccuracies in pickings.

The folder 'Test_data' contains some example waveforms along with a csv file where some arrivals are stored.

The folder 'CFM_ensemble' contains eight independent CFM models trained with timeshift, useful to build an ensemble approach, as suggested in [[2]](#2), [[3]](#3).

All the networks have been developed with Python 3.8 and TensorFlow version 2.9.1


If needed, the file 'CFM_env.yml' can be used to recreate the environment required for utilizing the network with the provided script ('predict.py')<br>
To this end:

## 1. Set up the environment:
- Install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Download the "CFM_env.yml" file
- Install the "CFMenvironment" virtual environment (on the command prompt):
```bash
conda update -n base -c defaults conda
conda config --append channels conda-forge
conda env create -f path../CFM_env.yml
```

## 2. Start to predict the polarities:
- Activate the environment (on the command prompt):
```bash
conda activate CFMenvironment
```

- Download and Launch the script 'predict.py' (on command prompt):
```
python predict.py --model=folder_model/CFM_with_timeshift.hdf5 --data=folder_data/*.sac --format=sac --arrivals=folder_arrivals/csvfile.csv --batch_size=1 --demean=false --normalize=true --results_dir=/home/user/Desktop/...
```


Important Notes: <br>
- The built-in script ('predict.py') currently supports the input-data formats: mseed, sac. The network and the data (of any custom format) can also be loaded through a custom script, with the data provided as a NumPy array.<br>
- The 'arrivals' optional argument should contain the path to the .csv file where information about the arrival times is stored. If the arrival time information of a trace is also stored in the SAC trace, this information is used, neglecting the info in the .csv file of arrivals.<br>
- We recall that all the networks can operate only on vertical components.
- The output of the "predict.py" script comprises two CSV files. One contains the IDs of waveforms that are deemed "not predictable" for certain reasons, while the other represents the predictions. Each trace ID is associated with a predicted value indicating upward polarity probability. To determine the acceptance of upward or downward polarity, a threshold needs to be set. While we initially recommend accepting upward polarities for predicted values above 0.925 and downward polarities for values below 0.075, we encourage users to experiment with the polarity acceptance thresholds to determine the best parameters for their specific application.
- To operate with the ensemble model, use the 8 CFM networks provided in the 'CFM_ensemble' folder. Each network should be passed as an argument in a separate call to the predict.py script, which outputs the polarity probability. The ensemble prediction for each waveform is obtained by averaging the predictions from all networks in the ensemble. 

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
                        two columns, either '...arrival_sample' or '...arrival_time', is required. If both are
                        provided, arrival_sample will be considered.
  --batch_size BATCH_SIZE
                        Optional: batch size (default=1)
  --demean DEMEAN       Optional: if 'true', data will be demeaned. Any other value is interpreted as 'false'.
                        RECOMMENDED TO DEMEAN (default='true')
  --normalize NORMALIZE
                        Optional: if 'true', data will be cut and normalized. Any other value is interpreted as
                        'false'. RECOMMENDED TO NORMALIZE (default='true')
  --results_dir RESULTS_DIR
                        Optional: Folder where to store the results. If not provided, a folder in the current path is
                        created
```

 

## References
<a id="1">[1]</a> 
Messuti, G., Scarpetta, S., Amoroso, O., Napolitano, F., Falanga, M., & Capuano, P. (2023).
CFM: a convolutional neural network for first-motion polarity classification of seismic records in volcanic and tectonic areas.
Frontiers in Earth Science, 11, 1223686.
DOI: 10.3389/feart.2023.1223686

<a id="2">[2]</a> 
Messuti, G.
P-wave polarity determination via ensemble deep learning models.
In Nuovo Cimento della Societa Italiana di Fisica C (2024) 47, 5
DOI: 10.1393/ncc/i2024-24265-x

<a id="3">[3]</a> 
Messuti, G., Amoroso, O., Napolitano, F., Falanga, M., Capuano, P., & Scarpetta, S. (2025). 
Uncertainty estimation via ensembles of deep learning models and dropout layers for seismic traces. 
In Advanced Neural Artificial Intelligence: Theories and Applications (pp. 107-117). Springer, Singapore.
DOI: 10.1007/978-981-96-0994-9_10
