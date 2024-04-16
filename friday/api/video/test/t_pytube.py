from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=Qofdx9tEWBw')

# stream = yt.streams.first()
# all_streams = yt.streams.all()

for stream in yt.streams.filter(file_extension='mp4'):
    stream.download('./content/video/')