import pandas as pd
import numpy as np
import os
from tabulate import tabulate

np.set_printoptions(precision=2, suppress=True)

print("Reading CSV input")

input_path = os.path.join(os.path.dirname(__file__), "../data/")
output_path = os.path.join(os.path.dirname(__file__), "../data/slices/")

df = pd.read_csv(
    os.path.normpath(input_path + "avocado.csv")
)

input_path_location = os.path.join(
    os.path.dirname(__file__), "../data/locations/"
)
expanded_locations = pd.read_csv(
    os.path.normpath(input_path_location + "expanded.csv")
)


class DataPreparation:

    def __init__(self, df):
        self.df = df

    def expand_date(self, to_year_week=False):

        self.df = self.df.drop(columns=["year"])
        self.df["date"] = pd.to_datetime(self.df["date"])

        if to_year_week:
            self.df["year"] = self.df["date"].dt.isocalendar().year
            self.df["week"] = self.df["date"].dt.isocalendar().week

        else:
            self.df["year"] = self.df["date"].dt.year
            self.df["month"] = self.df["date"].dt.month
            self.df["day"] = self.df["date"].dt.day

        self.df = self.df.drop(columns=["date"])

        return self

    def remove_date(self, keep_year=False):
        if keep_year:
            self.df = self.df.drop(columns=["date"])
        else:
            self.df = self.df.drop(columns=["date", "year"])
        return self

    def keep(self, total_volume, volume_components):
        if volume_components:
            self.df = self.df.drop(columns=[
                "total_volume",
                "total_bags"
                ])
        if total_volume:
            self.df = self.df.drop(columns=[
                "4046", "4225", "4770",
                "small_bags", "large_bags", "xlarge_bags",
                "total_bags"
            ])
        if not total_volume and not volume_components:
            self.df = self.df.drop(columns=[
                "4046", "4225", "4770",
                "small_bags", "large_bags", "xlarge_bags",
                "total_volume",
                "total_bags"
            ])
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
        df_organic = df_organic.drop(columns=["type"])

        df_conventional = self.df[self.df["type"] == "conventional"]
        df_conventional = df_conventional.drop(columns=["type"])

        return {"organic": df_organic, "conventional": df_conventional}

    def slice(self, by_avocado_type=False, by_location_level=False):
        slices = {}
        if by_avocado_type:
            slices.update(self.slice_by_avocado_type())
            if by_location_level:
                return Exception("Not implemented")
                # return self.slice_by_region_level()
        if not by_avocado_type and not by_location_level:
            slices.update({"avocado": self.df})
        return slices


data_processor = DataPreparation(df)
slices = (
    data_processor
    .keep(volume_components=True, total_volume=False)
    # .remove_date()
    .expand_date(to_year_week=True)
    .add_location_details(expanded_locations)
    .slice()
)

for slice_name, slice in slices.items():
    print(f"\n##### Preparing Slice: {slice_name} #####\n")
    slice.to_csv(
        os.path.normpath(output_path + slice_name + ".csv"),
        index=False
    )
    print(tabulate(slice.sample(5), headers='keys', tablefmt='psql'))
