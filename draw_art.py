#!/usr/bin/env python3
import datetime
import os
import subprocess
import sys

# Pixel font for rendering text on a 7-row grid (Sunday to Saturday)
FONT = {
    'H': ["#######", "...#...", "#######"],
    'E': ["#######", "#..#..#", "#..#..#"],
    'L': ["#######", "......#", "......#"],
    'O': [".#####.", "#.....#", ".#####."],
    'W': ["#######", ".....#.", "....#..", ".....#.", "#######"],
    'R': ["#######", "#..#.#.", "###..##"],
    'D': ["#######", "#.....#", ".#####."],
    '!': ["#####.#"],
    ' ': [".......", "......."],
}

def make_grid(text, width=53):
    cols = []
    for i, char in enumerate(text.upper()):
        char_cols = FONT.get(char, FONT[' '])
        cols.extend(char_cols)
        if i < len(text) - 1:
            cols.append(".......")
    
    if len(cols) < width:
        needed = width - len(cols)
        left_pad = needed // 2
        right_pad = needed - left_pad
        cols = ["......."] * left_pad + cols + ["......."] * right_pad
    elif len(cols) > width:
        print(f"Warning: Rendered message width ({len(cols)}) exceeds contribution graph width ({width}). Truncating.")
        cols = cols[:width]
        
    return cols

def print_preview(cols):
    print("\n--- Contribution Graph Preview ---")
    for r in range(7):
        row_str = ""
        for c in range(len(cols)):
            pixel = "█" if cols[c][r] == "#" else "."
            row_str += pixel
        print(row_str)
    print("----------------------------------\n")

def get_start_sunday(year):
    # Find the Sunday of the week containing Jan 1 of the given year
    jan1 = datetime.date(year, 1, 1)
    days_to_subtract = (jan1.weekday() + 1) % 7
    return jan1 - datetime.timedelta(days=days_to_subtract)

def run_git_command(args, env=None):
    try:
        subprocess.run(args, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(args)}")
        print(f"Error: {e.stderr.decode().strip()}")
        sys.exit(1)

def main():
    print("==================================================")
    print("   GitHub Contribution Graph Art Generator   ")
    print("==================================================")
    
    # Configuration
    default_text = "HELLO WORLD!"
    text = input(f"Enter the message to draw [Default: '{default_text}']: ").strip() or default_text
    
    default_year_choice = "rolling"
    year_str = input(f"Enter target year (e.g. 2024, or 'rolling' for the last 12 months) [Default: '{default_year_choice}']: ").strip().lower()
    
    if not year_str or year_str == "rolling":
        is_rolling = True
        year = None
    else:
        is_rolling = False
        try:
            year = int(year_str)
        except ValueError:
            print("Invalid year format. Defaulting to 'rolling'.")
            is_rolling = True
            year = None
    
    default_commits = 20
    commits_str = input(f"Enter commits per pixel (10-50 recommended) [Default: {default_commits}]: ").strip()
    commits_per_pixel = int(commits_str) if commits_str else default_commits
    
    # 1. Generate the grid
    cols = make_grid(text)
    print_preview(cols)
    
    # Calculate active pixels
    active_pixels = sum(col.count('#') for col in cols)
    total_commits = active_pixels * commits_per_pixel
    
    # 2. Date Calculation
    if is_rolling:
        today = datetime.date.today()
        # Find the Sunday of the current week
        days_to_subtract = (today.weekday() + 1) % 7
        current_sunday = today - datetime.timedelta(days=days_to_subtract)
        start_sunday = current_sunday - datetime.timedelta(weeks=52)
        print("Target Year: Last 12 months (Rolling)")
    else:
        start_sunday = get_start_sunday(year)
        print(f"Target Year: {year}")
        
    print(f"Start Sunday: {start_sunday}")
    print(f"Active pixels (days): {active_pixels}")
    print(f"Total commits to be made: {total_commits}")
    
    # Check if we are inside a git repo
    if not os.environ.get("DRY_RUN"):
        if not os.path.exists(".git"):
            print("\n[ERROR] Not in a Git repository. Please run this script inside a Git repository.")
            sys.exit(1)
            
        # Safety Check
        print("\n[WARNING] This script will create a large number of empty commits backdated to the target year.")
        print("It is HIGHLY recommended to run this in a brand new, empty repository to avoid cluttering your project history.")
        confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Aborted.")
            sys.exit(0)
            
        print("\nGenerating commits... Please wait.")
        
        env = os.environ.copy()
        count = 0
        
        for c in range(len(cols)):
            for r in range(7):
                if cols[c][r] == '#':
                    # Calculate the date for this column/row
                    commit_date = start_sunday + datetime.timedelta(days=c * 7 + r)
                    
                    for i in range(commits_per_pixel):
                        hour = 12
                        minute = i % 60
                        second = (i // 60) % 60
                        date_str = f"{commit_date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}:{second:02d} +0000"
                        
                        env["GIT_AUTHOR_DATE"] = date_str
                        env["GIT_COMMITTER_DATE"] = date_str
                        
                        # Create empty commit
                        msg = f"Contribution Art - Pixel ({c},{r}) - commit {i+1}/{commits_per_pixel}"
                        run_git_command(["git", "commit", "--allow-empty", "-m", msg], env=env)
                        count += 1
                        
                        # Print progress
                        if count % 50 == 0 or count == total_commits:
                            print(f"Progress: {count}/{total_commits} commits created...", end='\r')
                            
        print(f"\n\nSuccess! {count} commits created.")
        print("Now run:")
        print("  git push origin main")
        print("(Note: It can take 5-10 minutes for GitHub to update your contribution graph.)")
    else:
        print("\n[Dry Run] No commits created.")

if __name__ == "__main__":
    main()
