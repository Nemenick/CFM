from obspy import UTCDateTime
import obspy
import numpy as np
import pandas as pd
import tensorflow as tf
import argparse
import os
from datetime import datetime


def read_mseed(fname, csv_arrivals={}):
    sampling_rate=100
    try:
        stream = obspy.read(fname,format="MSEED")
    except Exception as e:                              # Try to read the mseed
        print(f"Error reading {fname}: {e}")
        return {}
    
    if csv_arrivals != {}:
        try:
            csv_arrivals = pd.read_csv(csv_arrivals)
        except Exception as e:                              # Try to read the csv arrival file
            csv_arrivals = {}
            print(f"Error reading csv of arrivals: {e}")

    data = np.zeros([len(stream), 400], dtype=np.float32)       # create the data np.array and the trace_ids list
    ids_predictable = []                                        # ID of "OK" traces 
    ids_not_predictable = []                                    # ID of traces "not predictable"
    error_not_predictable = []                                  # Reason why the trace is "not predictable"
    arrivals = []
    
    i = 0
    for trace in stream:
    
        if trace.id[-1].upper() != "Z":
            ids_not_predictable.append(trace.id)
            error_not_predictable.append("CFM only works on vertical component. This is not a vertical component!")
            continue
        
        arrival = -10
        # try to find a valid arrival time
        if "trace_P_arrival_sample" in csv_arrivals.keys():
            if len(csv_arrivals[csv_arrivals["trace_id"]==trace.id])>1:
                ids_not_predictable.append(trace.id)
                error_not_predictable.append("Two or more arrival found for the trace with this id!")
                continue
            if len(csv_arrivals[csv_arrivals["trace_id"]==trace.id])==1:
                arrival = int(float(csv_arrivals[csv_arrivals["trace_id"]==trace.id]["trace_P_arrival_sample"].iloc[0]))
        elif "trace_P_arrival_time" in csv_arrivals.keys():
            if len(csv_arrivals[csv_arrivals["trace_id"]==trace.id])>1:
                ids_not_predictable.append(trace.id)
                error_not_predictable.append("Two or more arrival found for the trace with this id!")
                continue
            if len(csv_arrivals[csv_arrivals["trace_id"]==trace.id])==1:
                arrival = int((UTCDateTime(csv_arrivals[csv_arrivals["trace_id"]==trace.id]["trace_P_arrival_time"].iloc[0])-trace.stats.starttime) * trace.stats.sampling_rate)
                
        if arrival < 0:
            ids_not_predictable.append(trace.id)
            error_not_predictable.append("Unable to find a valid P arrival")
            continue
        
        # Verify sampling rate
        if abs(trace.stats.sampling_rate - sampling_rate) > 0.1:
            ids_not_predictable.append(trace.id)
            error_not_predictable.append("Trace with sampling rate different to 100Hz")
            continue

        semi_amp = 200
        # Verify enough samples are present
        if arrival<semi_amp or arrival>len(trace.data)-semi_amp:
            ids_not_predictable.append(trace.id)
            error_not_predictable.append("Trace with not enough point before or after the arrival")
            continue

        ids_predictable.append(trace.id)
        data[i,:] = trace.data[arrival-semi_amp:arrival+semi_amp]
        arrivals.append(arrival)
        i+=1
    pd_pred = pd.DataFrame.from_dict({"id_predictable":ids_predictable,"trace_P_arrival_sample":arrivals})
    pd_not_pred = pd.DataFrame.from_dict({"id_not_predictable":ids_not_predictable, "error":error_not_predictable})
    if len(data) <1:
        print("WARNING: no data is predictable")        
    return data[:len(ids_predictable),:], pd_pred, pd_not_pred

