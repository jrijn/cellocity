from cellocity.channel import Channel
import tifffile
from pathlib import Path
import statistics

my_filename = "E:\EXP-21-BT0437\LB_MSS109_0min_100ms_1\Default\img_channel000_position000_time000000001_z000.tif"
chToAnalyze = 0  # 0-based indexing of channels
savepath = Path("E:\EXP-21-BT0437\LB_MSS109_0min_100ms_1")

#safely load file
with tifffile.TiffFile(my_filename, multifile=False) as tif:

    #strips ome.tif from filename
    label = my_filename.split(".")[0]
    channelName = label + "_Ch" + str(chToAnalyze + 1)
    channel_0 = Channel(chToAnalyze, tif, name=channelName)

    # Check the intended frame interval.
    finterval_s = round(channel_0.getIntendedFrameInterval_ms() / 1000, 2)
    frames_per_min = round(60 / finterval_s, 2)
    tunit = 's'
    print(
        "Intended dimensions: frame interval {:.2f}s, {:.2f} frames/min, pixel size: {:.2f} um ".format(
            finterval_s, frames_per_min, channel_0.pxSize_um))

    # Check actual frame interval from metadata.
    # actual_interval = (statistics.mean(channel_0.getActualFrameIntevals_ms()) / 1000)
    # print("Actual frame interval is: {:.2f} s".format(actual_interval))
    # print(channel_0.getActualFrameIntevals_ms())
    
    page = channel_0.pages[0]
    print("Is micromanager: {}, number of pages: {}".format(tif.is_micromanager, len(channel_0.pages)))
    print("Metadata: \n{}".format(tif.micromanager_metadata))
    print(page.tags)
    print(page.tags.get("IJMetadata"))
    print()
    # page.tags["MicroManagerMetadata"].value["ElapsedTime-ms"]
    # ImageDescription
    # IJMetadata