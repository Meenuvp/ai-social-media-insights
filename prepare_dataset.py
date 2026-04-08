import pandas as pd

# ---------------- LOAD DATA ----------------
twitter = pd.read_csv("twitter_dataset.csv")
linkedin_company = pd.read_csv("Linkedin_company.csv")
linkedin_people = pd.read_csv("Linkedin_people.csv")

# ---------------- TWITTER ----------------
twitter_df = pd.DataFrame({
    "platform": "Twitter",
    "account_type": "Person",
    "account_id": twitter["Username"].astype(str),
    "post": twitter["Text"].astype(str)
})

# ---------------- LINKEDIN COMPANY ----------------
linkedin_company_df = pd.DataFrame({
    "platform": "LinkedIn",
    "account_type": "Company",
    "account_id": linkedin_company["name"].astype(str),
    "post": linkedin_company["updates"].fillna(
        linkedin_company["about"]
    ).astype(str)
})

# ---------------- LINKEDIN PEOPLE ----------------
linkedin_people_df = pd.DataFrame({
    "platform": "LinkedIn",
    "account_type": "Person",
    "account_id": linkedin_people["name"].astype(str),
    "post": linkedin_people["posts"].fillna(
        linkedin_people["about"]
    ).astype(str)
})

# ---------------- MERGE ----------------
final_df = pd.concat(
    [twitter_df, linkedin_company_df, linkedin_people_df],
    ignore_index=True
)

# ---------------- CLEAN ----------------
final_df["post"] = final_df["post"].str.strip()
final_df.dropna(subset=["post"], inplace=True)
final_df = final_df[final_df["post"] != ""]

# ---------------- SAVE ----------------
final_df.to_csv("social_media_data.csv", index=False)

print("✅ Unified social media dataset created successfully!")