def read_sac(fname, csv_arrivals={}):
    sampling_rate=100
    try:
        stream = obspy.read(fname,format="SAC")
    except Exception as e:                              # Try to read the mseed
        print(f"Error reading {fname}: {e}")
        return {}
    
    if csv_arrivals != {}:
        try:
            csv_arrivals = pd.read_csv(csv_arrivals)
        except Exception as e:                              # Try to read the csv arrival file
            csv_arrivals = {}
            print(f"Error reading csv of arrivals: {e}")

    data = np.zeros([len(stream), 400], dtype=np.float32)       # create the data np.array and the trace_ids list
    ids_predictable = []                                        # ID of "OK" traces 
    ids_not_predictable = []                                    # ID of traces "not predictable"
    error_not_predictable = []                                  # Reason why the trace is "not predictable"
    arrivals = []
    i = 0
    for trace in stream:

        if trace.id[-1].upper() != "Z":
            ids_not_predictable.append(trace.id)
            error_not_predictable.append("CFM only works on vertical component. This is not a vertical component!")
            continue

        arrival = -10
        # try to find a valid arrival time
        if "a" in trace.stats.sac.keys():
            arrival = int((trace.stats.sac["a"]-trace.stats.sac["b"])*trace.stats.sampling_rate)
        elif "trace_P_arrival_sample" in csv_arrivals.keys():
            if len(csv_arrivals[csv_arrivals["trace_id"]==trace.id])>1:
                ids_not_predictable.append(trace.id)
                error_not_predictable.append("Two or more arrival found for the trace with this id!")
                continue
            if len(csv_arrivals[csv_arrivals["trace_id"]==trace.id])==1:
                arrival = int(float(csv_arrivals[csv_arrivals["trace_id"]==trace.id]["trace_P_arrival_sample"].iloc[0]))
        elif "trace_P_arrival_time" in csv_arrivals.keys():
            if len(csv_arrivals[csv_arrivals["trace_id"]==trace.id])>1:
                ids_not_predictable.append(trace.id)
                error_not_predictable.append("Two or more arrival found for the trace with this id!")
                continue
            if len(csv_arrivals[csv_arrivals["trace_id"]==trace.id])==1:
                arrival = int((UTCDateTime(csv_arrivals[csv_arrivals["trace_id"]==trace.id]["trace_P_arrival_time"].iloc[0])-trace.stats.starttime) * trace.stats.sampling_rate)
        if arrival < 0:
            ids_not_predictable.append(trace.id)
            error_not_predictable.append("Unable to find a valid P arrival")
            continue
        
        # Verify sampling rate
        if abs(trace.stats.sampling_rate - sampling_rate) > 0.1:
            ids_not_predictable.append(trace.id)
            error_not_predictable.append("Trace with sampling rate different to 100Hz")
            continue

        semi_amp = 200
        # Verify enough samples are present
        if arrival<semi_amp or arrival>len(trace.data)-semi_amp:
            ids_not_predictable.append(trace.id)
            error_not_predictable.append("Trace with not enough point before or after the arrival")
            continue

        ids_predictable.append(trace.id)
        data[i,:] = trace.data[arrival-semi_amp:arrival+semi_amp]
        arrivals.append(arrival)
        i+=1
    pd_pred = pd.DataFrame.from_dict({"id_predictable":ids_predictable,"trace_P_arrival_sample":arrivals})
    pd_not_pred = pd.DataFrame.from_dict({"id_not_predictable":ids_not_predictable, "error":error_not_predictable})
    if len(data) <1:
        print("WARNING: no data is predictable")        
    return data[:len(ids_predictable),:], pd_pred, pd_not_pred

