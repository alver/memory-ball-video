# Memory Ball Video Maker

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)

[GitHub Repo](https://github.com/alver/memory-ball-video)

**Keywords:** memory ball video, electronic ball, magic crystal ball, crystal ball display, video electronic ball, video crystal ball, UM-ER-02, photo slideshow maker, ffmpeg video transitions, free video maker, photo to video converter, slideshow with music, 480x480 video, memory ball software alternative, create video from photos, ffmpeg slideshow, python video maker, photo video editor free, xfade transitions, memory sphere video

[Русская версия / Russian Version](README.ru.md)

---

## 🎯 About This Project

This is a **free, open-source alternative** to paid software for creating videos from photos for Memory Ball.

## The Core Idea: FFmpeg Can Do It All

**You don't actually need this specific script!** The key insight is that **FFmpeg** - a free, powerful multimedia tool - can create professional videos with transitions from your photos. This script is just **one example** of how to automate the process.

### Why This Matters

- **Memory Ball manufacturers** suggest to use paid software for creating 480x480 videos
- **FFmpeg is free** and can do everything their paid software does
- **Modern AI assistants** (like Claude, ChatGPT, etc.) can write custom scripts for your specific needs in minutes
- **You have full control** - modify, adapt, or completely rewrite for your use case

### How to Approach This Task

1. **Use FFmpeg directly** - Learn FFmpeg commands and create videos manually
2. **Use this script** - A ready-made Python solution for common scenarios
3. **Ask an AI to write custom code** - Get a script tailored to your exact requirements
4. **Modify this script** - Adapt it to your specific workflow

**Bottom line:** Don't feel locked into paid software. FFmpeg + a bit of scripting (or AI help) gives you unlimited freedom!

---

## ⚠️ Important: Photo Preparation Required

**Before using the script, you must prepare your photos:**

### Photo Requirements
- **Exact size: 480×480 pixels**
- **Aspect ratio: 1:1 (square)**
- The script does **NOT** crop or resize photos automatically (yet)

### Why This Matters
Memory Ball requires exactly 480×480 pixel videos. If your photos are not square (480×480), the script will:
- Scale them to fit 480×480 (may add black bars)
- Potentially distort the image
- Not give optimal results

### How to Prepare Photos

**Option 1: Use Image Editing Software**
- Photoshop, GIMP, or any image editor
- Crop each photo to square (1:1 ratio)
- Resize to exactly 480×480 pixels
- Save as JPG or PNG

**Option 2: Batch Processing Tools**
- **Windows:** IrfanView (free), XnConvert
- **macOS:** Preview (built-in), Automator
- **Linux:** ImageMagick, GIMP batch mode

**Option 3: ImageMagick Command Line**
```bash
# Crop to square (center) and resize to 480x480
magick convert input.jpg -resize 480x480^ -gravity center -extent 480x480 output.jpg

# Batch process all photos in folder
for img in *.jpg; do magick convert "$img" -resize 480x480^ -gravity center -extent 480x480 "processed_$img"; done
```

### Best Practice
1. Create a folder `photos_original/` with your original photos
2. Process and crop all photos to 480×480
3. Save processed photos to `photos/` folder
4. Run the script on the `photos/` folder

---

## ✨ What This Script Does

Create beautiful videos with transitions from your photos for **Memory Ball (Electronic Ball UM-ER-02)** - completely **FREE** and **open-source**!

## 🤖 Want a Custom Solution?

**This script is just one example!** Modern AI assistants can create custom scripts for your specific needs:

- Different video sizes or formats
- Custom transition patterns
- Specific timing requirements
- Integration with your existing workflow
- Additional effects or features

**Try asking an AI assistant:**
> "Write me a Python script using FFmpeg to create a video from photos with crossfade transitions, 720p resolution, and background music that loops."

Most modern LLMs (Claude, ChatGPT, etc.) can write working code in minutes. **You're not limited to this script - you have the power to create exactly what you need!**

---

Memory Ball (Electronic Ball UM-ER-02) is a spherical device that displays photos and videos. It requires videos in a specific format: **480x480 pixels, MP4 format**.

## ✨ Features

- ✅ **Random transitions** - 16 different transition effects between photos
- ✅ **Background music** - Add looping music from MP3/M4A/WAV files
- ✅ **Custom photo order** - Specify which photos to show first, rest are randomized
- ✅ **Correct format** - Automatically creates 480x480 videos for Memory Ball
- ✅ **Free & Open Source** - No paid software needed!
- ✅ **Handles large batches** - Works with hundreds of photos

## 📋 Requirements

### Required Software

1. **Python 3.7+**
   - Windows: Download from [python.org](https://www.python.org/downloads/)
   - macOS: `brew install python3`
   - Linux: `sudo apt install python3`

2. **FFmpeg**
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### Verify Installation

```bash
python --version
ffmpeg -version
```

## 🚀 Quick Start

### 1. Download the Script

```bash
git clone https://github.com/YOUR_USERNAME/memory-ball-video-maker.git
cd memory-ball-video-maker
```

Or download `create_video.py` directly.

### 2. Prepare Your Files

```
my-project/
├── photos/          # Your photos here (JPG, PNG)
│   ├── IMG_001.jpg
│   ├── IMG_002.jpg
│   └── ...
├── music/           # Your music here (MP3, M4A, WAV) [optional]
│   ├── track1.mp3
│   └── track2.mp3
└── create_video.py  # The script
```

### 3. Run the Script

**Basic usage (random order):**
```bash
python create_video.py ./photos
```

**With custom settings:**
```bash
python create_video.py ./photos output.mp4 5 1
```
- `5` = seconds per photo
- `1` = transition duration

**With music:**
```bash
python create_video.py ./photos output.mp4 5 1 --music ./music
```

**With specific photos first:**
```bash
python create_video.py ./photos output.mp4 5 1 --first IMG_001.jpg IMG_002.jpg IMG_003.jpg
```

**Full example (music + fixed order):**
```bash
python create_video.py ./photos my_video.mp4 5 1 --music ./music --first favorite1.jpg favorite2.jpg
```

## 📖 Usage

### Command Syntax

```bash
python create_video.py <photo_folder> [output_file] [duration] [transition] [options]
```

### Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `photo_folder` | Path to folder with photos | Required | `./photos` |
| `output_file` | Output video filename | `output.mp4` | `my_video.mp4` |
| `duration` | Seconds per photo | `5` | `7` |
| `transition` | Transition duration (seconds) | `1` | `1.5` |

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `--music <folder>` | Add background music from folder | `--music ./music` |
| `--first <files...>` | Show specific photos first (in order) | `--first photo1.jpg photo2.jpg` |

### Examples

**1. Simple video (all random):**
```bash
python create_video.py ./photos
```

**2. Longer display time:**
```bash
python create_video.py ./photos video.mp4 10 1.5
```
Each photo shows for 10 seconds, transitions last 1.5 seconds

**3. With background music:**
```bash
python create_video.py ./photos video.mp4 5 1 --music ./my_music
```
Music loops automatically to match video length

**4. Important photos first, then random:**
```bash
python create_video.py ./photos video.mp4 5 1 --first wedding_001.jpg wedding_002.jpg wedding_005.jpg
```

**5. Complete setup:**
```bash
python create_video.py ./photos memory_ball.mp4 6 1 --music ./music --first cover.jpg intro.jpg
```

## 🎨 Available Transitions

The script randomly selects from 16 different transitions:

- `fade` - Classic crossfade
- `dissolve` - Dissolve effect
- `wipeleft/right/up/down` - Wipe transitions
- `slideleft/right/up/down` - Slide transitions
- `circleopen/close` - Circular reveal/hide
- `smoothleft/right/up/down` - Smooth slide
- `fadeblack` - Fade through black

Each transition is randomly chosen between photos for variety!

## 🎵 Music Support

- **Formats**: MP3, M4A, WAV, AAC
- **Looping**: Music automatically loops to match video length
- **Multiple tracks**: Place multiple files in music folder - they play in sequence then loop

**Music folder example:**
```
music/
├── song1.mp3
├── song2.mp3
└── song3.m4a
```

Playback order: song1 → song2 → song3 → song1 → song2 → ...

## 💡 Tips

1. **Photo quality**: Use 480x480 or larger photos for best quality
2. **Many photos**: Script handles 200+ photos without issues
3. **Processing time**: Depends on number of photos (1-5 minutes for 100 photos)
4. **Music length**: Can be shorter than video - it will loop automatically
5. **Testing**: Try with a few photos first to check timing

## 🐛 Troubleshooting

**"FFmpeg not found"**
- Make sure FFmpeg is installed and added to system PATH
- Test with: `ffmpeg -version`

**"No images found"**
- Check that photos are in correct folder
- Supported: `.jpg`, `.jpeg`, `.png`, `.bmp`

**Video too short/long**
- Adjust `duration` parameter (seconds per photo)
- Formula: `total_time = number_of_photos × duration`

**"File not found" for --first**
- Make sure filenames are exact (case-sensitive on Linux/Mac)
- Use relative path or just filename if in photos folder

## 🔧 Technical Details

- **Output format**: MP4 (H.264 video, AAC audio)
- **Resolution**: 480x480 pixels (Memory Ball requirement)
- **Frame rate**: 30 fps
- **Audio bitrate**: 192 kbps
- **Processing**: Creates intermediate clips then merges with transitions

## 📝 License

MIT License - feel free to use, modify, and distribute!

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 🙏 Acknowledgments

This project was created to provide a free alternative to paid Memory Ball software. 

**Special thanks to:**
- The open-source community
- FFmpeg developers for creating such a powerful tool
- Modern AI assistants that make coding accessible to everyone
- Everyone who contributes to making technology free and open

**Remember:** This is just one way to solve the problem. FFmpeg is incredibly powerful, and with a bit of help (human or AI), you can create any video workflow you need!

---

## 💭 Philosophy

We believe that:
- **Knowledge should be free** - No one should pay for basic video creation
- **Tools should be accessible** - FFmpeg is free and powerful
- **AI can help everyone** - Modern LLMs democratize coding
- **Open source wins** - Share solutions, help others

**Don't just use this script - understand the approach, adapt it, improve it, or create your own!**

---

## 📞 Support

If you find this useful, please ⭐ star the repository!

For issues or questions, please open a GitHub issue.
