# Linear code weight estimation by random bit stream compression

Source to reproduce the work in our [arxiv paper](https://arxiv.org/abs/1806.02099).

## Usage

`python3 BCH_generate.py` will save output from random sampling to `/data`.
`python3 BCH_plot_vs_known.py` compares the estimated and known weight distribution directly.
`python3 BCH_plot_TVD.py` measures the total variation distance between the estimates and known distribution.


## Requirements

```bash
sudo apt install sagemath python3-seaborn
```
