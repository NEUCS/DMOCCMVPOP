import yfinance as yf
import numpy as np
import pandas as pd
import os


def save_period_data(period, assets, folder_path):
    start_date_str = period["start_date"].strftime("%Y%m%d")
    end_date_str = period["end_date"].strftime("%Y%m%d")
    file_name = f"{start_date_str}_{end_date_str}.txt"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w") as file:
        file.write(f"{len(assets)}\n")
        for asset, mean_return in zip(assets, period["mean_returns"]):
            file.write(f"{mean_return}\n")
        file.write("\n")
        file.write(period["cov_matrix"].to_string(index=False, header=False))


def get_data_periods(assets, start_date, end_date, folder_path):
    data = yf.download(assets, start=start_date, end=end_date, proxy="127.0.0.1:7890")
    returns = data["Adj Close"].pct_change().dropna()

    periods = []
    start_dates = pd.date_range(start=start_date, end=end_date, freq="2M")

    for i in range(len(start_dates) - 1):
        start = start_dates[i]
        end = start_dates[i + 1] - pd.Timedelta(days=1)

        period_returns = returns.loc[start:end]
        period_mean_returns = period_returns.mean()
        period_cov_matrix = period_returns.cov()

        period = {
            "start_date": start,
            "end_date": end,
            "mean_returns": period_mean_returns,
            "cov_matrix": period_cov_matrix
        }
        periods.append(period)
        save_period_data(period, assets, folder_path)

    return periods


assets = ["AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "BRK-B", "JPM", "JNJ",
          "V", "NVDA", "PG", "UNH", "HD", "MA", "DIS", "PYPL", "BAC", "VZ",
          "NFLX", "KO", "PEP", "MRK", "ABT", "CSCO", "XOM", "CMCSA", "ADP", "ORCL"]
start_date = "2022-06-01"
end_date = "2023-07-31"
folder_path = "period_data_111"

os.makedirs(folder_path, exist_ok=True)

data_periods = get_data_periods(assets, start_date, end_date, folder_path)
