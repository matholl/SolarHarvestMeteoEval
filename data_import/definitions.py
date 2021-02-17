###############################################################################
# Input, ManualInput = 0 => No, ManualInput = 1 => Yes
def manInput(manualInput):
    class manualInput:
        def __init__(self, year, firstMonthOfMeasurement, lastMonthOfMeasurement):
            self.year = year
            self.firstMonthOfMeasurement = firstMonthOfMeasurement
            self.lastMonthOfMeasurement = lastMonthOfMeasurement
    dataSet2009 = manualInput(2009, 1, 12)
    # More specific testrun
    startOfMonthsloop = dataSet2009.firstMonthOfMeasurement
    endOfMonthsloop = dataSet2009.lastMonthOfMeasurement + 1
    return dataSet2009.year, dataSet2009.firstMonthOfMeasurement, dataSet2009.lastMonthOfMeasurement, startOfMonthsloop, endOfMonthsloop
    
###############################################################################
# Definitions
def definitions():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',\
              'August', 'September', 'October', 'November', 'December']
    daysPerMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    minPerMonth = [x * 24 * 60 for x in daysPerMonth]
   
    return months, daysPerMonth, minPerMonth