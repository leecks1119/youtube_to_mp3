import os
from pytube import YouTube
from moviepy.editor import *

def lambda_handler(event, context):
    # 이벤트로부터 유튜브 링크 추출
    youtube_link = event['youtube_link']

    # 유튜브 동영상 다운로드
    video = YouTube(youtube_link)
    video_stream = video.streams.filter(only_audio=True).first()
    video_stream.download('/tmp')

    # 다운로드한 동영상에서 소리 추출
    video_path = '/tmp/' + video_stream.default_filename
    audio_path = '/tmp/audio.mp3'
    video_clip = AudioFileClip(video_path)
    video_clip.write_audiofile(audio_path)

    # MP3 파일을 로컬 디렉토리로 이동
    output_path = '/tmp/output.mp3'
    os.rename(audio_path, output_path)

    return {
        'statusCode': 200,
        'body': output_path
    }
