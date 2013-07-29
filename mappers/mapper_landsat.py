# Name:        mapper_landsat
# Purpose:     Mapping for LANDSAT.tar.gz
# Authors:      Anton Korosov
# Licence:      This file is part of NANSAT. You can redistribute it or modify
#               under the terms of GNU General Public License, v.3
#               http://www.gnu.org/licenses/gpl-3.0.html

from vrt import VRT
import tarfile

try:
    from osgeo import gdal
except ImportError:
    import gdal

class Mapper(VRT):
    ''' Mapper for LANDSAT3,4,5,6,7.tar.gz files'''

    def __init__(self, fileName, gdalDataset, gdalMetadata, **kwargs):
        ''' Create LANDSAT VRT '''
        # try to open .tar or .tar.gz or .tgz file with tar
        tarFile = tarfile.open(fileName)

        tarNames = tarFile.getnames()
        print tarNames
        metaDict = []
        for tarName in tarNames:
            if ((tarName[0] == 'L' or tarName[0] == 'M') and
               (tarName[-4:] == '.TIF' or tarName[-4:] == '.tif')):
                print tarName
                bandNo = tarName[-6:-4]
                metaDict.append({
                    'src': {'SourceFilename': '/vsitar/%s/%s' % (fileName, tarName), 'SourceBand':  1},
                    'dst': {'wkv': 'toa_outgoing_spectral_radiance', 'suffix': bandNo}})
        print metaDict
        tmpName = metaDict[0]['src']['SourceFilename']
        print tmpName
        gdalDatasetTmp = gdal.Open(tmpName)
        # create empty VRT dataset with geolocation only
        VRT.__init__(self, gdalDatasetTmp, **kwargs)

        # add bands with metadata and corresponding values to the empty VRT
        self._create_bands(metaDict)
