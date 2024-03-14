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

The tool will first prompt you for your Tower Coverage username and password. Once you have provided that information,
the tool will download a list of all multi-maps associated with your account.

You will then be prompted to select a
multimap to export. Once you have selected a multimap, the tool will download the multimap and extract the coverage
models to the `./export` directory, which will be automatically created if it does not exist.

If you do not wish to enter your credentials every time you run the tool, you can modify the `run.py` file to set the
following variables:

```python
tc_username: str = ''
tc_password: str = ''
```

## Donate

Like my work?

<a href="https://www.buymeacoffee.com/AzorianMatt" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

**Want to sponsor me?** Please visit my organization's [sponsorship page](https://github.com/sponsors/AzorianSolutions).
