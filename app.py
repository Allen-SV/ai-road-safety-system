import streamlit as st
import tempfile
import os
import cv2
from tracker import process_video

st.set_page_config(page_title="Traffic Analysis Dashboard", layout="wide")

st.title("🚦 Traffic & Road Safety Analysis Dashboard")
st.markdown("Upload a video or select an existing one to analyze traffic, detect potholes, check for helmets, and monitor for crashes in real-time.")

# Sidebar for controls
st.sidebar.header("Video Source")

# Option to choose between existing videos or uploading a new one
source_option = st.sidebar.radio("Select Video Source", ("Upload New Video", "Use Existing Video"))

video_path = None

if source_option == "Upload New Video":
    uploaded_file = st.sidebar.file_uploader("Upload a video file (MP4)", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        # Save the uploaded video to a temporary file
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_file.read())
        tfile.flush()
        tfile.close() # Close it so opencv can read it on Windows
        video_path = tfile.name
else:
    # Scan current directory for mp4 files
    existing_videos = [f for f in os.listdir(".") if f.endswith('.mp4')]
    if existing_videos:
        selected_video = st.sidebar.selectbox("Select an existing video", existing_videos)
        video_path = selected_video
    else:
        st.sidebar.error("No mp4 files found in the current directory.")

if "analyze" not in st.session_state:
    st.session_state.analyze = False

# Start analysis button
if st.sidebar.button("Start Analysis"):
    st.session_state.analyze = True

if st.session_state.analyze:
    if video_path is None or not os.path.exists(video_path):
        st.error("Please provide a valid video file.")
        st.session_state.analyze = False
    else:
        st.success(f"Processing: {os.path.basename(video_path)}")
        
        # Create a placeholder in the UI for the video frames
        frame_placeholder = st.empty()
        
        # Adding a stop button feature via session state properly
        if st.button("Stop Analysis"):
            st.session_state.analyze = False
            st.warning("Analysis Stopped.")
            st.stop()
        
        # Process the video stream and update the placeholder
        try:
            for frame in process_video(video_path):
                frame_placeholder.image(frame, channels="RGB", use_container_width=True)
            if st.session_state.analyze:
                st.success("Analysis Complete!")
                st.session_state.analyze = False
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
            st.session_state.analyze = False
            
        # Clean up temporary file if we uploaded one
        if source_option == "Upload New Video" and video_path is not None:
            try:
                os.remove(video_path)
            except:
                pass
