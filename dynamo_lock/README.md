

### Create the virtual environment

```bash
conda create -n "test_ldl_env" python=3.10 ipython
```

To activate this environment, use

```bash
conda activate test_ldl_env
```

optional, ensure your python path is correct 

```bash
$ export PATH="/Users/David/opt/anaconda3/envs/test_ldl_env/bin:$PATH"
```

### Install requirements locally

```bash
rm -rf libs
mkdir -p libs/python/lib/python3.10/site-packages
pip3 install -r requirements.txt --target libs/python/lib/python3.10/site-packages
```