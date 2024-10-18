import os

# Function to get the GIT diff output using subprocess shell command    
def get_git_diff_output(directory):
    os.chdir(directory)
    return os.popen("git diff").read()

if __name__ == "__main__":
    print(get_git_diff_output("."))