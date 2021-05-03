import json
import statistics
import os


def readdirfiles(directory):
    """Import tiff files from a directory.
    This function reads all .tiff files from a directory and it's subdirectories and returns them as a list of
    hyperstacks.

    Args:
        directory: The path to a directory containing the tiff files.

    Returns:
        A list of filepaths.
    """
    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(directory):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    return listOfFiles


def meanfinterval(jdata, findkey = "ElapsedTime-ms"):
    keys = list(jdata.keys())
    out = []
    for key in keys:
            if findkey in jdata[key].keys(): out.append(jdata[key][findkey])
    outdiff = [j-i for i, j in zip(out[:-1], out[1:])]
    return statistics.mean(outdiff)


def medianfinterval(jdata, findkey = "ElapsedTime-ms"):
    keys = list(jdata.keys())
    out = []
    for key in keys:
            if findkey in jdata[key].keys(): out.append(jdata[key][findkey])
    outdiff = [j-i for i, j in zip(out[:-1], out[1:])]
    return statistics.median(outdiff)


def main():
    files = readdirfiles("E:\EXP-21-BT0437")
    out = {}
    for file in files:
        if file.endswith("metadata.json"):
            jdata = json.loads(open(file).read())
            filename = jdata['Summary']['Prefix']
            meantime = meanfinterval(jdata)
            mediantime = medianfinterval(jdata)
            percVariance = ((meantime-mediantime)/meantime)*100
            out[filename] = meantime
            print("{} : {}, {}, {}%".format(filename, round(meantime, 2), round(mediantime, 2), round(percVariance, 2)))
    # print(out)


main()
