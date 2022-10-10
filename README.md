Image manipulation tool in which you can select a large number of photos and
perform a lot of different operations on them.
---

## Installation

### Install from PyPI

```shell
pip install imgmanip
```

### If you want the program to be displayed in the system applications menu. (Linux only)

#### For current user

```shell
curl https://raw.githubusercontent.com/hawier-dev/imgmanip/develop/imgmanip.desktop > ~/.local/share/applications/imgmanip.desktop
```

#### For all users

```shell
curl https://raw.githubusercontent.com/hawier-dev/imgmanip/develop/imgmanip.desktop > ./imgmanip.desktop
sudo mv ./imgmanip.desktop /usr/share/applications/imgmanip.desktop
```

The current list of operations

- **Resize** - resizes the images to the given resolution or by a specified percentage.
- **Compress** - compresses the image. The lower the 'quality',
  the smaller the file size.
- **Invert** - inverts the colors of the image.
- **Flip** - flips the image in horizontal or vertical axis.
- **Color detection** - marks where the given color appears in the image.
  Additionally, it can save the **mask** in .png format.
- **Convert** - converts the image to the other format.
