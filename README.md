# stem-extractor

some software to extract stems from a youtube playlist

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the script:

```bash
python yt2stems.py
```

3. Enter the URL of the playlist you want to extract stems from:

![ui](/img/ui.png)

```bash
Enter the URL of the playlist you want to extract stems from: https://www.youtube.com/playlist?<playlist_id>
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
