# pippy

## About
A small *point-inside-polygon* (pip) library supporting *crossing* and *winding number* pip tests.

## Use
<p align="center"><img src="https://github.com/matt77hias/pippy/blob/master/res/samples=256.png" width="172"><img src="https://github.com/matt77hias/pippy/blob/master/res/samples=512.png" width="172"><img src="https://github.com/matt77hias/pippy/blob/master/res/samples=1024.png" width="172"><img src="https://github.com/matt77hias/pippy/blob/master/res/samples=2048.png" width="172"><img src="https://github.com/matt77hias/pippy/blob/master/res/samples=4096.png" width="172"></p>

### Monte-Carlo (*hit-or-miss*) convergence behaviour
#### Crossing number pip test
<p align="center"><img src="https://github.com/matt77hias/pippy/blob/master/res/MSE_f_cn.png" width="430"><img src="https://github.com/matt77hias/pippy/blob/master/res/RMSE_f_cn.png" width="430"></p>

#### Winding number pip test
<p align="center"><img src="https://github.com/matt77hias/pippy/blob/master/res/MSE_f_wn.png" width="430"><img src="https://github.com/matt77hias/pippy/blob/master/res/RMSE_f_wn.png" width="430"></p>

#### `matplotlib.path.Path.contains_point` pip test
<p align="center"><img src="https://github.com/matt77hias/pippy/blob/master/res/MSE_f_path.png" width="430"><img src="https://github.com/matt77hias/pippy/blob/master/res/RMSE_f_path.png" width="430"></p>

```python
# Code
test.test()
```
