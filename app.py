import streamlit as st
import json
import yt_dlp

def extract_format_data(format_data):
    return {
        "extension": format_data["ext"],
        "format_name": format_data["format"],
        "url": format_data["url"]
    }

def get_youtube_dl_output(video_url):
    with yt_dlp.YoutubeDL({'format': 'bestvideo+bestaudio/best', 'quiet': True, 'dump_single_json': True}) as ydl:
        try:
            return json.dumps(ydl.extract_info(video_url, download=False))
        except Exception as e:
            st.error(f"Error: {e}")
            return None

def extract_video_data_from_url(video_url):
    output = get_youtube_dl_output(video_url)
    return json.loads(output) if output else None

st.set_page_config(page_title="Download Station", layout="wide")

st.header("Download Video")
video_url = st.text_input("Enter video URL")
download_type = st.radio("Select Download Type", ('Video', 'Audio'))

if st.button("Download"):
    with st.spinner("Downloading... Please wait."):
        if video_url:
            video_data = extract_video_data_from_url(video_url)
            if video_data:
                st.write(f"### {video_data['title']}")
                st.image(video_data["thumbnail"])
                st.write("### Available Formats")
                formats = video_data["formats"]

                for fmt in formats:
                    if (download_type == 'Video' and fmt['vcodec'] != 'none' and fmt['acodec'] != 'none') or \
                       (download_type == 'Audio' and fmt['vcodec'] == 'none' and fmt['ext'] not in ['mhtml', 'html', 'txt', 'json']):
                        format_info = extract_format_data(fmt)
                        st.download_button(
                        label=f"{'📥'if download_type == 'Video' else '🎵'} Download {format_info['format_name']} ({format_info['extension']})",
                            data=format_info['url'],
                            file_name=f"{video_data['title']}.{format_info['extension']}",
                            mime=f"{'video' if download_type == 'Video' else 'audio'}/{format_info['extension']}"
                        )
            else:
                st.error("Failed to retrieve video data.")
        else:
            st.error("Please enter a valid YouTube video URL.")

st.markdown('</div>', unsafe_allow_html=True)  # Close the container div
