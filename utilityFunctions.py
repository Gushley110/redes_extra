import appConstants

def BuildDataSourceString(sourceName, typeName, 
    threshold = appConstants.RRD_THRESHOLD,
    sampleMin = appConstants.RRD_UNKNOWN,
    sampleMax = appConstants.RRD_UNKNOWN):

    return 'DS:{0}:{1}:{2}:{3}:{4}'.format(sourceName, 
        typeName, threshold, sampleMin, sampleMax)

