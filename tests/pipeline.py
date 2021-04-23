from cellocity.channel import Channel
import tifffile
from pathlib import Path
import statistics

my_filename = "E:\EXP-21-BT0437\LB_MSS109_0min_100ms_1\Default\img_channel000_position000_time000000000_z000.tif"
chToAnalyze = 0  # 0-based indexing of channels
savepath = Path("E:\EXP-21-BT0437\LB_MSS109_0min_100ms_1")

#safely load file
with tifffile.TiffFile(my_filename, multifile=True) as tif:

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
    print(channel_0.getActualFrameIntevals_ms())

    # If the actual frame interval does not match the intended frame interval, use the actual interval.
    if not channel_0.doFrameIntervalSanityCheck():
        print("Intended frame interval does not match intended.\nFixing frame interval...")
        channel_0.fixFrameInterval()
    else: print("Intended frame interval is OK")

    #Trim channel to speed up the proces.
    # channel_0.trim(150,220)

    from cellocity.channel import MedianChannel
    gliding_median_channel_0 = MedianChannel(channel_0)

    from cellocity.analysis import FarenbackAnalyzer
    fb_analyzer_ch0 = FarenbackAnalyzer(channel = gliding_median_channel_0, unit = "um/h")
    fb_analyzer_ch0.doFarenbackFlow()

    from cellocity.analysis import FlowAnalysis
    flow_analysis_ch0 = FlowAnalysis(fb_analyzer_ch0)
    draw_flow_frame_options = {'step' : 20, 'scale' : 20, 'line_thicknes' : 2}
    flow_analysis_ch0.draw_all_flow_frames_superimposed(scalebarFlag=False, scalebarLength=10, **draw_flow_frame_options)
    flow_analysis_ch0.saveFlowAsTif(savepath)

    from cellocity.analysis import FlowSpeedAnalysis
    speed_analysis_ch0 = FlowSpeedAnalysis(fb_analyzer_ch0)
    speed_analysis_ch0.calculateSpeeds()
    speed_analysis_ch0.calculateAverageSpeeds()
    speed_analysis_ch0.saveArrayAsTif(outdir=savepath)
    speed_analysis_ch0.saveCSV(outdir=savepath, fname="mySpeeds.csv", tunit="s")