import pandas as pd

# ---------- 1. Load & clean ---------- #
def load_data(uploaded_file: str | bytes) -> pd.DataFrame:
    """
    Read the CSV, coerce dates & amounts,
    and return a clean DataFrame.
    """
    df = pd.read_csv(uploaded_file)

    # Normalise column names just in case
    df.columns = [c.strip().title() for c in df.columns]

    # Parse the Date column once, right up‑front
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Ensure amounts are numeric
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Drop any rows that failed to parse cleanly
    df = df.dropna(subset=["Date", "Amount", "Description"])

    return df.reset_index(drop=True)


# ---------- 2. Categorisation ---------- #
def categorize_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'Category' column based on the Description text.
    """
    def classify(desc: str) -> str:
        desc = desc.lower()
        if any(x in desc for x in ["salary", "credit"]):
            return "Income"
        elif any(x in desc for x in ["swiggy", "zomato"]):
            return "Food"
        elif "amazon" in desc or "flipkart" in desc:
            return "Shopping"
        elif "uber" in desc or "ola" in desc:
            return "Transport"
        elif any(x in desc for x in ["rent", "emi", "loan"]):
            return "Housing"
        elif any(x in desc for x in ["bill", "electricity", "water"]):
            return "Utilities"
        else:
            return "Other"

    df["Category"] = df["Description"].astype(str).apply(classify)
    return df


# ---------- 3. Prophet‑ready helper ---------- #
def prepare_prophet_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a daily aggregated DataFrame with Prophet’s
    expected columns: ds (date) and y (positive spend value).
    Income rows are excluded.
    """
    exp_df = df[df["Category"] != "Income"].copy()

    # Daily spend (expenses are negative; take abs to make them positive)
    daily = (
        exp_df.groupby("Date")["Amount"]
        .sum()
        .abs()
        .reset_index()
        .rename(columns={"Date": "ds", "Amount": "y"})
    )

    return daily

