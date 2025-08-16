# ShiroInk

ShiroInk is a tool for processing manga images to be optimized for Kindle devices. It supports resizing, sharpening, and saving images in CBZ format.

## Features

- Resize images to a specified resolution
- Sharpen images for better readability
- Save images in CBZ format
- Support for right-to-left (RTL) manga
- Multi-threaded processing

## Requirements

- Python 3.9+
- [Rich](https://github.com/Textualize/rich)
- [Pillow](https://python-pillow.org/)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/esoso/shiroink.git
    cd shiroink
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To process manga images, run the following command:

```sh
python main.py <src_dir> <dest_dir> [options]
```

### Arguments

- `src_dir`: Source directory containing files to process
- `dest_dir`: Destination directory to place processed files

### Options

- `-r, --resolution`: Resolution to resize the images (default: `1072x1448`)
- `--rtl`: Switch the order of two-page images
- `-q, --quality`: Quality level for optimization (1-9, default: `6`)
- `-d, --debug`: Enable debug output
- `-w, --workers`: Number of threads to use (default: `4`)
- `--dry-run`: Show what would be done without actually doing it

### Example

```sh
python main.py /path/to/source /path/to/destination -r 800x600 --rtl -q 3 --debug
```

## Docker

You can also run ShiroInk using Docker:

- Run the Docker container:
    ```sh
    docker run --rm -it \
        -v /path/to/source:/home/shino/src \
        -v /path/to/destination:/home/shino/dest \
        ghcr.io/esoso/shiroink /manga/src /manga/dest
    ```

## License

This project is licensed under the ISC License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Rich](https://github.com/Textualize/rich) for the beautiful console output
- [Pillow](https://python-pillow.org/) for image processing
