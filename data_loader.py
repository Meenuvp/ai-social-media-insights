import pandas as pd
import json

def load_data():
    dfs = []

    # ---------------- TWITTER ----------------
    twitter = pd.read_csv("twitter_dataset.csv")
    twitter_df = pd.DataFrame({
        "platform": "twitter",
        "account_id": twitter["Username"].astype(str),
        "post": twitter["Text"].astype(str)
    })
    dfs.append(twitter_df)

    # ---------------- LINKEDIN COMPANY ----------------
    linkedin_company = pd.read_csv("linkedin_company.csv")

    company_posts = []
    for _, row in linkedin_company.iterrows():
        if pd.notna(row.get("updates")):
            try:
                updates = json.loads(row["updates"])
                for post in updates:
                    company_posts.append({
                        "platform": "linkedin",
                        "account_id": str(row["company_id"]),
                        "post": post.get("text", "")
                    })
            except Exception:
                pass

    if company_posts:
        dfs.append(pd.DataFrame(company_posts))

    # ---------------- LINKEDIN PEOPLE ----------------
    linkedin_people = pd.read_csv("linkedin_people.csv")

    people_posts = []
    for _, row in linkedin_people.iterrows():
        if pd.notna(row.get("posts")):
            try:
                posts = json.loads(row["posts"])
                for post in posts:
                    people_posts.append({
                        "platform": "linkedin",
                        "account_id": str(row["id"]),
                        "post": post.get("title", "")
                    })
            except Exception:
                pass

    if people_posts:
        dfs.append(pd.DataFrame(people_posts))

    return pd.concat(dfs, ignore_index=True)


def filter_data(df, platform, account_id):
    return df[
        (df["platform"] == platform.lower()) &
        (df["account_id"] == str(account_id))
    ]
