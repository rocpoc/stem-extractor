# stem-extractor

some software to extract stems from a youtube playlist

## Usage

1. Install dependencies:

```bash
pip3 install -r requirements.txt
```

2. Run the script:

```bash
python3 yt2stems.py
```

3. Enter the URL of the playlist or video you want to extract stems from:

![ui](/img/ui.png)

```output
# playlist:
https://www.youtube.com/playlist?list=PLxxx...
# or single video:
https://www.youtube.com/watch?v=xxxxx
```

4. The script will download the playlist and extract the stems:

```bash
Downloading playlist...
Extracting stems...
```

5. The stems will be saved in the `separated` directory:

```bash
Stems extracted and saved in: separated/
```
