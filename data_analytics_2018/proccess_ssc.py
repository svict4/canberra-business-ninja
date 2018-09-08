from preprocessing import Preprocessing
import pandas as pd


class ProcessSSCData:
    def __init__(self, src_file=None):
        """
            src_file (str):    the name of the data file
        """
        src_file = src_file if src_file is not None else "2016Census_G01_ACT_POA.csv"
        self.dataobj = Preprocessing()
        self.division_centers = self.dataobj.process_act_division_boundaries()
        df = pd.read_csv(
            self.dataobj.create_directory(src_file),
        )
        df = df.loc[" (ACT)" in df.iloc[:, 0]]

        assert True

# def __init__(self, ssc_src_file=None):
#
#    # ssc_src_file = "../datasets/SSC_2016_AUST_ACT.csv"
#    ssc_src_file = ssc_src_file if ssc_src_file is not None else "2016Census_G01_ACT_POA.csv"
#
#    df = pd.DataFrame(ssc_src_file)
#
#    with open(self.dataobj.create_directory(ssc_src_file)) as f:
# 		self.ssc_data = f.readlines()
# 	self.ssc_map = {}
# 	for line in self.ssc_data:
# 		split_array = line.split(",")
# 		code = int(split_array[1])
# 		suburb = split_array[2]
# 		if not suburb.find("ACT Remainder") or not suburb.find("Migratory") or not suburb.find("No usual"):
# 			continue
# 		suburb = suburb.replace(" (ACT)", "")
# 		suburb = suburb.upper()
# 		if (code not in self.ssc_map) and (suburb in self.division_centers):
# 			self.ssc_map[code] = suburb

# def convert_ssc_to_suburb_name(self, ssc):
# 	if ssc in self.ssc_map:
# 		return self.ssc_map[ssc]
# 	else:
# 		return False


def convert_ssc_to_suburb_name(self, ssc):
    if ssc in self.ssc_map:
        return self.ssc_map[ssc]
    else:
        return False


if __name__ == "__main__":
    ssc_obj = ProcessSSCData()
    print(ssc_obj.convert_ssc_to_suburb_name(80084))
