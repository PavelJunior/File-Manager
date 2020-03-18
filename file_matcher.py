#!/usr/bin/python3

import re


def is_image(obj):
    match = re.match(r".*(\.jpg|\.jpeg|\.png|\.jpx|\.gif|\.webp|\.cr2|\.tif|\.bmp|\.jxr|\.psd|\.ico|\.heic)$", obj)
    return True if match else False


def is_video(obj):
    match = re.match(r".*(\.mp4|\.m4v|\.mkv|\.webm|\.mov|\.avi|\.wmv|\.mpg|\.flv)$", obj)
    return True if match else False


def is_audio(obj):
    match = re.match(r".*(\.mid|\.mp3|\.m4a|\.ogg|\.flac|\.wav|\.amr)$", obj)
    return True if match else False


def is_archive(obj):
    match = re.match(r".*(\.epub|\.zip|\.tar|\.rar|\.gz|\.bz2|\.7z|\.xz|\.pdf|\.exe|\.swf|\.rtf|\.eot|\.ps|\.sqlite|\.nes|\.crx|\.cab|\.deb|\.ar|\.Z|\.lz)$", obj)
    return True if match else False


def is_font(obj):
    match = re.match(r".*(\.woff|\.woff2|\.ttf|\.otf)$", obj)
    return True if match else False


def file_type(obj):
    type_checks = {
        is_image: 'image',
        is_video: 'video',
        is_audio: 'audio',
        is_archive: 'archive',
        is_font: 'font'
    }

    for function, type in type_checks.items():
        if function(obj):
            return type
    return 'other'