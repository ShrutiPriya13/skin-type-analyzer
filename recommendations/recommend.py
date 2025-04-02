import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get absolute file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
CSV_FILE_PATH = os.path.join(BASE_DIR, "data", "skincare_products_clean.csv")  # Adjust path

try:
    df = pd.read_csv(CSV_FILE_PATH)
    df = df.sample(n=40, random_state=42)
    df.to_csv(CSV_FILE_PATH, index=False)

    # Debug: Print dataset columns and sample data
    print("Dataset Columns:", df.columns.tolist())
    print("Sample Data:\n", df.head())

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()  

    # Rename columns
    column_mapping = {
        "product_name": "product_name",
        "skin type": "skin_type",
        "category": "category",
        "ingredients": "ingredients",
        "product_url": "product_url",
        "price": "price"
    }
    df.rename(columns=column_mapping, inplace=True)

    # Ensure required columns exist
    required_columns = set(column_mapping.values())
    if not required_columns.issubset(set(df.columns)):
        raise KeyError(f"Missing required columns. Found: {list(df.columns)}")

    # Drop missing values
    df.dropna(subset=["product_name", "skin_type", "category", "ingredients"], inplace=True)

    # Check if dataframe is empty after cleaning
    if df.empty:
        print("Warning: No valid data available after cleaning.")
        similarity_matrix = None
    else:
        # Combine 'Ingredients' and 'Category' for similarity analysis
        df['features'] = df['ingredients'].astype(str) + " " + df['category'].astype(str)

        # Convert text data to numerical representation using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(df['features'])

        # Compute similarity between products
        similarity_matrix = cosine_similarity(tfidf_matrix)

except Exception as e:
    print(f"Error loading recommendation dataset: {e}")
    df = None
    similarity_matrix = None

def recommend_products(skin_type, num_recommendations=5):
    """Recommends skincare products based on the detected skin type."""
    
    if df is None or similarity_matrix is None:
        return [{"error": "Recommendation system is not available."}]

    # Debug: Check available skin types
    print("Unique Skin Types in Dataset:", df['skin_type'].unique())

    # Normalize skin type for matching (avoid modifying the original df)
    skin_type = skin_type.strip().lower()
    df_filtered = df.copy()
    df_filtered["skin_type"] = df_filtered["skin_type"].str.strip().str.lower()

    # Filter products based on skin type
    skin_type_products = df_filtered[df_filtered['skin_type'] == skin_type]

    if skin_type_products.empty:
        print(f"No products found for skin type: {skin_type}")
        return [{"error": f"No products found for skin type: {skin_type}"}]

    # Get indices of matching products
    product_indices = skin_type_products.index.tolist()
    recommendations = set()  # Use a set to remove duplicates

    for idx in product_indices:
        sim_scores = list(enumerate(similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Exclude self-recommendation
        sim_indices = [i[0] for i in sim_scores if i[0] != idx][:num_recommendations]
        recommendations.update(sim_indices)

    # Convert to structured output
    recommended_products = df_filtered.iloc[list(recommendations)][["product_name", "product_url", "price"]].to_dict(orient="records")

    # Debug: Print recommended products
    print(f"Recommended Products for {skin_type}: {recommended_products}")

    return recommended_products  # Returns structured JSON response

