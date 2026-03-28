# 🎬 CineMatch — Movie Recommender System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![TMDB](https://img.shields.io/badge/TMDB-API-01B4E4?style=for-the-badge&logo=themoviedatabase&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5.1-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)

**A full-stack movie recommendation system powered by TF-IDF content filtering and TMDB live data.**

[![🚀 Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Click%20Here-e8b84b?style=for-the-badge)](https://movierecommendation-juspzbc78f7k2eypqxj8gr.streamlit.app/)

</div>

---

## 🌐 Live Demo

> **Try it now:** [https://movierecommendation-juspzbc78f7k2eypqxj8gr.streamlit.app/](https://movierecommendation-juspzbc78f7k2eypqxj8gr.streamlit.app/)

No installation required — just open the link and start exploring movies.

---

## 📌 Overview

CineMatch is a content-based movie recommendation engine that combines a locally trained **TF-IDF model** on a dataset of **50,000+ movies** with real-time data from the **TMDB API**. It delivers two types of recommendations:

- **Similar Movies (TF-IDF)** — finds movies with similar content, plot keywords, cast, and genres using cosine similarity on TF-IDF vectors
- **Genre Recommendations** — fetches popular movies in the same genre using TMDB Discover API

---

## 🧠 How It Works

```
User searches movie
        │
        ▼
   TMDB Search API ──► Returns live results with posters
        │
        ▼
  User clicks movie
        │
        ├──► /movie/id/{tmdb_id} ──► Fetches full details from TMDB
        │
        ├──► TF-IDF Model (local) ──► Cosine similarity on 50,000 movie dataset
        │         └──► Top N similar titles ──► TMDB API attaches posters
        │
        └──► TMDB Discover API ──► Genre-based popular movies
```

---

## 📊 Model & Dataset

| Property | Details |
|----------|---------|
| **Dataset Size** | 50,000+ movies |
| **Algorithm** | TF-IDF Vectorization + Cosine Similarity |
| **Features Used** | Title, Overview, Genres, Keywords, Cast |
| **Similarity Metric** | Cosine Similarity |
| **Model Accuracy** | ~85% relevance on genre-matched recommendations |
| **Vectorizer** | scikit-learn `TfidfVectorizer` |
| **Matrix Format** | Scipy Sparse Matrix |
| **Poster Source** | TMDB API (live) |

> **Accuracy note:** Measured as the percentage of top-10 recommendations that share at least one genre with the query movie across 500 test queries on the local dataset.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit Frontend            │
│  • Search, Browse, Details, Grid UI     │
│  • Session state routing (home/details) │
└──────────────────┬──────────────────────┘
                   │ HTTP
┌──────────────────▼──────────────────────┐
│           FastAPI Backend               │
│  • /home          → TMDB feed           │
│  • /tmdb/search   → TMDB keyword search │
│  • /movie/id/{id} → TMDB details        │
│  • /movie/search  → TF-IDF + Genre recs │
│  • /recommend/genre → TMDB Discover     │
│  • /recommend/tfidf → Raw TF-IDF debug  │
└──────────────────┬──────────────────────┘
                   │
       ┌───────────┴───────────┐
       ▼                       ▼
  TF-IDF Model            TMDB API
  (df.pkl,                (Live posters,
  tfidf_matrix.pkl,        details,
  indices.pkl)             discover)
```

---

## ✨ Features

- 🔍 **Live Search** — keyword search powered by TMDB with dropdown suggestions
- 🎬 **Movie Details** — full details including backdrop, tagline, runtime, rating, genres
- 🤖 **TF-IDF Recommendations** — content-based similar movies from 50K dataset
- 🎭 **Genre Recommendations** — TMDB-powered popular movies in the same genre
- 🔥 **Home Feed** — Trending, Popular, Top Rated, Now Playing, Upcoming
- 📱 **Responsive Grid** — adjustable column layout (3–8 columns)
- ⭐ **Ratings & Metadata** — star ratings, release year, vote count displayed on cards
- 🌙 **Dark Cinematic UI** — custom dark theme with gold accents

---

## 🚀 Local Setup

### Prerequisites

- Python 3.11
- TMDB API Key ([get one free here](https://www.themoviedb.org/settings/api))

### 1. Clone the repository

```bash
git clone https://github.com/your-username/movierecommendation.git
cd movierecommendation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
TMDB_API_KEY=your_tmdb_api_key_here
```

### 4. Add model files

Place these pickle files in the project root:

```
movierecommendation/
├── df.pkl              # DataFrame with 50K movies
├── indices.pkl         # Title → index mapping
├── tfidf_matrix.pkl    # Scipy sparse TF-IDF matrix
├── tfidf.pkl           # Fitted TfidfVectorizer
```

### 5. Start the backend

```bash
uvicorn main:app --reload --port 8000
```

### 6. Start the frontend

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📦 Requirements

```
fastapi==0.111.0
uvicorn==0.30.1
python-dotenv==1.0.1
httpx==0.27.0
pandas==2.2.2
numpy==2.0.1
scipy==1.13.1
scikit-learn==1.5.1
pillow==10.4.0
streamlit==1.36.0
requests
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/home` | Home feed (trending, popular, etc.) |
| `GET` | `/tmdb/search` | Keyword search via TMDB |
| `GET` | `/movie/id/{tmdb_id}` | Full movie details |
| `GET` | `/movie/search` | TF-IDF + genre recommendations bundle |
| `GET` | `/recommend/genre` | Genre-based recommendations |
| `GET` | `/recommend/tfidf` | Raw TF-IDF recommendations (debug) |

---

## 📁 Project Structure

```
movierecommendation/
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version for Streamlit Cloud
├── .env                    # API keys (not committed)
├── .gitignore
├── df.pkl                  # Movie dataset (50K movies)
├── indices.pkl             # Title index map
├── tfidf_matrix.pkl        # TF-IDF sparse matrix
└── tfidf.pkl               # TF-IDF vectorizer
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository, set main module to `app.py`
4. Add `TMDB_API_KEY` in **Settings → Secrets**
5. Make sure `runtime.txt` contains `python-3.11`

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit 1.36 |
| Backend | FastAPI 0.111 |
| ML Model | scikit-learn TF-IDF |
| Movie Data | TMDB API v3 |
| Matrix Math | NumPy + SciPy |
| HTTP Client | httpx (async) + requests |
| Deployment | Streamlit Cloud + Render |

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [TMDB](https://www.themoviedb.org/) for the movie database API
- [Streamlit](https://streamlit.io/) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework

---

<div align="center">
Made with ❤️ and 🎬

[![🚀 Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Click%20Here-e8b84b?style=for-the-badge)](https://movierecommendation-juspzbc78f7k2eypqxj8gr.streamlit.app/)
</div>
