The installer build places ffmpeg.exe and ffprobe.exe here, together with FFmpeg's own licence file.
They are not kept in the repository. The build workflow downloads a pinned release and records its checksum.
Cinematic Studio runs FFmpeg as a separate program; it does not link against it.
