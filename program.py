import os
import pandas as pd
import librosa
import numpy as np
from pymongo import MongoClient

# Function to load metadata
def load_metadata(metadata_file):
    try:
        metadata = pd.read_csv(metadata_file, index_col=0, header=[0, 1])
        return metadata
    except Exception as e:
        print(f"Error loading metadata: {str(e)}")
        return None

# Function to extract features from audio files
def extract_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, duration=30)

        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        zero_crossing_rate = librosa.feature.zero_crossing_rate(y)

        features = {
            'mfcc_mean': np.mean(mfccs, axis=1).tolist(),
            'mfcc_std': np.std(mfccs, axis=1).tolist(),
            'spectral_centroid_mean': np.mean(spectral_centroid).item(),
            'zero_crossing_rate_mean': np.mean(zero_crossing_rate).item()
        }

        return features

    except Exception as e:
        print(f"Error extracting features from {audio_path}: {str(e)}")
        return None

# Function to connect to MongoDB and load data
def load_to_mongodb(data, collection_name):
    try:
        # Provide MongoDB Atlas connection string
        client = MongoClient('mongodb+srv://Tashfeen:helloworld@cluster0.4nmnavg.mongodb.net/')
        db = client['music']
        # Provide MongoDB Atlas collection name
        collection = db[collection_name]
        collection.insert_many(data)
        print("Data loaded into MongoDB successfully.")
    except Exception as e:
        print(f"Error loading data into MongoDB: {str(e)}")

if __name__ == "__main__":
    # Paths
    metadata_file = 'fma_metadata/tracks.csv'
    audio_folder = '000'

    # Load metadata
    metadata = load_metadata(metadata_file)

    if metadata is not None:
        # Extract features and create documents for MongoDB
        data_to_insert = []
        for track_id, track_info in metadata.iterrows():
            audio_path = os.path.join(audio_folder, f"{track_id:06}.mp3")
            if os.path.exists(audio_path):
                features = extract_features(audio_path)
                if features is not None:
                    document = {
                        'track_id': track_id,
                        'genres': track_info['track', 'genres'],
                        'features': features
                    }
                    data_to_insert.append(document)

        # Load data into MongoDB
        if data_to_insert:
            load_to_mongodb(data_to_insert, 'audio_features')
        else:
            print("No data to insert into MongoDB.")
    else:
        print("Failed to load metadata.")
