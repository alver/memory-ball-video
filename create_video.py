#!/usr/bin/env python3
"""
Memory Ball Video Maker
Creates videos with transitions from photos for Memory Ball (Electronic Ball UM-ER-02)

Author: alver
License: MIT
Repository: https://github.com/alver/memory-ball-video
"""

import os
import sys
import subprocess
import random
from pathlib import Path
import tempfile
import shutil

def get_video_duration(video_path):
    """Get video duration using ffprobe"""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)],
        capture_output=True, text=True, check=True
    )
    return float(result.stdout.strip())

def get_scale_filter(mode='crop'):
    """
    Get FFmpeg video filter for scaling/cropping to 480x480
    
    Modes:
    - 'crop': Crop center to square (no black bars, may lose edges)
    - 'pad': Add black bars to fit (shows full image)
    - 'blur': Blurred background with original centered (artistic)
    - 'stretch': Stretch to fit (distorts image - not recommended)
    """
    
    if mode == 'crop':
        # Crop center to square, then scale to 480x480
        return "scale='min(iw,ih)':'min(iw,ih)',crop=480:480,scale=480:480,setsar=1"
    
    elif mode == 'pad':
        # Scale to fit within 480x480, add black bars
        return "scale=480:480:force_original_aspect_ratio=decrease,pad=480:480:(ow-iw)/2:(oh-ih)/2:black,setsar=1"
    
    elif mode == 'blur':
        # Blurred background + original image centered
        return "[0:v]scale=480:480:force_original_aspect_ratio=increase,crop=480:480,boxblur=20[bg];[0:v]scale=480:480:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1"
    
    elif mode == 'stretch':
        # Stretch to 480x480 (not recommended)
        return "scale=480:480,setsar=1"
    
    else:
        # Default to crop
        return "scale='min(iw,ih)':'min(iw,ih)',crop=480:480,scale=480:480,setsar=1"

