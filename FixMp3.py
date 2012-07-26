#!/usr/bin/env python

import eyeD3
import os
import os.path
import shutil

def sanitize(s):
    if s == None or len(s) == 0:
        s = "Unknown"
    s = s.strip()
    s = s.replace('/', '_')
    s = s.replace('"', '_')
    s = s.replace("'", '_')
    s = s.replace('*', '_')
    s = s.replace('&', '_')
    s = s.replace(' ', '_')
    s = s.replace('__', '_')
    s = s.replace('__', '_')
    s = s.replace('__', '_')
    s = s.replace('.', '')

    if s.startswith('The_') and not s == 'The_The':
        s = s[4:]

    return s

def get_tag(filename):
    tag.link(filename, eyeD3.ID3_V2)

    artist = None
    album = None
    title = None
    artist1 = None
    album1 = None
    title1 = None

    try:
        artist = tag.getArtist()
        album = tag.getAlbum()
        title = tag.getTitle()
        (disc, setSize) = tag.getDiscNum()
        (track, discSize) = tag.getTrackNum()
    except:
        pass

    try:
        tag.link(filename, eyeD3.ID3_V1)
        artist1 = tag.getArtist()
        album1 = tag.getAlbum()
        title1 = tag.getTitle()
        (disc1, setSize) = tag.getDiscNum()
        (track1, setSize) = tag.getTrackNum()
    except:
        pass

    if artist1 != None and (artist == None or artist.strip() == ''):
        artist = artist1

    if album1 != None and (album == None or album.strip() == ''):
        album = album1

    if title1 != None and (title == None or title.strip() == ''):
        title = title1

    artist = sanitize(artist)
    album = sanitize(album)
    title = sanitize(title)

    return (artist, album, title, track, disc)

tag = eyeD3.Tag()
inPath = "iPodMusic"
outPath = "MusicFixed"
maximumFilenameLength = 31
i = 0

if not os.path.exists(outPath):
    os.mkdir(outPath)

# build a list of files
for root, dirs, files in os.walk(inPath):
    for name in files:
        filename = os.path.join(root, name)
        if filename.endswith(".mp3"):
            (artist, album, title, track, disc) = get_tag(filename)

            # make the destination path
            if len(artist) > maximumFilenameLength:
                artist = artist[:maximumFilenameLength]
            if len(album) > maximumFilenameLength:
                album = album[:maximumFilenameLength]
            outTitle = title
            if track != None:
                outTitle = str(track) + "-" + outTitle
            if disc != None:
                outTitle = str(disc) + "-" + outTitle
            if outTitle > maximumFilenameLength - 4:
                outTitle = outTitle[:maximumFilenameLength - 4]

            destPath = os.path.join(outPath, artist)

            if not os.path.exists(destPath):
                os.mkdir(destPath)

            destPath = os.path.join(destPath, album)

            if not os.path.exists(destPath):
                os.mkdir(destPath)

            destPath = os.path.join(destPath, outTitle)
            origDestPath = destPath

            incr = 0
            while os.path.exists(destPath + ".mp3"):
                destPath = origDestPath + str(incr)
                incr += 1

            destPath += ".mp3"

            shutil.copyfile(filename, destPath)

            i += 1
        else:
            print filename

print "Processed ", i, " MP3 files"
