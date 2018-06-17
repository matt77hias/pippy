[![License][s1]][li]

[s1]: https://img.shields.io/badge/licence-GPL%203.0-blue.svg
[li]: https://raw.githubusercontent.com/matt77hias/pippy/master/LICENSE.txt

# pippy

## About
A small *point-inside-polygon* (pip) library supporting *crossing* and *winding number* pip tests.

## Use
<p align="center">
<img src="res/samples=128.png" width="214">
<img src="res/samples=256.png" width="214">
<img src="res/samples=512.png" width="214">
<img src="res/samples=1024.png" width="214">
</p>
<p align="center">
<img src="res/samples=2048.png" width="214">
<img src="res/samples=4096.png" width="214">
<img src="res/samples=8192.png" width="214">
<img src="res/samples=16384.png" width="214">
</p>

### Monte-Carlo (*hit-or-miss*) convergence behaviour
#### Crossing number pip test
<p align="center">
<img src="res/RMSE_f_cn_experiments=16.png" width="430">
<img src="res/RMSE_f_cn.png" width="430">
</p>
<p align="center">16 versus 1028 experiments</p>

#### Winding number pip test
<p align="center">
<img src="res/RMSE_f_wn_experiments=16.png" width="430">
<img src="res/RMSE_f_wn.png" width="430">
</p>
<p align="center">16 versus 1028 experiments</p>

#### `matplotlib.path.Path.contains_point` pip test
<p align="center">
<img src="res/RMSE_f_path_experiments=16.png" width="430">
<img src="res/RMSE_f_path.png" width="430">
</p>
<p align="center">16 versus 1028 experiments</p>

```python
# Code
test.test()
```
