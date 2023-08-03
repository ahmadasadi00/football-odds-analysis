import imageio
import plotly.graph_objects as go
import io
import numpy as np
from PIL import Image

def plotly_fig2array(fig):
    fig_bytes = fig.to_image(format="png")
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)

def plotly_fig_to_video(plotly_fig, video_path: str):
    """A function that gets the plotly animation fig and convert it to a video

    Args:
        plotly_fig (_type_): plotly figure object
        video_path (str): path to save the video
    """
    frames = plotly_fig2array(plotly_fig)
    video_path = f"{video_path}.mp4"
    imageio.mimsave(video_path, frames, fps=10)