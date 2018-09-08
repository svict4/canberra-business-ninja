from __future__ import print_function
import sys
from geopy.distance import great_circle
import numpy as np
import pandas as pd
from glob import glob
import os

# from data_points import DataPoints
from config import base_directory


class Preprocessing:
    def __init__(self):
        self.data_directory = os.path.join(base_directory, '..', 'datasets2018')
        self.raw_data_folder = "../datasets2018"
        self.output_folder = "../src/data2018"

        # self.ag

        self.in_act_division_boundaries = "ACT_Division_Boundaries_data.csv"


        self.in_act_age = "2016Census_G01_ACT_POA.csv"


        # self.in_act_police_stations_locations = "ACT_Police_Station_Locations.csv"
        # self.in_act_hospital_locations = "Hospitals_in_the_ACT.csv"
        # self.in_act_public_toilets = "Public_Toilets_in_the_ACT.csv"
        # self.in_act_fitness_sites = "Fitness_Sites.csv"
        # self.in_act_cyclist_crashes = "Cyclist_Crashes.csv"
        # self.in_tafe_campus_locations = "ACT_TAFE_Campus_Locations.csv"
        # self.in_library_locations = "Library_Locations.csv"
        # self.in_arts_facilities = "ACT_Arts_Facilities_List.csv"
        # self.in_bbq = "Public_Barbeques_in_the_ACT.csv"
        # self.in_public_furniture = "Public_Furniture_in_the_ACT.csv"
        # self.in_playgrounds = "Town_And_District_Playgrounds.csv"
        # self.in_dog_parks = "Fenced_Dog_Parks.csv"
        # self.in_crime_stats = "ACT_CrimeStats_-_Jan2012_to_Mar2017"
        # self.in_bus_data = "Bus_Stops_July_2017.csv"
        #
        # self.out_act_police_stations_locations = "safety_distance_to_police_stations.data"
        # self.out_act_hospital_locations = "health_distance_to_hospitals.data"
        # self.out_act_public_toilets = "safety_distance_to_public_toilets.data"
        # self.out_act_fitness_sites = "health_distance_to_fitness_sites.data"
        # self.out_act_cyclist_crashes = "transport_cyclist_crashes.data"
        # self.out_tafe_campus_locations = "education_distance_to_tafe_campuses.data"
        # self.out_library_locations = "education_distance_to_libraries.data"
        # self.out_arts_facilities = "education_distance_to_art_facilities.data"
        # self.out_bbq = "green_spaces_distance_to_bbqs.data"
        # self.out_public_furniture = "green_spaces_distance_to_public_furniture.data"
        # self.out_playgrounds = "green_spaces_distance_to_playgrounds.data"
        # self.out_dog_parks = "green_spaces_distance_to_fenced_dog_parks.data"
        # self.out_crime_stats = "safety_crime_stats_last_2.5_years.data"
        # self.out_bus_data = "transport_bus_stops.data"

    def create_directory(self, file):
        """ create the path including the file """
        assert isinstance(file, str)
        assert str
        return os.path.join(self.data_directory, file)

    def process_act_division_boundaries(self):
        with open(self.raw_data_folder + "/" + self.in_act_division_boundaries) as input:
            ret_val = dict()
            lines = input.readlines()
            points = []
            for index, line in enumerate(lines):
                all_lat = 0.0
                all_lon = 0.0
                count = 0.0
                if index == 0:
                    continue
                sline = line.strip()
                division_name = sline[sline.find(')))",')+5:].split(",")[3]
                for coordinate in sline[sline.find("(((")+3: sline.find(")))")].split(","):
                    lat_lon = coordinate.strip().split(" ")
                    all_lon = all_lon + (float)(lat_lon[0])
                    all_lat = all_lat + (float)(lat_lon[1])
                    count = count + 1.0
                lon = all_lon / count
                lat = all_lat / count
                point = [lon, lat]
                ret_val[division_name] = point
                points.append(point)
        self.write_collection_of_points_to_file(
            points,
            self.output_folder + "/division_centers.json"
        )
        return ret_val

    def read_age_data(self):
        """ read the age data """
        path = os.path.join(base_directory, '..', 'datasets2018', self.in_act_age)
        df = pd.read_csv(path)
        assert True


    def read_census_data(self):
        """ compile the many census data files """
        # path = os.path.join(base_directory, '..', 'dataset2018', '*')
        path = os.path.join(base_directory, '..', 'datasets2018', '*')
        files = glob(path)
        dfs = []
        for file in files:
            # file_name = file.split(os.path.sep)[-1]
            # 2016Census_G01_ACT_POA
            # data_file = re.search(r"2016Census_G01_ACT_POA\.csv\Z", file_name)
            df = pd.read_csv(
                file
            )
            dfs.append(df)
        df_compiled = pd.concat(
            dfs,
            join='outer',
            # axis=1,
            sort=True,
        )
        assert True



    @staticmethod
    def write_collection_of_points_to_file(points, file):
        with open(file, 'w+') as output_file:
            output_file.write('{"type": "FeatureCollection", "features": [')
            for index, point in enumerate(points):
                output_file.write(
                    '{"type": "Feature", "geometry": { "type": "Point", "coordinates": [' + str(point[0]) + ',' +
                    str(point[1]) + ']}, "properties": {"marker-size": "small"}}\n'
                )
                if len(points) != index + 1:
                    output_file.write(',')
            output_file.write(']}')

    @staticmethod
    def get_distance(a, b):
        return great_circle(a, b).kilometers

    def print_distance_from_points_to_district_center(self, points, division_centers, path_to_file, invert=False):
        variable = (path_to_file[path_to_file.rfind('/') + 1:len(path_to_file) - 3])
        with open(path_to_file, 'w+') as file:
            points_to_write = []
            for center in division_centers.keys():
                min_distance = sys.maxint
                dc = division_centers[center]
                for pd in points:
                    # print(dc, pd)
                    dist = self.get_distance(dc, pd)
                    if dist < min_distance:
                        min_distance = dist
                points_to_write.append([center, dc[0], dc[1], min_distance])

            np_points_to_write = np.array(points_to_write)
            min_dist = min(np_points_to_write[:, 3])
            max_dist = max(np_points_to_write[:, 3])

            # file.write("export const " + variable + " = [")
            for point in points_to_write:
                file.write("[{},{},{},{}]\n".format(
                    point[0],
                    point[1],
                    point[2],
                    self.normalize(float(min_dist), float(max_dist), float(point[3]), invert))
                )
            # file.write("]")

    @staticmethod
    def normalize(min, max, current, invert=False):
        ret_val = (float(current - min) / float(max - min)) * float(100.0)
        if invert:
            ret_val = 100.0 - ret_val
        return ret_val



    def execute(self):
        division_centers = self.process_act_division_boundaries()
        self.process_police_stations_locations(division_centers)
        self.process_hospital_locations(division_centers)
        self.process_fitness_sites(division_centers)
        self.process_public_toilets(division_centers)
        self.process_cyclist_crashes(division_centers)
        self.process_tafe_campus_locations(division_centers)
        self.process_library_locations(division_centers)
        self.process_arts_facilities(division_centers)
        self.process_bbq(division_centers)
        self.process_public_furniture(division_centers)
        self.process_playgrounds(division_centers)
        self.process_fenced_dog_park(division_centers)
        self.process_crime_stats(division_centers)
        self.process_bus_data(division_centers)

if __name__ == "__main__":
    preproc = Preprocessing()
    preproc.read_age_data()
    # preproc.execute()
    assert True
