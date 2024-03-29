[![License][s1]][co] [![License][s2]][li]

[s1]: https://app.codacy.com/project/badge/Grade/b4b3f99be7f44698a6081b4a84e65afc
[s2]: https://img.shields.io/badge/licence-GPL%203.0-blue.svg

[co]: https://app.codacy.com/gh/matt77hias/pippy/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade
[li]: https://raw.githubusercontent.com/matt77hias/pippy/master/LICENSE.txt

# pippy

## About
A small *point-inside-polygon* (pip) library supporting *crossing* and *winding number* pip tests.

## Use
<p align="center">
<img src="res/samples=128.png" width="203">
<img src="res/samples=256.png" width="203">
<img src="res/samples=512.png" width="203">
<img src="res/samples=1024.png" width="203">
</p>
<p align="center">
<img src="res/samples=2048.png" width="203">
<img src="res/samples=4096.png" width="203">
<img src="res/samples=8192.png" width="203">
<img src="res/samples=16384.png" width="203">
</p>

### Monte-Carlo (*hit-or-miss*) convergence behaviour
#### Crossing number pip test
<p align="center">
<img src="res/RMSE_f_cn_experiments=16.png" width="410">
<img src="res/RMSE_f_cn.png" width="410">
</p>
<p align="center">16 versus 1028 experiments</p>

#### Winding number pip test
<p align="center">
<img src="res/RMSE_f_wn_experiments=16.png" width="410">
<img src="res/RMSE_f_wn.png" width="410">
</p>
<p align="center">16 versus 1028 experiments</p>

#### `matplotlib.path.Path.contains_point` pip test
<p align="center">
<img src="res/RMSE_f_path_experiments=16.png" width="410">
<img src="res/RMSE_f_path.png" width="410">
</p>
<p align="center">16 versus 1028 experiments</p>

```python
# Code
test.test()
```
