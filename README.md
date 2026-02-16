# Memory Ball Video Maker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)

[GitHub Repo](https://github.com/alver/memory-ball-video)

**Keywords:** memory ball video, electronic ball, magic crystal ball, crystal ball display, video electronic ball, video crystal ball, UM-ER-02, photo slideshow maker, ffmpeg video transitions, free video maker, photo to video converter, slideshow with music, 480x480 video, memory ball software alternative, create video from photos, ffmpeg slideshow, python video maker, photo video editor free, xfade transitions, memory sphere video, memory orb video, dream sphere ball, crystal ball video player, 3D crystal ball, memory sphere lamp, electronic crystal ball

[Русская версия / Russian Version](/memory-ball-video/README.ru.html)

---

## What is Memory Ball?

Memory Ball (also sold as Memory Orb, Memory Sphere, Dream Sphere, Crystal Ball Video Player, and under model names like UM-ER-02) is a small spherical device with a built-in screen that plays videos. It has become a popular personalized gift — people load them with family photos, ultrasound images, wedding memories, or any other meaningful content.

The sphere is typically about 2.7 inches (70mm) in diameter, has a built-in rechargeable battery (2–4 hours of playback), 4GB of internal storage, and a round LCD display with **480×480 pixel resolution**. You load content onto it via USB-C cable or, in newer WiFi models, wirelessly through an app. The device plays MP4 videos and shows JPG images from the memory card.

The catch? There are two:
1. The ball do not play the images from the separate folder, and I didn't find any instruction how to make this work. So, photos and images needs to be cnverted to video.
2. Most manufacturers suggest **paid proprietary software** for creating videos. Some versions come with a "free" app that works, but it's limited and often poorly made.

**You don't need their software.** Everything it does — and much more — can be done for free with **FFmpeg**.

---

## FFmpeg: the tool that does everything with video

[FFmpeg](https://ffmpeg.org/) is a free, open-source command-line tool for working with video, audio, and images. It has been around since 2000, it is used by huge companies (YouTube, Netflix, VLC, even NASA's Perseverance rover on Mars), and it can handle practically any multimedia task you can imagine.

Here's what matters for us: **FFmpeg can do anything you'd ever want to do to prepare video for Memory Ball, and it does it for free.**

### What FFmpeg can do (examples)

**Convert video format and resolution.** Have an MP4 in 1080p? Convert it to 480×480 in one command:

```bash
ffmpeg -i input.mp4 -vf "scale=480:480" -c:v libx264 output.mp4
```

**Create a video from photos.** Have a folder of JPGs? Turn them into a slideshow:

```bash
ffmpeg -framerate 1/5 -pattern_type glob -i '*.jpg' -vf "scale=480:480" -c:v libx264 -pix_fmt yuv420p slideshow.mp4
```

This shows each photo for 5 seconds. Change `1/5` to `1/3` for 3 seconds, `1/10` for 10, and so on.

**Add transitions between photos.** FFmpeg supports dozens of transition effects (crossfade, dissolve, wipe, slide, circle reveal, and more) through its `xfade` filter. This is exactly what the paid Memory Ball software does — but FFmpeg does it better and with more options.

**Add music to a video.** Overlay an audio track on your slideshow:

```bash
ffmpeg -i video.mp4 -i music.mp3 -c:v copy -c:a aac -shortest output.mp4
```

**Loop music to match video length:**

```bash
ffmpeg -i video.mp4 -stream_loop -1 -i music.mp3 -c:v copy -c:a aac -shortest output.mp4
```

**Crop, pad, or resize any video.** Square crop from the center:

```bash
ffmpeg -i input.mp4 -vf "crop=min(iw\,ih):min(iw\,ih),scale=480:480" output.mp4
```

Add black bars to fit without cropping:

```bash
ffmpeg -i input.mp4 -vf "scale=480:480:force_original_aspect_ratio=decrease,pad=480:480:(ow-iw)/2:(oh-ih)/2" output.mp4
```

**Trim a video.** Cut out a specific segment:

```bash
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:01:00 -c copy clip.mp4
```

**Create collages and picture-in-picture.** Combine multiple videos into one frame:

```bash
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex "[0:v]scale=240:240[left];[1:v]scale=240:240[right];[left][right]hstack" collage.mp4
```

**Extract frames from video.** Pull out individual images:

```bash
ffmpeg -i video.mp4 -vf "fps=1" frame_%04d.jpg
```

**Convert between any formats.** MP4, AVI, MOV, MKV, WebM, GIF — FFmpeg handles them all. It supports virtually every video and audio codec in existence.

### The point

FFmpeg is an incredibly powerful and flexible tool. The paid software that comes with Memory Ball does one simple thing: it creates a slideshow from photos with some transitions. FFmpeg can do that and a thousand other things.

You can learn FFmpeg commands yourself, or — even easier — **ask any modern AI assistant** (Claude, ChatGPT, etc.) to write you an FFmpeg command or script for exactly what you need. Describe what you want in plain language, and you'll get a working command in seconds.

---

## Script in repo: a ready-made example

As a practical example, I've written a Python script that automates one of the most common tasks: creating a video slideshow from photos with random transitions and optional background music. It's designed specifically for Memory Ball's 480×480 format, but it can be adapted for anything.

You can use this script as-is, modify it, or just use it as inspiration to write your own. The script is available at [GitHub](https://github.com/alver/memory-ball-video).

### What the script does

- Takes a folder of photos and creates an MP4 video with transitions
- Randomly selects from 16 different transition effects (fade, dissolve, wipe, slide, circle, smooth, and more)
- Optionally adds background music that loops to match video length
- Lets you specify which photos appear first (the rest are randomized)
- Outputs 480×480 MP4 ready for Memory Ball
- Automatically handles photos of any size — crops, pads, or blurs to fit (configurable)

### Requirements

You need **Python 3.7+** and **FFmpeg** installed:

- **Windows:** Download Python from [python.org](https://www.python.org/downloads/), FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) (add to PATH)
- **macOS:** `brew install python3 ffmpeg`
- **Linux:** `sudo apt install python3 ffmpeg`

Verify both are working:

```bash
python --version
ffmpeg -version
```

### Quick start

1. Download `create_video.py` from the [repository](https://github.com/alver/memory-ball-video)
2. Put your photos in a `photos/` folder
3. Run:

```bash
python create_video.py --photos ./photos
```

That's it. You'll get `output.mp4` ready for your Memory Ball.

### More options

```bash
# Custom filename, 7 seconds per photo, 1.5 second transitions
python create_video.py --photos ./photos --output my_video.mp4 --duration 7 --transition 1.5

# Add background music
python create_video.py --photos ./photos --music ./music

# Show specific photos first, then randomize the rest
python create_video.py --photos ./photos --first favorite1.jpg favorite2.jpg

# Choose how non-square photos are handled: crop (default), pad, blur, or stretch
python create_video.py --photos ./photos --mode blur

# Everything together
python create_video.py --photos ./photos --output memory_ball.mp4 --duration 6 --transition 1 --music ./music --first cover.jpg intro.jpg --mode blur
```

### Parameters

| Parameter | What it does | Default |
|-----------|-------------|---------|
| `--photos <folder>` | Folder with your photos | Required |
| `--output <file>` | Output filename | `output.mp4` |
| `--duration <seconds>` | Seconds per photo | `5` |
| `--transition <seconds>` | Transition duration in seconds | `1` |
| `--music <folder>` | Folder with music files (MP3, M4A, WAV) | None |
| `--first <files...>` | Photos to show first (in order) | None |
| `--mode <mode>` | How to handle non-square photos: `crop`, `pad`, `blur`, `stretch` | `crop` |

### Available transitions

The script randomly picks from: `fade`, `dissolve`, `wipeleft`, `wiperight`, `wipeup`, `wipedown`, `slideleft`, `slideright`, `slideup`, `slidedown`, `circleopen`, `circleclose`, `smoothleft`, `smoothright`, `smoothup`, `smoothdown`, `fadeblack`.

### Photo scaling modes

- **crop** (default) — Crops to square from center. No black bars, but edges may be cut off.
- **pad** — Adds black bars to fit the full image. Shows everything, but with letterboxing.
- **blur** — Uses a blurred version of the photo as background with the original centered on top. Artistic effect, no bars.
- **stretch** — Stretches to 480×480. Distorts the image, not recommended.

### Folder structure

```
my-project/
├── photos/           # Your photos (JPG, PNG, BMP)
├── music/            # Music files (optional)
└── create_video.py   # The script
```

---

## Troubleshooting

**"FFmpeg not found"** — Make sure FFmpeg is installed and in your system PATH. Test with `ffmpeg -version`.

**"No images found"** — Check that your photos are in the right folder and are `.jpg`, `.jpeg`, `.png`, or `.bmp`.

**Video is too short or too long** — Adjust the `duration` parameter. Total time = number of photos × duration.

**Processing takes a long time** — This is normal for hundreds of photos. For 100 photos it typically takes 1–5 minutes. The script processes in batches.

---

## Technical details

- Output: MP4 (H.264 video, AAC audio)
- Resolution: 480×480
- Frame rate: 30 fps
- Audio: 192 kbps

---

## License

MIT — use, modify, and distribute freely.

---

## The bigger picture

I believe you shouldn't have to pay for basic video creation. FFmpeg is free, powerful, and can do everything the paid Memory Ball software does — and much more. Modern AI assistants make it easy for anyone to write custom scripts and commands. This project is just one example of what's possible.

Don't just use this script — understand the approach. FFmpeg is the real tool. Learn it, ask AI to help you with it, or write your own scripts. You have full control.
