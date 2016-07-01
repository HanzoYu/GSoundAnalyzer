class Paths:
    """Class to hold paths used by several other modules
    
    Attributes:
        dataDir (str): Path of a directory containing data that needs to be analyzed
        outFile (str): Path of a file to where output should be written
    """
    def __init__(self):
        """Set to default values"""
        self.dataDir = '/mnt/cluster/delta/home/yu_pe/GraSound_Data_PFC2015/D2/'
        self.outFile = '/home/kamp_al/thesis/gsound/testout.gsound'

    def getDataDir(self):
        """Return the path to the data directory
        
        Raises:
            Exception: Exception when none is set
        
        Returns:
            str: path to data directory
        """
        if self.dataDir == '':
            # TODO error handling here
            raise Exception('No valid data directory set')
        else:
            return self.dataDir

    def getOutFile(self):
        """Return the path to the output file
        
        Raises:
            Exception: Exception when none is set
        
        Returns:
            str: path to output file
        """
        if self.outFile == '':
            raise Exception('No valid output file set')
        else:
            return self.outFile

    # def setOutFile(self, fname):
    #     if isOutFile(fname):
    #         self.outFile = fname
    #     else:
    #         raise Exception('Not a correct output file.')


paths = Paths()