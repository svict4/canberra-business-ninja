from __future__ import print_function
import sys
from geopy.distance import great_circle
import numpy as np
import pandas as pd
from glob import glob
import os
import re
from decimal import Decimal, ROUND_UP
from copy import deepcopy
import json
from collections import OrderedDict

# from data_points import DataPoints
from config import base_directory


class Preprocessing:
    def __init__(self):
        self.data_directory = os.path.join(base_directory, '..', 'datasets2018')
        self.raw_data_folder = "../datasets2018"
        self.output_folder = "../src/data2018"
        self.age_path = os.path.join(base_directory, '..', 'datasets2018', 'age.csv')
        self.income_path = os.path.join(base_directory, '..', 'datasets2018', 'income.csv')
        self.in_act_age = "2016Census_G01_ACT_POA.csv"
        self.out_json = os.path.join(base_directory, '..', 'src', 'data2018', 'census.json')

    @staticmethod
    def _to_postcode(df=None, row_header="POA_CODE_2016"):
        """ convert the default postcode to just the numbers """
        def converter(row):
            row[row_header] = row[row_header].replace("POA", "")
            return row
        df = df.apply(converter, axis=1)
        return df

    def read_age(self):
        """ read the age csv """
        df = pd.read_csv(
            self.age_path,
            # index_col=0,
        )
        df = self._to_postcode(df=df)
        df = df.set_index('POA_CODE_2016')
        return df

    def read_income(self):
        """ read the income csv """
        df = pd.read_csv(
            self.income_path
        )
        df = self._to_postcode(df=df)
        df = df.set_index('POA_CODE_2016')
        return df

    def _mean_of_range(self, df, multiplyer=Decimal('1')):
        """ find the mean of the input header range """
        headers = df.columns.values
        means = {}
        indices = []
        # getcontext().prec = 4
        for index, header in enumerate(headers):
            ranges = re.search(r".*_(\d*)_(\d*)_.*", header)
            try:
                min_ = ranges.group(1)
                max_ = ranges.group(2)
                mean_ = (Decimal(min_) + Decimal(max_)) / Decimal('2')
                means[header] = "{:.0f}".format((mean_ * multiplyer).quantize(0, ROUND_UP))
                indices.append(index)
            except AttributeError:
                try:
                    ranges = re.search(r".*_(\d*)_(.*)_.*", header)
                    min_ = ranges.group(1)
                    means[header] = "{:.0f}".format((Decimal(min_) * multiplyer).quantize(0, ROUND_UP))
                    indices.append(index)
                except AttributeError:
                    continue
        df = deepcopy(df).iloc[:, indices]
        df = df.rename(columns=means)
        return df

    def to_json(self, file=None):
        """ convert the csv data to json """
        file = file if file is not None else self.out_json
        df_age = self.read_age()
        df_income = self.read_income()
        data = {}
        data['age'] = self._mean_of_range(df=df_age).to_dict(into=OrderedDict)
        data['income'] = self._mean_of_range(df_income, multiplyer=Decimal('100')).to_dict(into=OrderedDict)
        data_json = json.dumps(data)
        with open(file, 'w') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4, sort_keys=True)

    # def create_directory(self, file):
    #     """ create the path including the file """
    #     assert isinstance(file, str)
    #     assert str
    #     return os.path.join(self.data_directory, file)


if __name__ == "__main__":
    preproc = Preprocessing()
    df_age = preproc.read_age()
    df_income = preproc.read_income()
    json = preproc.to_json()
    means = preproc._mean_of_range(df=df_age)
    # for mean in means:
    #     assert isinstance(mean, (int, float))
    means_income = preproc._mean_of_range(df=df_income)
    # preproc.execute()
    assert True
