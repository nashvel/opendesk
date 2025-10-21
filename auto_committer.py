#!/usr/bin/env python3
"""
Auto-Committer Script
Modifies itself 100 times and commits each change to GitHub.
Runs automatically at 6 AM daily.
"""

import os
import sys
import time
import random
import subprocess
from datetime import datetime
import schedule

class AutoCommitter:
    def __init__(self):
        self.script_path = os.path.abspath(__file__)
        self.target_file = os.path.join(os.path.dirname(self.script_path), 'changes.txt')
        self.commit_count = 0
        self.max_commits = 10
        
    def modify_target_file(self):
        """Modify the changes.txt file by adding a timestamp line"""
        try:
            # Read existing content
            if os.path.exists(self.target_file):
                with open(self.target_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
            else:
                content = "change me 100 times."
            
            # Add a timestamp line
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            random_num = random.randint(1000, 9999)
            new_line = f"Change #{self.commit_count + 1}: {timestamp} - Random: {random_num}"
            
            # Append the new line
            modified_content = content + "\n" + new_line
            
            with open(self.target_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
                
            print(f"Modified changes.txt (change #{self.commit_count + 1})")
            return True
            
        except Exception as e:
            print(f"Error modifying changes.txt: {e}")
            return False
    
    def git_commit_only(self):
        """Commit changes locally (no push)"""
        try:
            # Get current directory
            repo_dir = os.path.dirname(self.script_path)
            
            # Add changes
            subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True)
            
            # Commit with message
            commit_msg = f"Auto-commit #{self.commit_count + 1} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=repo_dir, check=True)
            
            print(f"Committed change #{self.commit_count + 1}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Git commit error: {e}")
            return False
        except Exception as e:
            print(f"Error in git commit: {e}")
            return False
    
    def git_push_all(self):
        """Push all commits to GitHub"""
        try:
            # Get current directory
            repo_dir = os.path.dirname(self.script_path)
            
            # Push to GitHub
            subprocess.run(['git', 'push'], cwd=repo_dir, check=True)
            
            print(f"Successfully pushed all commits to GitHub!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Git push error: {e}")
            return False
        except Exception as e:
            print(f"Error in git push: {e}")
            return False
    
    def run_commit_cycle(self):
        """Run the complete cycle of 100 modifications and commits"""
        print(f"Starting auto-commit cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Working on: {self.target_file}")
        print(f"Note: Will commit locally after each change, then push all at the end for speed!")
        
        success_count = 0
        
        for i in range(self.max_commits):
            self.commit_count = i
            
            print(f"\n--- Processing change {i + 1}/{self.max_commits} ---")
            
            # Modify the target file
            if self.modify_target_file():
                # Commit locally (no push yet)
                if self.git_commit_only():
                    success_count += 1
                    print(f"Successfully completed change {i + 1}")
                else:
                    print(f"Failed to commit change {i + 1}")
            else:
                print(f"Failed to modify changes.txt for change {i + 1}")
        
        print(f"All changes completed! Successfully processed {success_count}/{self.max_commits} changes")
        
        # Now push all commits at once
        if success_count > 0:
            print(f"Pushing all {success_count} commits to GitHub...")
            if self.git_push_all():
                print(f"All commits successfully pushed to GitHub!")
            else:
                print(f"Failed to push commits to GitHub")
        
        print(f"Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def setup_scheduler(self):
        """Set up the scheduler to run at 6 AM daily"""
        schedule.every().day.at("06:00").do(self.run_commit_cycle)
        
        print("Scheduler set up to run at 6:00 AM daily")
        print("Waiting for next scheduled run...")
        print("Press Ctrl+C to stop the scheduler")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")

def main():
    """Main function"""
    committer = AutoCommitter()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--run-now":
            # Run immediately for testing
            committer.run_commit_cycle()
        elif sys.argv[1] == "--schedule":
            # Run with scheduler
            committer.setup_scheduler()
        else:
            print("Usage:")
            print("  python auto_committer.py --run-now    # Run immediately")
            print("  python auto_committer.py --schedule   # Run with daily scheduler")
    else:
        print("Auto-Committer Script")
        print("This script modifies changes.txt 25 times and commits each change to GitHub.")
        print("\nUsage:")
        print("  python auto_committer.py --run-now    # Run immediately")
        print("  python auto_committer.py --schedule   # Run with daily scheduler at 6 AM")

if __name__ == "__main__":
    main()
