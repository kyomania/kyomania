"""Blender-Bildfolgen (RGBA, 540x960) -> Szenen-Clips 1080x1920 mit Pastell-Verlauf."""
import subprocess, sys, numpy as np, cv2, os
GR = {1: ("#b8b0f5", "#93c4f3"), 2: ("#9fc0f5", "#f3b6d6"), 3: ("#c6cff6", "#cdb2f2"), 4: ("#b6b0f4", "#a9c4f6")}
def hx(h): return np.array([int(h[i:i+2], 16) for i in (5, 3, 1)], np.float32)  # BGR
for s in [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4]:
    a, b = hx(GR[s][0]), hx(GR[s][1]); y = np.linspace(0, 1, 1920)[:, None, None]
    bg = (a * (1 - y) + b * y) * np.ones((1920, 1080, 3), np.float32)
    # weicher heller Schein in der Mitte
    yy, xx = np.mgrid[0:1920, 0:1080]; g = np.exp(-(((xx - 540) / 700) ** 2 + ((yy - 1000) / 900) ** 2))[..., None]
    bg = bg * (1 - 0.25 * g) + 255 * 0.25 * g
    cv2.imwrite(f"blender/bg{s}.png", bg.astype(np.uint8))
    out = f"brand-reel/assets/video/s{s}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", f"blender/bg{s}.png", "-framerate", "24", "-i", f"blender/frames/s{s}/f%04d.png",
        "-filter_complex", "[1]scale=1080:1920:flags=lanczos[fg];[0][fg]overlay=shortest=1,format=yuv420p",
        "-r", "24", "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-movflags", "+faststart", out], check=True)
    print("encoded", out)
