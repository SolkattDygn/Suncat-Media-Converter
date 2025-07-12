# Suncat Media Converter

A very simple program to easily convert the audio inside video files to PCM.
Originally created by me to make it easier to convert the audio in my video files for use 
in Davinci Resolve which natively does not support AAC under linux.

It uses ffmpeg to do this but without the hassle of figuring out what to put in terminal.

## Requirements:
- A Debian-based Linux system (e.g., Linux Mint, Ubuntu)
- Python 3 installed (already included on most systems)
- ffmpeg installed
- Basic knowledge of using the terminal

## Install Guide:
### Option 1 (.deb): 
Download the .deb file and install it from terminal with

`sudo dpkg -i suncat-media-converter_<version>.deb`

Replace <version> with the actual version number shown in the filename.

Example:
`sudo dpkg -i suncat-media-converter_1.0.0.deb`

### Option 2 (build from source): 

  #### Step 1: Open a Terminal

  Press Ctrl + Alt + T to open a terminal window.


#### Step 2: Download or Clone This Project

  If you haven't already, download this project folder or clone it from GitHub:

  `git clone https://github.com/SolkattDygn/Suncat-Media-Converter.git`
  `cd Suncat-Media-Converter`

#### Step 3: Build the .deb Package

Navigate within terminal to the folder where you downloaded  Suncat Media Converter to

Copy the following command block and run as a whole in the terminal:

  ```
pkg_dir="suncat-media-converter"
version=$(grep ^Version: "$pkg_dir/DEBIAN/control" | awk '{print $2}')
dpkg-deb --build "$pkg_dir"
mv "$pkg_dir.deb" "${pkg_dir}_${version}.deb"
```

This will create a file named like: suncat-media-converter_1.0.0.deb

#### Step 4: Install the App

Run this command to install the .deb file:

`sudo dpkg -i suncat-media-converter_<version>.deb`

Replace <version> with the actual version number shown in the filename.

Example:

`sudo dpkg -i suncat-media-converter_1.0.0.deb`

#### Step 5: Run the App

After installation, open your application menu and search for:
Suncat Media Converter
Click to launch the app.

#### Notes:
- If the icon doesn’t appear immediately, try logging out and back in.

### Howto Uninstall: 
If you ever want to remove the app:

`sudo dpkg -r suncat-media-converter`