def demean(data,semiamp=200):
    lung = len(data[0])
    data = data - np.mean(data[ : , lung//2-semiamp : lung//2-5], axis=1).reshape(len(data),1)
    return data

def normalize(data,threshold=20):
    lung = len(data[0])
    data = data * 1.0                 
    sism_0_arr = data[:,0:lung//2-5]
    data = data / (threshold * np.max([np.max(sism_0_arr,axis=1),-np.min(sism_0_arr,axis = 1)], axis = 0).reshape(len(sism_0_arr),1))
    data[data > 1.0] = 1.0
    data[data < -1.0] = -1.0
    data = data / (np.max([np.max(data,axis=1),-np.min(data,axis = 1)], axis = 0).reshape(len(data),1))
    return data

harrival = """Optional: CSV file where P-wave arrivals are specified. The structure must be as follows: trace_id, trace_P_arrival_sample (int), trace_P_arrival_time (UTCDateTime).
Only one of the two column, either '...arrival_sample' or '...arrival_time', is required. If both are provided, arrival_sample will be considered."""
parser = argparse.ArgumentParser()

parser.add_argument("--model", type=str, help="REQUIRED: Path of the model used to make the predictions.")
parser.add_argument("--data", type=str, help="REQUIRED: Path of the input data. Can accept wildcards for sac or mseed formats")
parser.add_argument("--format", type=str, help="REQUIRED: input data file format. Accepted values are 'sac' or 'mseed'")
parser.add_argument("--arrivals", type=str, default={}, help=harrival)
parser.add_argument("--batch_size", type=int, default=16, help="Optional: batch size (default=1)")
parser.add_argument("--demean", type=str, default="true", help="Optional: if 'true', data will be demeaned. Any other value is interpreted as 'false'. RECOMANDED TO DEMEAN (default='true')")
parser.add_argument("--normalize", type=str, default="true", help="Optional: if 'true', data will be cut and normalized. Any other value is interpreted as 'false'. RECOMANDED TO NORMALIZE (default='true')")
parser.add_argument("--results_dir", type=str, default=None, help="Optional: Folder where to store the results. If not provided, a folder in the current path is created")



args = parser.parse_args()

model_path = args.model
model = tf.keras.models.load_model(model_path)



if args.format.lower() == "mseed":
    data, pd_pred, pd_not_pred = read_mseed(args.data, args.arrivals)
elif args.format.lower() == "sac":
    data, pd_pred, pd_not_pred = read_sac(args.data, args.arrivals)
else:
    print("No valid format is provided")
    exit()
# data          --> np.array of shape (n_traces, 160)
# pd_pred       --> pd dataframe, contains id of predictable waveforms with their respective arrival considered and predictions
# pd_not_pred   --> pd dataframe, contains id of not_predictable waveforms with the motivation

# Get the current date and time to create the folder where to store the outcomes.
current_time = str(datetime.now())
current_time = current_time.replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
try:
    os.mkdir(f"{args.results_dir}/results_{current_time}")
    path = f"{args.results_dir}/results_{current_time}"
except:
    if args.results_dir is not None:
        print(f"The path provided ('{args.results_dir}') is not a valid path to store the results. Creating a folder in the current path")
    else:
        print(f"No path to store the results provided. Creating a folder in the current path")
    os.mkdir(f"results_{current_time}")
    path = f"results_{current_time}"


if len(data)<1:
    print("Number of predictable traces equal to 0. Exit")
    pd_pred.to_csv(f"{path}/waveforms_predicted.csv",index=False)
    pd_not_pred.to_csv(f"{path}/waveforms_not_predicted.csv",index=False)
    exit()

if args.demean.lower() == "true":
    data = demean(data)
else:
    print("WARNING: Not demeaning the waveforms. The option is correct only if they are already provided demeaned.")
if args.normalize.lower() == "true":
    data = normalize(data)
else:
    print("WARNING: Not normalizing the waveforms. The option is correct only if they are already provided normalized.")

semi_amp = len(data[0])//2
y = model.predict(data[:,semi_amp-80:semi_amp+80], batch_size=args.batch_size)
y.reshape(max(y.shape))

pd_pred["prediction"] = y

pd_pred.to_csv(f"{path}/waveforms_predicted.csv",index=False)
pd_not_pred.to_csv(f"{path}/waveforms_not_predicted.csv",index=False)
