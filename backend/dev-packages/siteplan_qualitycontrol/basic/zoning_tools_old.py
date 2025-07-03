"""
Functions to get the zoning information based on the APN or address information.
"""

import os
import re
import json
import numpy as np
from urllib.request import Request, urlopen
import pandas as pd
from pandas import DataFrame
from pathlib import Path

from siteplan_qualitycontrol.utils import global_var


def apn_coordinate_gen(
        apn: str = None):
    """
    Given an APN number, get the geometric coordinate.

    @param: apn: string containing the APN number.

    @return: apn_exist: boolean indicating if the APN exist.
    @return: apn_city: city for the APN, empty string if APN not exist.
    @return: apn_county: county for the APN, empty string if APN not exist. 
    @return: apn_address: address for the APN, empty string if APN not exist. 
    @return: x: x coordinate for the APN, 0 if APN not exist.
    @return: y: y coordinate for the APN, 0 if APN not exist.
    """
    apn = apn.replace("-", "")
    apn_url_list = {"MARICOPA": f"https://services.arcgis.com/ykpntM6e3tHvzKRJ/arcgis/rest/services/Parcels_view/FeatureServer/0/query?f=json&where=APN%20LIKE%20%27{apn}%25%27&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=APN_DASH%2COWNER_NAME%2CPHYSICAL_ADDRESS%2CMAIL_ADDRESS%2CMAIL_ADDR1%2CMAIL_CITY%2CMAIL_STATE%2CMAIL_ZIP%2CPHYSICAL_STREET_NUM%2CPHYSICAL_STREET_DIR%2CPHYSICAL_STREET_NAME%2CPHYSICAL_STREET_TYPE%2CPHYSICAL_CITY%2CPHYSICAL_ZIP%2CLATITUDE%2CLONGITUDE%2CDEED_NUMBER%2CDEED_DATE%2CSALE_DATE%2CSALE_PRICE%2CMCRNUM%2CMCR_BOOK%2CMCR_PAGE%2CSUBNAME%2CLAND_SIZE%2CLOT_NUM%2CSTR%2CCONST_YEAR%2CLIVING_SPACE%2CINCAREOF%2CTAX_YR_CUR%2CFCV_CUR%2CLPV_CUR%2CTAX_YR_PREV%2CFCV_PREV%2CLPV_PREV%2CLC_CUR%2CLC_PREV%2CPUC%2CJURISDICTION%2CCITY_ZONING%2CFLOOR%2CAPN%2COBJECTID&orderByFields=APN%20ASC&outSR=102100", 
                    "PINAL": f"https://gis.pinal.gov/mapping/rest/services/TaxParcels/MapServer/3/query?f=json&where=LOWER(PARCELID)%20LIKE%20%27{apn}%25%27&returnGeometry=true&spatialRel=esriSpatialRelIntersects&maxAllowableOffset=0.010583354500042334&outFields=*&outSR=102100&resultRecordCount=25",
                    "COCONINO": f"https://services1.arcgis.com/Rlvx5g8pKeK13apH/arcgis/rest/services/Coconino_County_Parcels/FeatureServer/0/query?f=json&where=(ALTERNATEAPN%20%3D%202)%20AND%20(APN%20LIKE%20%27{apn}%25%27)&returnGeometry=true&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22edit%22%7D"}
    city_name_list = {"MARICOPA": 'PHYSICAL_CITY',
                      "PINAL": 'PSTLCITY', 
                      "COCONINO": 'SITUS_CITY'}
    address_name_list = {"MARICOPA": 'PHYSICAL_ADDRESS',
                         "PINAL": 'SITEADDRESS', 
                         "COCONINO": 'SITUS'}
    # go through counties
    apn_county = ""
    apn_city = ""
    apn_address = ""
    x = 0
    y = 0
    apn_exist = True
    for (county, apn_url) in apn_url_list.items():
        req = Request(url=apn_url,headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        results = json.loads(html)['features']

        if len(results) == 0:
            apn_exist = False
            continue
        else:
            # for now, the average of all ring coordinates are taken
            # possible problem: for irregular shape, this "center" might locate outside the site
            # for some properties, there are some "holes" inside, which give the property more than one set of "ring"
            x_list = []
            y_list = []
            # test: list all the (x, y) pairs in the ring and take the average
            for ring in results[0]['geometry']['rings']:
                for x_, y_ in ring:
                    x_list.append(x_)
                    y_list.append(y_)
            x = np.array(x_list).mean()
            y = np.array(y_list).mean()
            apn_city = results[0]['attributes'][city_name_list[county]]
            apn_county = county
            apn_address = results[0]['attributes'][address_name_list[county]]
            break

    return apn_exist, apn_city, apn_county, apn_address, x, y
    

def address_coordinates_gen(
        address: str = None):
    """
    Given an address, get the geometric coordinate.

    @param: apn: string containing the APN number.

    @return: detect_address: Corrected address, for case with missing city, etc. 
    @return: x: x coordinate for the address.
    @return: y: y coordinate for the address.
    """
    address = address.replace("&", "and")
    state_name_list = ["Arizona", "AZ"]
    if not any(re.search(substring, address, re.IGNORECASE) for substring in state_name_list):
        address = address + ", Arizona"
    final_add = '%20'.join((address+' ').replace(',','').split())
    street_url = 'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?SingleLine='\
    +final_add+'&maxLocations=1&outFields=Addr_type%2CMatch_addr%2CStAddr%2CCity&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D&f=json'
    req = Request(
        url=street_url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    html = urlopen(req).read()
    if len(json.loads(html)['candidates']) > 0:
        results = json.loads(html)['candidates'][0]['location']
        detect_address = json.loads(html)['candidates'][0]['address']
        x, y = results['x'], results['y']
    else:
        detect_address = "Arizona"
        x = 0
        y = 0

    return detect_address, x, y


def get_zone_info_city(
        city: str = None,
        x: float = None, 
        y: float = None,):
    """
    Given city and (x, y) cooridnates, get the zoning information.
    This is for case when location of (x, y) belong to city.

    @param: city: string of city name.
    @return: x: x coordinate of the location.
    @return: y: y coordinate of the location.

    @return: city: city name.
    @return: zone: zoning inforamtion.
    """
    # from the dtected address, get the city name
    # city = detected_address.replace(" ", "").split(",")[1]

    # Todo: the xmin, ymin, xmax, ymax, may need modification.
    x_min = x_max = x
    y_min = y_max = y

    zone_url_list = {"SCOTTSDALE": f"https://maps.scottsdaleaz.gov/arcgis/rest/services/OpenData/MapServer/24/query?f=json&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D&maxAllowableOffset=76.43702828515632&orderByFields=OBJECTID&outFields=OBJECTID%2Cfull_zoning&outSR=102100&resultType=tile&returnCentroid=true&returnExceededLimitFeatures=false&spatialRel=esriSpatialRelIntersects&where=1%3D1&geometryType=esriGeometryEnvelope&inSR=102100", 
                     "PHOENIX": f"https://maps.phoenix.gov/pub/rest/services/Public/Zoning/MapServer/0/query?f=json&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D&orderByFields=OBJECTID&outFields=LABEL1%2COBJECTID&outSR=102100&quantizationParameters=%7B%22extent%22%3A%7B%22spatialReference%22%3A%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D%2C%22xmin%22%3A{x_min}%2C%22ymin%22%3A3{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D%2C%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A0.07464553543472296%7D&resultType=tile&returnCentroid=true&returnExceededLimitFeatures=false&spatialRel=esriSpatialRelIntersects&where=1%3D1&geometryType=esriGeometryEnvelope&inSR=102100", 
                     "ELOY": f"https://services7.arcgis.com/VfOwt1fngp5cVBlk/arcgis/rest/services/EloyZoning_view_Public/FeatureServer/0/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A0.5971642835609073%2C%22extent%22%3A%7B%22xmin%22%3A754279.885170605%2C%22ymin%22%3A598881.4373359606%2C%22xmax%22%3A844260.7854330726%2C%22ymax%22%3A683908.4366797879%2C%22spatialReference%22%3A%7B%22wkid%22%3A2223%2C%22latestWkid%22%3A2223%7D%7D%7D", 
                     "GLENDALE": f"https://gismaps.glendaleaz.com/gisserver/rest/services/AdminAreas/Misc_Glendale_Areas/MapServer/9/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A2.388657133972221%2C%22extent%22%3A%7B%22xmin%22%3A-17746700%2C%22ymin%22%3A-44067300%2C%22xmax%22%3A628438.401902888%2C%22ymax%22%3A981568.4954068214%2C%22spatialReference%22%3A%7B%22wkid%22%3A2868%2C%22latestWkid%22%3A2868%2C%22xyTolerance%22%3A0.0032808398950131233%2C%22zTolerance%22%3A0.001%2C%22mTolerance%22%3A0.001%2C%22falseX%22%3A-17746700%2C%22falseY%22%3A-44067300%2C%22xyUnits%22%3A3048%2C%22falseZ%22%3A0%2C%22zUnits%22%3A1%2C%22falseM%22%3A0%2C%22mUnits%22%3A1%7D%7D%7D", 
                     "MESA": f"https://services2.arcgis.com/1gVyYKfYgW5Nxb1V/arcgis/rest/services/Zoning/FeatureServer/2/query?f=json&geometry={x_min}%2C{y_min}4%2C{x_max}%2C{y_max}&maxRecordCountFactor=4&resultOffset=0&resultRecordCount=8000&where=1%3D1&orderByFields=OBJECTID&outFields=OBJECTID%2CZoning&quantizationParameters=%7B%22extent%22%3A%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D%2C%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A1.1943285669555674%7D&resultType=tile&spatialRel=esriSpatialRelIntersects&geometryType=esriGeometryEnvelope&defaultSR=102100", 
                     "FLAGSTAFF": f"https://gis.flagstaffaz.gov/arcgisserver/rest/services/Planning_Info_Map/MapServer/dynamicLayer/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=ORD_NUM%2CREGULATIONDESCRIPTION%2CReference%2COBJECTID%2CREGULATIONCLASSIFICATION&outSR=102100&layer=%7B%22source%22%3A%7B%22type%22%3A%22mapLayer%22%2C%22mapLayerId%22%3A13%7D%7D", 
                     "PEORIA": f"https://gis.peoriaaz.gov/arcgis/rest/services/CD/Peoria_Zoning/MapServer/20/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=OBJECTID%2CCASE_NUM%2CORD_NUM%2CZONE_CODE%2CGIS_MODDATE%2CACRES%2CDOCLINK%2CMCR_ZONING&outSR=102100", 
                     "TEMPE": f"https://gis.tempe.gov/arcgis/rest/services/Open_Data/Zoning_Districts/FeatureServer/0/query?f=json&geometry=%7B%22xmin%22%3A-12460458.602936026%2C%22ymin%22%3A3950265.621779863%2C%22xmax%22%3A-12459847.106709745%2C%22ymax%22%3A3950877.1180061437%7D&orderByFields=OBJECTID&outFields=OBJECTID%2CZoningCode&outSR=102100&quantizationParameters=%7B%22extent%22%3A%7B%22spatialReference%22%3A%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D%2C%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D%2C%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A1.1943285669555674%7D&resultType=tile&returnCentroid=true&returnExceededLimitFeatures=false&spatialRel=esriSpatialRelIntersects&where=1%3D1&geometryType=esriGeometryEnvelope&inSR=102100", 
                     "GILBERT": f"https://maps.gilbertaz.gov/arcgis/rest/services/OD/Growth_Development_Maps_1/MapServer/8/query?f=json&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D&orderByFields=OBJECTID&outFields=OBJECTID%2CZCODE&outSR=102100&quantizationParameters=%7B%22extent%22%3A%7B%22spatialReference%22%3A%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D%2C%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D%2C%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A2.388657133911135%7D&resultType=tile&returnCentroid=true&returnExceededLimitFeatures=false&spatialRel=esriSpatialRelIntersects&where=1%3D1&geometryType=esriGeometryEnvelope&inSR=102100", 
                     "AVONDALE": f"https://gisweb.avondaleaz.gov/server/rest/services/Planning/Zoning/MapServer/6/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=CASENO%2CCOMMONAME%2CSUBTYPE%2CZONETYPE%2CZONEDIST%2COrdinanceDocLink%2CDocLink%2CAssociatedCASENOs%2COBJECTID%2CPOLY_ID%2CCOMMENT%2CBUBBLE%2CShape_Length%2CShape_Area&outSR=102100"}
    zone_name_list = {"SCOTTSDALE": 'full_zoning', 
                      "PHOENIX": 'LABEL1', 
                      "ELOY": 'Zoning', 
                      "GLENDALE": 'BASE_ZONE', 
                      "MESA": 'Zoning', 
                      "FLAGSTAFF": 'REGULATIONCLASSIFICATION', 
                      "PEORIA": 'ZONE_CODE', 
                      "TEMPE": 'ZoningCode', 
                      "GILBERT": 'ZCODE', 
                      "AVONDALE": 'ZONETYPE'} 

    zone_url = zone_url_list[city]
    req = Request(url=zone_url,headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    results = json.loads(html)['features']
    if len(results) == 0:
        zone = None
    else:
        zone = results[0]['attributes'][zone_name_list[city]]

    return city, zone


def get_zone_info_county(
        city: str = None, 
        county: str = None, 
        x: float = None, 
        y: float = None):
    """
    Given the city, county and (x, y) coordinate of a location, get the zoning information.
    If location belong to county, get zoning from county.
    If location belong to city, get zoning from city using function get_zone_info_city().

    @param: city: string containing city.
    @param: county: string containing county.
    @return: x: x coordinate of the location.
    @return: y: y coordinate of the location.

    @return: city: detected city.
    @return: county: detected county.
    @return: zone: detected zone.
    """
    # Todo: the xmin, ymin, xmax, ymax, may need modificaiton
    x_min = x_max = x
    y_min = y_max = y

    # pinal county
    # in pinal county, the county zoning map mark the zoning for city as city name
    if county == "PINAL":
        pinal_county_zones = {'1': 'CR-1A', '2': 'CR-1', '3': 'CR-2', '4': 'CR-3', '5': 'CR-4', '6': 'CR-5', \
        '7': 'SR', '8': 'SH', '9': 'CAR', '10': 'GR', '11': 'MH', '12': 'RV', '13': 'MHP', '14': 'RVP', '15': 'TR', \
        '16': 'CB-1', '17': 'CB-2', '18': 'CI-B', '19': 'CI-1', '20': 'CI-2', '21': 'Undesignated', '22': 'Multiple', \
        '23': 'RU-10', '24': 'RU-5', '25': 'RU-3.3', '26': 'RU-2', '27': 'RU-1.25', '28': 'RU-C', '29': 'R-43', '30': \
        'R-35', '31': 'R-20', '32': 'R-12', '33': 'R-9', '34': 'R-7', '35': 'MD', '36': 'MR', '37': 'AC-1', '38': 'AC-2', \
        '39': 'AC-3', '40': 'O-1', '41': 'O-2', '42': 'C-1', '43': 'C-2', '44': 'C-3', '45': 'I-1', '46': 'I-2', \
        '47': 'I-3', '48': 'MH-8', '49': 'MH-435', '50': 'PM/RV', '51': 'APACHE JUNCTION', '52': "CASA GRANDE", \
        '53': 'COOLIDGE', '54': 'ELOY', '55': 'FLORENCE', '56': 'KEARNY', '57': 'MAMMOTH', '58': 'MARANA', '59': 'MARICOPA', \
        '60': 'QUEEN CREEK', '61': 'SUPERIOR', '62': 'WINKELMAN'}

        county_zone_url = f"https://gis.pinal.gov/mapping/rest/services/Zoning_2010/MapServer/0/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A0.5971642835615913%2C%22extent%22%3A%7B%22xmin%22%3A611539.762204431%2C%22ymin%22%3A546275.5107313767%2C%22xmax%22%3A1152514.0770688802%2C%22ymax%22%3A903301.6016566455%2C%22spatialReference%22%3A%7B%22wkt%22%3A%22PROJCS%5B%5C%22NAD_1983_StatePlane_Arizona_Central_FIPS_0202_IntlFeet%5C%22%2CGEOGCS%5B%5C%22GCS_North_American_1983%5C%22%2CDATUM%5B%5C%22D_North_American_1983%5C%22%2CSPHEROID%5B%5C%22GRS_1980%5C%22%2C6378137.0%2C298.257222101%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0.0%5D%2CUNIT%5B%5C%22Degree%5C%22%2C0.0174532925199433%5D%5D%2CPROJECTION%5B%5C%22Transverse_Mercator%5C%22%5D%2CPARAMETER%5B%5C%22False_Easting%5C%22%2C700000.0%5D%2CPARAMETER%5B%5C%22False_Northing%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Central_Meridian%5C%22%2C-111.9166666666667%5D%2CPARAMETER%5B%5C%22Scale_Factor%5C%22%2C0.9999%5D%2CPARAMETER%5B%5C%22Latitude_Of_Origin%5C%22%2C31.0%5D%2CUNIT%5B%5C%22Foot%5C%22%2C0.3048%5D%5D%22%2C%22xyTolerance%22%3A0.0019293809336555%2C%22zTolerance%22%3A0.001%2C%22mTolerance%22%3A0.001%2C%22falseX%22%3A-17746700%2C%22falseY%22%3A-44067300%2C%22xyUnits%22%3A3048%2C%22falseZ%22%3A-100000%2C%22zUnits%22%3A10000%2C%22falseM%22%3A-100000%2C%22mUnits%22%3A10000%7D%7D%7D"
        req = Request(url=county_zone_url,headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        results = json.loads(html)['features']
        zone_number = results[0]['attributes']['ZONING']
        if zone_number <= 50:
            zone = pinal_county_zones[str(zone_number)]
            jurisdiction = county
            print("belong to county", county, zone)
        else:
            detected_city = pinal_county_zones[str(zone_number)]
            jurisdiction = detected_city
            if city.upper() != detected_city.upper():
                # sometimes, the mail address city are not the jurisdiction city
                city, zone = get_zone_info_city(detected_city, x, y)
                print("city detected not match", city, detected_city)
            else:
                city, zone = get_zone_info_city(city, x, y)
                print("belong to city, check city", city, zone)
    # coconino county
    # in coconino county, the zoning for city is empty
    elif county == "COCONINO":
        county_zone_url = f"https://services1.arcgis.com/Rlvx5g8pKeK13apH/arcgis/rest/services/County_Zoning/FeatureServer/0/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A19.109257071269987%2C%22extent%22%3A%7B%22xmin%22%3A288192.85597112775%2C%22ymin%22%3A1209390.104330711%2C%22xmax%22%3A1050449.010170605%2C%22ymax%22%3A2184144.61581365%2C%22spatialReference%22%3A%7B%22wkid%22%3A2223%2C%22latestWkid%22%3A2223%7D%7D%7D"
        req = Request(url=county_zone_url,headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        results = json.loads(html)['features']
        if len(results) == 0:
            jurisdiction = city
            city, zone = get_zone_info_city(city, x, y)
            print("belong to city, check city", city, zone)
        else:
            jurisdiction = county
            zone = results[0]['attributes']['ZONINGCODE']
            print("belong to county", county, zone)
    # maricopa county
    # in maricopa county, there is different link to check if the area belongs to a city or directly to the county
    elif county == "MARICOPA":
        # county_city_url = f"https://gis.maricopa.gov/arcgis/rest/services/IndividualService/City/MapServer/0/query?f=json&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D&maxAllowableOffset=0&outFields=CityName%2CFullCityName%2COBJECTID&spatialRel=esriSpatialRelIntersects&where=1%3D1&geometryType=esriGeometryEnvelope&inSR=102100&outSR=102100"
        county_city_url = f"https://services.arcgis.com/ykpntM6e3tHvzKRJ/arcgis/rest/services/Parcels_view/FeatureServer/0/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryEnvelope&inSR=102100&outFields=*&outSR=102100&resultType=tile&quantizationParameters=%7B%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A1.1943285668574048%2C%22extent%22%3A%7B%22xmin%22%3A-12616394.3919%2C%22ymin%22%3A3854950.876699999%2C%22xmax%22%3A-12365565.0318%2C%22ymax%22%3A4035096.9921000004%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D%7D%7D"
        req = Request(url=county_city_url,headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        results = json.loads(html)['features']
        # TODO: for cases of intersection of two streets, without direction such as NW, there will be no information fetched
        if len(results) == 0:
            jurisdiction = None
            zone = None
            print("no information detected")
        else:
            # detected_city = results[0]['attributes']['CityName']
            detected_city = results[0]['attributes']['JURISDICTION']
            if detected_city == "UNINCORPORATED MARICOPA COUNTY":
                jurisdiction = county
                objectid= results[0]['attributes']['OBJECTID']
                county_zone_url = f"https://gis.maricopa.gov/arcgis/rest/services/PND/PlanNet/MapServer/21/query?f=json&objectIds={objectid}&outFields=*&returnZ=true&spatialRel=esriSpatialRelIntersects"
                # county_zone_url = f"https://gis.maricopa.gov/arcgis/rest/services/PND/PlanNet/MapServer/21/query?f=json&geometry=%7B%22xmin%22%3A{x_min}%2C%22ymin%22%3A{y_min}%2C%22xmax%22%3A{x_max}%2C%22ymax%22%3A{y_max}%7D&orderByFields=OBJECTID&outFields=OBJECTID%2CZONE&outSR=102100&quantizationParameters=%7B%22extent%22%3A%7B%22spatialReference%22%3A%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D%2C%22xmin%22%3A-12523442.714242995%2C%22ymin%22%3A3913575.8482029866%2C%22xmax%22%3A-12445171.197278995%2C%22ymax%22%3A3991847.365166988%7D%2C%22mode%22%3A%22view%22%2C%22originPosition%22%3A%22upperLeft%22%2C%22tolerance%22%3A152.87405657031263%7D&resultType=tile&returnCentroid=true&returnExceededLimitFeatures=false&spatialRel=esriSpatialRelIntersects&where=1%3D1&geometryType=esriGeometryEnvelope&inSR=102100"
                req = Request(url=county_zone_url,headers={'User-Agent': 'Mozilla/5.0'})
                html = urlopen(req).read()
                results = json.loads(html)['features']
                zone = results[0]['attributes']['ZONE']
                print("belong to county", county, zone)
            elif city.upper() != detected_city.upper():
                jurisdiction = detected_city
                city, zone = get_zone_info_city(city, x, y)
                print("city detected not match", city, detected_city)
            else:
                jurisdiction = detected_city
                city, zone = get_zone_info_city(city, x, y)
                print("belong to city, check city", city, zone)

    return city, county, zone, jurisdiction


def apn_zoning_info_generate(
        apn: str = None, 
        city: str = None):
    """
    Given apn information, generate zoning information.
    
    @param: apn: string containing APN.
    @param: city: string containing city.

    @return: zone: zoning information.
    """
    apn_exist, apn_city, apn_county, apn_address, x, y = apn_coordinate_gen(apn)
    if city != None and apn_city != city:
        return {"status": "fail", 
                "error message": f"address does not belong to {city}, it belongs to {apn_city}"}
    if apn_exist:
        city, county, zone, jurisdiction = get_zone_info_county(apn_city, apn_county, x, y)
        if zone == None:
            return {"status": "fail", 
                    "error message": "no zoning detected", 
                    "source": "APN", 
                    "city": city, 
                    "county": county, 
                    "zone": zone, 
                    "jurisdiction": jurisdiction}
    else:
        return {"status": "fail", 
                "error message": "apn not exist"}
    # return a information dictionary
    return_info = {"status": "succeed", 
                   "source": "APN", 
                   "city": city, 
                   "county": county, 
                   "zone": zone, 
                   "jurisdiction": jurisdiction}
    return return_info


def address_zoning_info_generate(
        address: str = None, 
        city: str = None):
    """
    Given address, generate zoning information.

    @param: address: string containing address.
    @param: city: string containing city.

    @return: zone: zoning information.
    """
    detected_address, x, y = address_coordinates_gen(address)
    print(detected_address)
    # for some cases, there is a direction notation in the address.
    # we manully adjust the coordinates based on the address
    if "NE" in address.split(" ")[0]:
        # north east of the intersection
        x = x + 100
        y = y + 100
    if "NW" in address.split(" ")[0]:
        # north west of the intercestion
        x = x - 100
        y = y + 100
    if "SE" in address.split(" ")[0]:
        # south east of the intersection
        x = x + 100
        y = y - 100
    if "SW" in address.split(" ")[0]:
        # south west of the intersection
        x = x - 100
        y = y - 100
    add_city = detected_address.split(",")[-3].replace(" ", "").upper()
    if city != None and add_city != city:
        return {"status": "fail", 
                "error message": f"address does not belong to {city}, it belongs to {add_city}"}
    add_county = global_var.CITY_COUNTY[add_city][0]
    city, county, zone, jurisdiction = get_zone_info_county(add_city, add_county, x, y)
    if zone == None:
        return {"status": "fail", 
                "error message": "no zoning detected", 
                "source": "ADDRESS", 
                "city": city, 
                "county": county, 
                "zone": zone, 
                "jurisdiction": jurisdiction}
    # return a information dictionary
    return_info = {"status": "succeed", 
                   "source": "ADDRESS", 
                   "city": city, 
                   "county": county, 
                   "zone": zone, 
                   "jurisdiction": jurisdiction}
    return return_info