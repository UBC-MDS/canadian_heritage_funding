# authors: Joyce Wang, Amelia Tang, Wenxin Xiang, Artan Zandian
# date: 2021-11-25

"""Outputs eda plots and tables

Usage: eda_plots.py --data=<data> --table=<table> --plot1=<plot1> --plot2=<plot2> --plot3=<plot3>

Options:
--data=<data>                file path of the csv file to read
--table=<table>              file path of the target category count table
--plot1=<plot1>              file path of the target_distribution_plot
--plot2=<plot2>              file path of the funding_year_discipline_plot
--plot3=<plot3>              file path of the feature_counts_plot

"""

import os
import pandas as pd
import numpy as np
import altair as alt
from docopt import docopt

opt = docopt(__doc__)


def main(data, table_path, plot1_path, plot2_path, plot3_path):
    """
    reads data, saves dataframe as csv file and call functions to save
    plots as png files

    Parameters
    ----------
    data : str
        file path for the data
    table_path : str
        file path to save the table
    plot1_path : str
        file path to save the plot
    plot2_path : str
        file path to save the plot
    plot3_path : str
        file path to save the plot
    """
    data = pd.read_csv(data, encoding="ISO-8859-1")
    data["audiences"] = data["audiences"].str.split(", ", expand=False)
    data["disciplines"] = data["disciplines"].str.split(", ", expand=False)
    data_expl = data.explode("audiences").explode("disciplines")


    distr_table = target_distribution_table(data)
    plot1 = target_distr_plot(data)
    plot2 = funding_year_discipline_plot(data_expl)
    plot3 = feature_counts_plot(data, data_expl)

    # output table
    try:
        distr_table.to_csv(table_path, index=True)
    except:
        os.makedirs(os.path.dirname(table_path))
        distr_table.to_csv(table_path, index=True)

    # output plots
    output_plots(plot1, plot1_path, 4)
    output_plots(plot2, plot2_path, 4)
    output_plots(plot3, plot3_path, 4)


def target_distribution_table(data):
    """
    generate a dataframe describing count of each category

    Parameters
    ----------
    data : dataframe
        data to process

    Returns
    -------
    dataframe
        dataframe containing count of each category
    """
    summary = pd.DataFrame(
        data.groupby("amount_category").count()["amount_approved"]).rename(columns={"amount_approved": "Count"}
        )

    return summary


def target_distr_plot(data):
    """
    generate plot for distribution of each target category

    Parameters
    ----------
    data : dataframe
        data to generate plot for

    Returns
    -------
    altair plot
        plot of distribution of each target category
    """
    q10 = data["amount_approved"].quantile(0.1)
    q25 = data["amount_approved"].quantile(0.25)
    q50 = data["amount_approved"].quantile(0.5)
    q75 = data["amount_approved"].quantile(0.75)

    labeling = [f"over ${q75/1000}K",
                f"${q50/1000}-{q75/1000}K",
                f"${q25/1000}-{q50/1000}K",
                f"${q10/1000}-{q25/1000}K",
                f"less than ${q10/1000}K"]

    plot =  (
        alt.Chart(data).mark_bar(clip=True).encode(
            alt.X("amount_approved", scale=alt.Scale(domain=(0, 260000)), 
                bin=alt.Bin(maxbins=200), stack=False, title="Amount approved"),
            alt.Y("count()"),
            alt.Color("amount_category", sort=labeling, title = "Amount Category"))
        .properties(width=250, height=250)
        .facet("amount_category", columns=3, title="Distribution of approved amount by threshold")
    )

    return plot



def funding_year_discipline_plot(data_expl):
    """
    generate plot for funding for each year period and different disciplines

    Parameters
    ----------
    data_expl : dataframe
        data to generate plot for

    Returns
    -------
    altair plot
        the generated plot
    """
    plot = (
        alt.Chart(data_expl).mark_bar().encode(
            alt.Y("disciplines", type="ordinal", title=None),
            alt.X("count()"),
            alt.Color("amount_category", title="Amount Category"))
        .properties(width=200, height=150)
        .facet("fiscal_year", columns=1, title="Fixed pooled funding per discipline")
    )

    return plot


def feature_counts_plot(data, data_expl):
    """
    generate plot for counts of data for each feature

    Parameters
    ----------
    data : dataframe
        data to generate plot for
    data_expl : dataframe
        data to generate plot for with "disciplines" and "audiences" columns
        exploded

    Returns
    -------
    altair plot
        the generated plot
    """    
    columns_eda = ['fiscal_year',
               'province',
               'region',
               'community_type',
               'grant_or_contribution',
               'presenter_type',
               'project_sub_type',
               'project_type']
    columns_exploded = ["disciplines", "audiences"]

    plot = (
        alt.Chart(data).mark_bar().encode(
            alt.Y(alt.repeat(), type="ordinal"),
            alt.X("count()", stack=False),)
        .properties(width=130, height=150)
        .repeat(columns_eda, columns=2, title="Count of categorical columns")
    )
    plot_expl = (
        alt.Chart(data_expl).mark_bar().encode(
            alt.Y(alt.repeat(), type="ordinal"),
            alt.X("count()", stack=False),)
        .properties(width=160, height=150)
        .repeat(columns_exploded)
    )

    combined = plot & plot_expl
    return combined


def output_plots(plot, file_path, scale):
    """
    helper function to save altair plots to file, and make new folder
    if file_path is not found

    Parameters
    ----------
    plot : altair plot
        the plot to save
    file_path : str
        file path to save the plot
    scale : float
        the scale factor when saving the plot
    """
    try:
        plot.save(file_path, scale_factor=scale)
    except:
        os.makedirs(os.path.dirname(file_path))
        plot.save(file_path, scale_factor=scale)


    

if __name__ == "__main__":
    main(opt["--data"], opt["--table"], opt["--plot1"], opt["--plot2"], opt["--plot3"])
