import os
import subprocess
import venv


def install(folder):
    return subprocess.run([python_executable, '-m', 'pip', 'install', '-r',
                           os.path.join(os.path.curdir, folder, 'requirements.txt')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


path = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
venv_path = os.path.join(path, 'venv')

os.chdir(path)

print('Creating/Checking Virtual Environment...')
env = venv.EnvBuilder(with_pip=True)
env.create(venv_path)
python_executable = env.ensure_directories(venv_path).env_exe


print('Installing/Checking requirements...')
install('api')
install('fetcher')

print('Running tests...')
os.system(f'{python_executable} -m pytest')
