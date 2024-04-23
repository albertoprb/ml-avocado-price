import pandas as pd
import numpy as np
import os
from tabulate import tabulate

np.set_printoptions(precision=2, suppress=True)


input_path = os.path.join(os.path.dirname(__file__), "../data/")
output_path = os.path.join(os.path.dirname(__file__), "../data/output/")

print("Reading JSON input")
df = pd.read_csv(
    os.path.normpath(input_path + "avocado.csv")
)
geographies = pd.read_csv(
    os.path.normpath(input_path + "geographies_processed.csv")
)


class DataPreparation:

    def __init__(self, df):
        self.df = df

    def convert_date(self, to_year_week=False):
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["year"] = self.df["date"].dt.year
        if to_year_week:
            self.df["date"] = pd.to_datetime(self.df["date"])
            self.df["year"] = self.df["date"].dt.isocalendar().year
            self.df["week"] = self.df["date"].dt.isocalendar().week # Creates a problem matching week to year
        else:
            self.df["month"] = self.df["date"].dt.month
            self.df["day"] = self.df["date"].dt.day
        self.df = self.df.drop(columns=["date"])
        return self

    def remove_redundant_features(self):
        self.df = self.df.drop(columns=["total_volume", "total_bags"])
        return self

    def add_location_details(self, geographies):
        df_geo = pd.merge(self.df, geographies, on='geography')
        df_geo.drop(columns=[
            'location_raw',
            'location_count',
            'location_name',
        ], inplace=True)
        df_geo.info()
        self.df = df_geo
        return self

    def slice_by_region_level(self):
        return Exception("Not implemented")

    def slice_by_avocado_type(self):
        df_organic = self.df[self.df["type"] == "organic"]
        df_conventional = self.df[self.df["type"] == "conventional"]
        return {"organic": df_organic, "conventional": df_conventional}

    def slice(self, by_location_level=False, by_avocado_type=False):
        slices = {}
        if by_avocado_type:
            slices.update(self.slice_by_avocado_type())
            if by_location_level:
                return Exception("Not implemented")
                # return self.slice_by_region_level()
        return slices


data_processor = DataPreparation(df)
slices = (
    data_processor
    .remove_redundant_features()
    .convert_date(to_year_week=True)
    .add_location_details(geographies)
    .slice(by_avocado_type=True)
)

for slice_name, slice in slices.items():
    print(f"\n##### Preparing Slice: {slice_name} #####\n")
    slice.to_csv(
        os.path.normpath(output_path + slice_name + ".csv"),
        index=False
    )
    print(tabulate(slice.sample(5), headers='keys', tablefmt='psql'))
