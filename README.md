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
See examples in the [notebook](https://github.com/wayneweiqiang/PhaseNet/blob/master/docs/example_batch_prediction.ipynb): [example_batch_prediction.ipynb](example_batch_prediction.ipynb)


PhaseNet currently supports four data formats: mseed, sac, hdf5, and numpy. The test data can be downloaded here:
```
wget https://github.com/wayneweiqiang/PhaseNet/releases/download/test_data/test_data.zip
unzip test_data.zip
```

- For mseed format:
```
python phasenet/predict.py --model=model/190703-214543 --data_list=test_data/mseed.csv --data_dir=test_data/mseed --format=mseed --amplitude --response_xml=test_data/stations.xml --batch_size=1 --sampling_rate=100 --plot_figure
```
```
python phasenet/predict.py --model=model/190703-214543 --data_list=test_data/mseed2.csv --data_dir=test_data/mseed --format=mseed --amplitude --response_xml=test_data/stations.xml --batch_size=1 --sampling_rate=100 --plot_figure
```

- For sac format:
```
python phasenet/predict.py --model=model/190703-214543 --data_list=test_data/sac.csv --data_dir=test_data/sac --format=sac --batch_size=1 --plot_figure
```

- For numpy format:
```
python phasenet/predict.py --model=model/190703-214543 --data_list=test_data/npz.csv --data_dir=test_data/npz --format=numpy --plot_figure
```

- For hdf5 format:
```
python phasenet/predict.py --model=model/190703-214543 --hdf5_file=test_data/data.h5 --hdf5_group=data --format=hdf5 --plot_figure
```

- For a seismic array (used by [QuakeFlow](https://github.com/wayneweiqiang/QuakeFlow)):
```
python phasenet/predict.py --model=model/190703-214543 --data_list=test_data/mseed_array.csv --data_dir=test_data/mseed_array --stations=test_data/stations.json  --format=mseed_array --amplitude
```

Notes: 


Optional arguments:
```
usage: predict.py [-h] [--batch_size BATCH_SIZE] [--model_dir MODEL_DIR]
                  [--data_dir DATA_DIR] [--data_list DATA_LIST]
                  [--hdf5_file HDF5_FILE] [--hdf5_group HDF5_GROUP]
                  [--result_dir RESULT_DIR] [--result_fname RESULT_FNAME]
                  [--min_p_prob MIN_P_PROB] [--min_s_prob MIN_S_PROB]
                  [--mpd MPD] [--amplitude] [--format FORMAT]
                  [--s3_url S3_URL] [--stations STATIONS] [--plot_figure]
                  [--save_prob]

optional arguments:
  -h, --help            show this help message and exit
  --batch_size BATCH_SIZE
                        batch size
  --model_dir MODEL_DIR
                        Checkpoint directory (default: None)
  --data_dir DATA_DIR   Input file directory
  --data_list DATA_LIST
                        Input csv file
  --hdf5_file HDF5_FILE
                        Input hdf5 file
  --hdf5_group HDF5_GROUP
                        data group name in hdf5 file
  --result_dir RESULT_DIR
                        Output directory
  --result_fname RESULT_FNAME
                        Output file
  --min_p_prob MIN_P_PROB
                        Probability threshold for P pick
  --min_s_prob MIN_S_PROB
                        Probability threshold for S pick
  --mpd MPD             Minimum peak distance
  --amplitude           if return amplitude value
  --format FORMAT       input format
  --stations STATIONS   seismic station info
  --plot_figure         If plot figure for test
  --save_prob           If save result for test
```
