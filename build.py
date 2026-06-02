import subprocess
import sys
from pathlib import Path

def run_cmd(args, cwd=None):
    print(f"Running: {' '.join(args)}")
    res = subprocess.run(args, cwd=cwd, shell=True)
    if res.returncode != 0:
        print(f"Command failed with exit code: {res.returncode}")
        sys.exit(res.returncode)

def main():
    root = Path(__file__).resolve().parent
    
    # 1. Sync dependencies
    print("--- Syncing dependencies ---")
    run_cmd(["uv", "sync"], cwd=root)
    
    # 2. Test static compilation
    print("--- Testing static wiki compilation ---")
    run_cmd(["uv", "run", "kb-wiki", "build"], cwd=root)
    
    # 3. Build distribution package
    print("--- Building distribution package ---")
    run_cmd(["uv", "build"], cwd=root)
    
    print("--- Build completed successfully! ---")

if __name__ == "__main__":
    main()
