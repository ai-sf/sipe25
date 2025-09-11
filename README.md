# SIPE25 Static Site Mirror

This repository automates the process of mirroring, cleaning, and publishing the static site for [sipe25.com](https://sipe25.com) to [ai-sf.it/sipe25](https://ai-sf.it/sipe25) using GitHub Actions.

While it works in this case, it should in principle work for any Wordpress website, avoiding the limitations of the cheaper plans of wordpress.com.

## Structure

- `.env`: Environment variables for domain and URLs.
- `requirements.txt`: Python dependencies (`beautifulsoup4`, `requests`).
- `scripts/`
  - `download_mirror.sh`: Bash script to download a static mirror using HTTrack.
  - `index_cleanup.py`: Removes redundant `index*.html` files except `index.html`.
  - `fix_links.py`: Cleans up HTML links and image attributes in the mirrored site.
- `.github/workflows/update-mirror.yml`: GitHub Actions workflow for automating the mirror, cleanup, link fixing, image resizing, and publishing to GitHub Pages.

## Usage

### Manual

1. **Download the mirror:**
	```sh
	bash scripts/download_mirror.sh <domain> [output_dir] [depth]
	```
2. **Clean up index files:**
	```sh
	python scripts/index_cleanup.py <mirror_dir>
	```
3. **Fix links:**
	```sh
	python scripts/fix_links.py <mirror_dir> <base_url> <new_base_url>
	```

### Automated (GitHub Actions)

- The workflow is triggered manually.
- It downloads the mirror, cleans and fixes links, resizes images, and publishes to the `gh-pages` branch.

## Environment Variables

Set in `.env`:
```
DOMAIN=sipe25.com
BASE_URL=https://sipe25.com
NEW_BASE_URL=https://ai-sf.it/sipe25
```

## Requirements

- Python 3.x
- HTTrack
- See `requirements.txt` for Python packages.

## License

The code in this branch is licensed under the MIT License (see [LICENSE](LICENSE)).

**Important:** The content published to the `gh-pages` branch (the mirrored website) is subject to its original copyright and is not covered by this license.

## Author

Developed by Dario Zarcone (for AISF).
