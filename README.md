# CFM
Repository related to the paper "CFM: a convolutional neural network for first-motion polarity classification of seismic records in volcanic and tectonic areas".

The folder 'dataset B test set (Mt. Pollino area)' contains two files. The first file contains the vertical components of the seismic waveforms used (hdf5 file), and the second file contains the metadata related to the specific waveform (csv).
The waveforms are centered on P-phase arrivals, demeaned, and normalized, as explained in the paper.

The folder 'Network_CFM' contains the network we trained (hdf5 file) and the plots of the accuracy and the loss computed using both the validation and the training set as the epoch changes.
The CFM network has been developed with python 3.8 and tensorflow version 2.9.1
