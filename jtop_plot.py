from matplotlib import pyplot as plt
import pandas as pd
from pathlib import Path
from jtop import jtop
import matplotlib.dates as mdates

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def main(interval: int):

    # read log files
    log_files = list(Path("./logs").glob('*.log*'))
    dfs = [pd.read_csv(log, skiprows=lambda i: i % interval != 0) for log in log_files]
    df = pd.concat(dfs, ignore_index=True)

    # set column names
    with jtop() as jetson:
        key = [str(k) for k in jetson.stats.keys()]
    print("keys:", ",".join(key))
    df.columns = key

    df['time'] = pd.to_datetime(df['time'])

    col1 = 'steelblue'
    col2 = 'orange'
    total_memory = 7.5

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111)
    ax.set_title('CPU/RAM Consumption')
    ax.set_xlabel('Date')
    ax.set_ylabel('CPU', color=col1)
    ax.plot(df['time'], sum(df[f'CPU{i+1}'] for i in range(6)), color=col1)

    ax2 = ax.twinx()
    ax2.plot(df['time'], df['RAM']*total_memory, color=col2)
    ax2.set_ylabel('RAM', color=col2, fontsize=16)


    seclocator = mdates.SecondLocator(bysecond=[20, 40]) 
    minlocator = mdates.MinuteLocator(byminute=range(0, 60, 15))
    hourlocator = mdates.HourLocator(byhour=range(0, 24, 2))
    ax.xaxis.set_minor_locator(minlocator)
    ax.xaxis.set_major_locator(hourlocator)
    ax.tick_params(axis='x', labelrotation=45)

    plt.show()

if __name__ == "__main__":

    # TODO: add start time and endtime logging
    
    import argparse
    parser = argparse.ArgumentParser(description='Simple jtop logger')
    parser.add_argument('--interval', type=int, default=60)
    args = parser.parse_args()
    main(args.interval)