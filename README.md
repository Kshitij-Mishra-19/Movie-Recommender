# Movie Recommender System
A Streamlit app that recommends 5 similar movies based on content (genres, keywords, cast, crew, and overview), using a precomputed cosine-similarity matrix, and shows posters fetched from the OMDB API.

## How it works
1. `movie-recommender-system-model.ipynb` builds the model from the raw TMDB 5000 dataset:
   - Merges `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` on title.
   - Extracts genres, keywords, top cast, and director from each movie.
   - Combines these with the overview into a single "tags" string per movie, stemmed with NLTK's `PorterStemmer`.
   - Vectorizes tags with `CountVectorizer` (top 5000 words, English stop words removed).
   - Computes pairwise `cosine_similarity` across all vectors to produce the similarity matrix.
   - Saves the results as `movie_dict.pkl` (movie metadata) and `similarity.pkl` (similarity matrix).
2. `app.py` loads those two pickle files and serves the interactive recommender — no model training happens at app runtime.

## Setup (running the app)
1. Install dependencies:
```bash
   pip install -r requirements.txt
```
2. Get a free OMDB API key from https://www.omdbapi.com/apikey.aspx
3. Provide the key one of two ways:
   - **Local Streamlit:** copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your key.
   - **Environment variable:** `export OMDB_API_KEY=your_key_here`
4. Run the app:
```bash
   streamlit run app.py
```

## Deploying to Streamlit Cloud
Add `OMDB_API_KEY` under your app's **Settings → Secrets** in the Streamlit Cloud dashboard (same TOML format as `secrets.toml.example`).

## Regenerating the model (optional)
The repo already ships with `movie_dict.pkl` and `similarity.pkl`, so this step isn't required to run the app. Only do this if you want to retrain on updated data or tweak the feature engineering.
```bash
pip install -r requirements-dev.txt
jupyter notebook movie-recommender-system-model.ipynb
```
Run all cells; this regenerates `movie_dict.pkl` and `similarity.pkl` in place from `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`.

## Files
- `app.py` — Streamlit app
- `movie_dict.pkl` - movie metadata (title, genres, cast, etc.)
- `similarity.pkl` - precomputed cosine similarity matrix (float32)
- `movie-recommender-system-model.ipynb` - notebook that builds the model from raw data
- `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv` - raw TMDB 5000 dataset
- `requirements.txt` - runtime dependencies for the app
- `requirements-dev.txt` - extra dependencies needed only to run the notebook

## Author
**Kshitij Mishra**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/kshitij-mishra-19)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/Kshitij-Mishra-19)

## ⭐ Support
If you found this project helpful or interesting, consider giving it a star on GitHub - it helps others discover it and means a lot!

[![GitHub stars](https://img.shields.io/github/stars/Kshitij-Mishra-19/Movie-Recommender?style=social)](https://github.com/Kshitij-Mishra-19/Movie-Recommender)