def create_video_from_images(input_folder, output_file="output.mp4", duration=5, 
                            transition_duration=1, music_folder=None, first_photos=None,
                            scale_mode='crop'):
    """
    Create video from images with random transitions and music.
    
    Args:
        input_folder: Path to folder with images
        output_file: Output video filename
        duration: Duration to show each photo (seconds)
        transition_duration: Transition duration between photos (seconds)
        music_folder: Path to folder with music files (optional)
        first_photos: List of filenames to show first in specified order (optional)
        scale_mode: How to handle non-square images ('crop', 'pad', 'blur', 'stretch')
    """
    
    # All available xfade transitions
    transitions = [
        'fade', 'dissolve', 'circleopen', 'circleclose', 'fadeblack',
        'smoothleft', 'smoothright', 'smoothup', 'smoothdown',
        'wipeleft', 'wiperight', 'wipeup', 'wipedown',
        'slideleft', 'slideright', 'slideup', 'slidedown',
    ]
    
    # Get list of images
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    all_images = {f.name: f for f in Path(input_folder).iterdir() 
                  if f.suffix.lower() in image_extensions}
    
    if not all_images:
        print(f"Error: No images found in folder {input_folder}")
        return
    
    # Build final photo list
    images = []
    
    # First add fixed photos (if specified)
    if first_photos:
        print("Fixed photos at the beginning:")
        for idx, photo_name in enumerate(first_photos, 1):
            if photo_name in all_images:
                images.append(all_images[photo_name])
                print(f"  {idx}. {photo_name}")
                # Remove from list to avoid duplicates
                del all_images[photo_name]
            else:
                print(f"  WARNING: {photo_name} not found in folder!")
    
    # Remaining photos in random order
    remaining_images = list(all_images.values())
    random.shuffle(remaining_images)
    images.extend(remaining_images)
    
    print(f"\nTotal images: {len(images)}")
    if first_photos:
        print(f"  - Fixed at beginning: {len(first_photos)}")
        print(f"  - Random: {len(remaining_images)}")
    print(f"Parameters: {duration}s/photo, transition {transition_duration}s")
    print(f"Scale mode: {scale_mode}")
    
    # Get music files
    music_files = []
    if music_folder and Path(music_folder).exists():
        music_extensions = {'.mp3', '.m4a', '.wav', '.aac'}
        music_files = [f for f in Path(music_folder).iterdir() 
                      if f.suffix.lower() in music_extensions]
        if music_files:
            print(f"Found {len(music_files)} music files")
    
    # Get scale filter for this mode
    scale_filter = get_scale_filter(scale_mode)
    
    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp())
    
    try:
        print("\nStage 1: Creating video clips from photos...")
        
        # Create intermediate video for each photo
        video_clips = []
        for i, img in enumerate(images):
            clip_file = temp_dir / f"clip_{i:04d}.mp4"
            
            if i % 10 == 0 or i == len(images) - 1:
                print(f"  Processing photo {i+1}/{len(images)}...")
            
            # Create video from single photo with proper scaling
            cmd = [
                'ffmpeg',
                '-loop', '1',
                '-i', str(img),
                '-t', str(duration),
                '-vf', f'fps=30,{scale_filter},format=yuv420p',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-crf', '23',
                '-pix_fmt', 'yuv420p',
                '-an',  # No audio
                '-y',
                str(clip_file)
            ]
            
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            video_clips.append(clip_file)
        
        print("\nStage 2: Merging with transitions...")
        
        # Merge clips with transitions
        if len(video_clips) == 1:
            video_no_music = video_clips[0]
        else:
            current_clips = video_clips.copy()
            merge_round = 0
            
            while len(current_clips) > 1:
                merge_round += 1
                print(f"  Round {merge_round}: merging {len(current_clips)} clips...")
                next_clips = []
                
                i = 0
                while i < len(current_clips):
                    if i + 1 < len(current_clips):
                        merged_file = temp_dir / f"merge_r{merge_round}_{i:04d}.mp4"
                        transition = random.choice(transitions)
                        
                        # Get durations of both clips
                        dur1 = get_video_duration(current_clips[i])
                        dur2 = get_video_duration(current_clips[i + 1])
                        
                        # Final duration accounting for transition overlap
                        output_duration = dur1 + dur2 - transition_duration
                        offset = dur1 - transition_duration
                        
                        cmd = [
                            'ffmpeg',
                            '-i', str(current_clips[i]),
                            '-i', str(current_clips[i + 1]),
                            '-filter_complex',
                            f"[0:v][1:v]xfade=transition={transition}:duration={transition_duration}:offset={offset}[v]",
                            '-map', '[v]',
                            '-c:v', 'libx264',
                            '-preset', 'ultrafast',
                            '-crf', '23',
                            '-pix_fmt', 'yuv420p',
                            '-t', str(output_duration),
                            '-y',
                            str(merged_file)
                        ]
                        
                        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        next_clips.append(merged_file)
                        i += 2
                    else:
                        # Odd clip - carry over as is
                        next_clips.append(current_clips[i])
                        i += 1
                
                current_clips = next_clips
            
            video_no_music = current_clips[0]
        
        # Get actual duration of final video
        video_duration = get_video_duration(video_no_music)
        print(f"\n  Actual video duration: {video_duration:.1f} seconds")
        
        print("\nStage 3: Adding music...")
        
        if music_files:
            # Create looped music of needed length
            looped_music = temp_dir / "looped_music.m4a"
            
            # Create music list with repeats until needed duration
            music_list = temp_dir / "music_list.txt"
            
            # Calculate total music duration
            music_durations = []
            for music in music_files:
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                     '-of', 'default=noprint_wrappers=1:nokey=1', str(music)],
                    capture_output=True, text=True, check=True
                )
                music_dur = float(result.stdout.strip())
                music_durations.append(music_dur)
            
            # Create list with repeats
            with open(music_list, 'w', encoding='utf-8') as f:
                current_duration = 0
                while current_duration < video_duration:
                    for idx, music in enumerate(music_files):
                        f.write(f"file '{music.absolute()}'\n")
                        current_duration += music_durations[idx]
                        if current_duration >= video_duration:
                            break
            
            # Concatenate music into single file
            print("  Creating looped audio...")
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(music_list),
                '-t', str(video_duration),
                '-c:a', 'aac',
                '-b:a', '192k',
                '-y',
                str(looped_music)
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Add audio to video
            print("  Combining video and audio...")
            cmd = [
                'ffmpeg',
                '-i', str(video_no_music),
                '-i', str(looped_music),
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-shortest',
                '-y',
                output_file
            ]
            subprocess.run(cmd, check=True)
        else:
            # No music - just copy
            cmd = [
                'ffmpeg',
                '-i', str(video_no_music),
                '-c', 'copy',
                '-y',
                output_file
            ]
            subprocess.run(cmd, check=True)
        
        print(f"\n✅ Video successfully created: {output_file}")
        print(f"   Duration: {video_duration:.1f} seconds ({len(images)} photos)")
        
    finally:
        # Remove temporary files
        print("\nCleaning up temporary files...")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_video.py <photo_folder> [output_file.mp4] [duration] [transition_duration] [--music music_folder] [--first photo1.jpg photo2.jpg ...] [--mode crop|pad|blur|stretch]")
        print("\nExamples:")
        print("  python create_video.py ./photos")
        print("  python create_video.py ./photos output.mp4 5 1")
        print("  python create_video.py ./photos output.mp4 5 1 --music ./music")
        print("  python create_video.py ./photos output.mp4 5 1 --first IMG_001.jpg IMG_002.jpg IMG_003.jpg")
        print("  python create_video.py ./photos output.mp4 5 1 --mode blur")
        print("  python create_video.py ./photos output.mp4 5 1 --music ./music --mode pad")
        print("\nScale modes:")
        print("  crop   - Crop center to square (default, no black bars)")
        print("  pad    - Add black bars to show full image")
        print("  blur   - Blurred background with original centered")
        print("  stretch - Stretch to fit (distorts image)")
        sys.exit(1)
    
    folder = sys.argv[1]
    output = "output.mp4"
    dur = 5
    trans = 1
    music_path = None
    first_photos_list = None
    mode = 'crop'  # Default mode
    
    i = 2
    positional_count = 0
    
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == '--music':
            if i + 1 < len(sys.argv):
                music_path = sys.argv[i + 1]
                i += 1
        elif arg == '--mode':
            if i + 1 < len(sys.argv):
                mode = sys.argv[i + 1]
                if mode not in ['crop', 'pad', 'blur', 'stretch']:
                    print(f"Warning: Unknown mode '{mode}', using 'crop'")
                    mode = 'crop'
                i += 1
        elif arg == '--first':
            # Collect all filenames after --first until next -- or end
            first_photos_list = []
            i += 1
            while i < len(sys.argv) and not sys.argv[i].startswith('--'):
                first_photos_list.append(sys.argv[i])
                i += 1
            i -= 1  # Step back one to not skip next argument
        elif not arg.startswith('--'):
            if positional_count == 0:
                output = arg
            elif positional_count == 1:
                try:
                    dur = float(arg)
                except ValueError:
                    pass
            elif positional_count == 2:
                try:
                    trans = float(arg)
                except ValueError:
                    pass
            positional_count += 1
        
        i += 1
    
    create_video_from_images(folder, output, dur, trans, music_path, first_photos_list, mode)
