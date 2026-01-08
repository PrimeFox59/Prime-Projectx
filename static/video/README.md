# Video Background

Place your background video here as `bg.mp4`.

## Recommendations:
- **Resolution:** 1920x1080 (Full HD) or 1280x720 (HD)
- **Duration:** 10-30 seconds (looping)
- **Format:** MP4 (H.264 codec)
- **File size:** Keep under 5MB for fast loading
- **Content ideas:**
  - Abstract particles/plexus networks
  - Circuit board animations
  - Digital rain/matrix effect
  - Geometric patterns
  - Nebula/space scenes
  - Tech HUD animations

## Free Resources:
- Pexels Videos: https://www.pexels.com/videos/
- Pixabay: https://pixabay.com/videos/
- Coverr: https://coverr.co/
- Videezy: https://www.videezy.com/

## Optimization:
Use ffmpeg to compress:
```bash
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset slow -vf scale=1280:720 bg.mp4
```

If you don't have a video yet, the app will work fine with particle background only.
