# GitHub Contribution Graph Art Generator

A simple Python script to draw custom pixel art/messages on your GitHub contribution graph by creating backdated empty commits.

## Preview Example
Below is an example of what a rendered message grid looks like in the terminal:
```text
--- Contribution Graph Preview ---
█...█.█████.█.....█.....█████.█...█.█████.█████.█████...█...
█...█.█.....█.....█.....█...█.█...█.█...█.█...█.█...█...█...
█████.████..█.....█.....█...█.█...█.█...█.█...█.█...█...█...
█...█.█.....█.....█.....█...█.█.█.█.█...█.█████.█...█.......
█...█.█████.█████.█████.█████.██.██.█████.█..█..█████...█...
----------------------------------
```

## How to Use

1. **Create a new, empty repository** on GitHub. It is highly recommended to use a dedicated repository for this so your main project histories aren't cluttered with thousands of empty commits.
2. **Clone** the repository to your local machine.
3. Place `draw_art.py` inside the repository directory.
4. Run the script:
   ```bash
   python draw_art.py
   ```
5. Follow the interactive prompts:
   - **Message**: Enter the text you want to render (e.g., `HELLO WORLD!`).
   - **Target Year**: Enter the year you want the contribution graph art to appear in (e.g. `2024`), or type `rolling` to render it in the last 12 months (current rolling year view on your profile) [Default: `rolling`].
   - **Commits per pixel**: The number of commits to make per pixel. More commits make the green color darker on GitHub (10-50 recommended).
6. Once the script finishes generating the backdated commits, push the changes to GitHub:
   ```bash
   git push origin main
   ```
7. Wait 5-10 minutes for GitHub to rebuild your contribution graph.

## File Structure

- `draw_art.py`: The interactive Python script that renders text into a 7-row grid and creates the backdated empty commits.
- `README.md`: Documentation for the project.
