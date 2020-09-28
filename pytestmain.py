"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""
import os
import subprocess
import webbrowser


def main():
    subprocess.run(['coverage', 'erase'])
    subprocess.run(['coverage', 'run', f'--omit=*/site-packages/*', '-m', 'pytest'])
    subprocess.run(['coverage', 'html'])
    webbrowser.open("file://" + os.getcwd() + "/htmlcov/index.html", new=2)

if __name__ == '__main__':
    main()