# Tower Coverage Exporter

This project provides a CLI tool that extracts coverage models from Tower Coverage multi-maps in ESRI Shapefile format.

## TL;DR - Linux

To get started quickly with a simple deployment, execute the following `bash` / `shell` commands on a Debian Linux
based system with `git` and `Python 3.8+` installed.

```
git clone https://github.com/AzorianSolutions/tower-coverage-exporter.git
cd tower-coverage-exporter
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Once you have finished this step, you are now ready to run the tool. To do this, you should run the following command:

```
./run.py
```

Temporary and exported files will be created in the `./export` directory, which will be automatically created if it
does not exist.
