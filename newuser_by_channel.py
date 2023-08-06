#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 14:09:54 2023

@author: sohrab-salehin
"""

# Table that I use for this report: https://metabase.pinsvc.net/question/6013-bus-table-for-budget-tracker

# importing packages

import pandas as pd
import numpy as np

# importing files:
    # note that bus_4 should be updated each time: the
    # previous data is from day zero to 2023-06-30
    # SO bus_4 SHOULD BE FROM 2023-07-01 TO ACTUAL DATE



bus_1 = pd.read_csv(
    "bus_1.csv",
    parse_dates=["Book Created At"],
    dtype={"Book ID": str, "Cell Phone": str},
)
bus_2 = pd.read_csv(
    "bus_2.csv",
    parse_dates=["Book Created At"],
    dtype={"Book ID": str, "Cell Phone": str},
)
bus_3 = pd.read_csv(
    "bus_3.csv",
    parse_dates=["Book Created At"],
    dtype={"Book ID": str, "Cell Phone": str},
)
bus_4 = pd.read_csv(
    "bus_4.csv",
    parse_dates=["Book Created At"],
    dtype={"Book ID": str, "Cell Phone": str},
)
bus = pd.concat([bus_1, bus_2, bus_3, bus_4])
bus = bus[bus["Ticket Status"] != "FAILED"]
bus = bus.drop_duplicates(subset="Book ID").reset_index(drop=True)
bus = bus.sort_values(by="Book Created At")

# Masking new and returning users:

first_occurrence_mask = ~bus["Cell Phone"].duplicated(keep="first")
first_occurrence_df = bus[first_occurrence_mask]
index = first_occurrence_df.index
bus.loc[index, "newuser"] = True
index = bus[bus["newuser"].isna()].index
bus.loc[index, "newuser"] = False

# Labeling marketing channels: 

index = bus[bus["Discount Code"].str.startswith("SLB", na=False)].index
bus.loc[index, "channel_type"] = "loyalty"

index = bus[
    bus["Discount Code Tag"].str.contains("journey", na=False, case=False)
].index
bus.loc[index, "channel_type"] = "crm"

index = bus[
    bus["Discount Code Tag"].str.contains("campaign", na=False, case=False)
].index
bus.loc[index, "channel_type"] = "campaign"

index = bus[
    bus["Discount Code Tag"].str.contains("affiliate", na=False, case=False)
].index
bus.loc[index, "channel_type"] = "affiliate"

index = bus[(bus["channel_type"].isna()) & (bus["Discount Code"].notna())].index
bus.loc[index, "channel_type"] = "other_voucher"

index = bus[bus["Discount Code"].isna()].index
bus.loc[index, "channel_type"] = "adwords & organic"

# Here you should specify from date and to date of the report: 

date_from= input('Please specify from date of the report: ')
date_to= input('Please specify to date of the report: ')

bus_for_report = bus[
    (bus["Book Created At"] >= date_from) & (bus["Book Created At"] <= date_to)
]

# Report Table:

report_table = pd.pivot_table(
    bus_for_report,
    index="channel_type",
    columns="newuser",
    values=["Book ID"],
    aggfunc="nunique",
)
report_table