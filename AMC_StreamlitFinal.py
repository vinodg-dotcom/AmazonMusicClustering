import streamlit as st
import pandas as pd
import os

# Set page layout to wide
st.set_page_config(layout="wide", page_title="Music Clustering Dashboard")

st.sidebar.title("🎮 Navigation")
view_mode = st.sidebar.selectbox(
    "Select View Mode:", ["Saved Analysis Portfolio", "Live Cluster Explorer"]
)

@st.cache_data
def load_data():
    return pd.read_csv("https://github.com/vinodg-dotcom/AmazonMusicClustering/blob/main/final_clustered_music_dataset.csv?raw=true")

try:
    df = load_data()
except Exception as e:
    st.error("Could not find 'final_clustered_music_dataset.csv'. Please run your Jupyter Notebook cells to export the file first.")
    st.stop()

# -------------------------------------------------------
# MODE 1: SAVED ANALYSIS PORTFOLIO
# -------------------------------------------------------
if view_mode == "Saved Analysis Portfolio":
    st.title("📈 Saved Analysis Portfolio")
    st.write(
        "Select a specific analysis plot from the dropdown below to visualize the clustering results."
    )

    # Dropdown updated to match your exact portfolio file list
    selected_graph = st.selectbox(
        "Select Graph to View:",
        [
            "The Elbow Method Plot",
            "Combined Music Radar Chart",
            "PCA Cluster Scatter Plot",
            "Feature Intensity Heatmap per Cluster",
            "Danceability vs Acousticness across Clusters",
        ],
    )

    # Explicit mapping to your exact requested filenames
    graph_map = {
        "The Elbow Method Plot": "kmeans_elbow_method_plot.png",
        "Combined Music Radar Chart": "simple_music_radar_chart.png",
        "PCA Cluster Scatter Plot": "music_pca_dataframe_scatter.png",
        "Feature Intensity Heatmap per Cluster": "Feature Intensity Heatmap per Cluster.png",
        "Danceability vs Acousticness across Clusters": "Danceability vs Acousticness across Clusters.png",
    }

    image_filename = graph_map[selected_graph]

    if os.path.exists(image_filename):
        st.image(image_filename, use_container_width=True)
    else:
        st.warning(f"The asset '{image_filename}' was not found. Please run your Jupyter notebook cell to generate it.")

# -------------------------------------------------------
# MODE 2: LIVE CLUSTER EXPLORER
# -------------------------------------------------------
elif view_mode == "Live Cluster Explorer":
    st.title("🔍 Live Cluster Explorer")
    st.write("Deep dive into each individual cluster profile, tracks, and underlying audio footprints.")

    # Unique Cluster IDs from your 4-cluster KMeans configuration
    cluster_options = sorted(df["Cluster_Label"].unique())
    selected_cluster = st.selectbox("Select Music Cluster:", cluster_options, format_func=lambda x: f"Cluster {x}")

    cluster_summaries = {
        0: """
        ### **Cluster 0: Classical Soundscapes**
        * **Acousticness:** ⬆️ **Very High** *(Predominant feature)*
        * **Energy / Loudness:** ⬇️ **Low** *(Soft, mellow dynamics)*
        * **Instrumentalness:** ⬆️ **Elevated** *(Strong representation of instrumental tracks)*
        """,
        1: """
        ### **Cluster 1: Commercial Pop**
        * **Energy & Danceability:** ⬆️ **High Peaks** *(Optimized for clubs/radio)*
        * **Loudness:** ⚡ **High Volume / Compressed**
        * **Acoustic / Instrumental:** ⬇️ **Near Zero** *(Synthetic or heavily produced)*
        """,
        2: """
        ### **Cluster 2: Spoken Word, Rap & Podcasts**
        * **Speechiness:** ⬆️ **The Absolute Highest Peak** *(Voice-centric tracks)*
        * **Liveness:** ⬆️ **Elevated** *(Spontaneous or live-mic feel)*
        * **Instrumentalness:** ⬇️ **Zero** *(No lingering arrangements)*
        """,
        3: """
        ### **Cluster 3: Melodic Grooves**
        * **Valence (Positivity):** ⬆️ **Highest Peak** *(Happy, upbeat tracks)*
        * **Danceability:** ⬆️ **Strong** *(Rhythmic and groovy rhythm sections)*
        * **Acousticness:** ⬇️ **Low** *(Primarily modern electronic/amplified instrumentation)*
        """,
    }

    col_img, col_txt = st.columns([1, 1])

    with col_img:
        radar_filename = f"music_radar_cluster_{selected_cluster}.png"
        if os.path.exists(radar_filename):
            st.image(radar_filename, caption=f"Musical DNA Radar: Cluster {selected_cluster}", use_container_width=True)
        else:
            st.caption(f"Radar visualization file '{radar_filename}' not found. Run your notebook to export it.")

    with col_txt:
        st.info(cluster_summaries[selected_cluster])

        filtered_df = df[df["Cluster_Label"] == selected_cluster]
        
        stat_col1, stat_col2 = st.columns(2)
        stat_col1.metric("Total Songs Assigned", f"{len(filtered_df):,}")
        stat_col2.metric("Market Track Share", f"{(len(filtered_df) / len(df) * 100):.1f}%")

    st.subheader(f"Sample Tracks in Cluster {selected_cluster}")
    
    search_query = st.text_input("Search tracks by Song Title or Artist Name:", "")
    
    display_df = filtered_df[["name_song", "name_artists", "genres", "release_date"]].copy()
    display_df.columns = ["Song Title", "Artist", "Genres", "Release Date"]

    if search_query:
        display_df = display_df[
            display_df["Song Title"].str.contains(search_query, case=False, na=False) |
            display_df["Artist"].str.contains(search_query, case=False, na=False)
        ]

    st.dataframe(display_df.head(100), use_container_width=True, hide_index=True)