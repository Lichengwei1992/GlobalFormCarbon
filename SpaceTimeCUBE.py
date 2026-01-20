import os
import rasterio
import xarray as xr
import numpy as np
import dask.array as da
import pandas as pd

from rasterio.windows import Window
from rasterio.enums import Resampling

folder = r"E:\Data\ODIAC\New folder"
years = [2000, 2005, 2010, 2015, 2020]
tif_files = [os.path.join(folder, f"{y}.tif") for y in years]

# 获取空间参考、坐标
with rasterio.open(tif_files[0]) as src:
    profile = src.profile
    transform = src.transform
    height, width = src.height, src.width
    x_coords = np.array([transform * (col, 0) for col in range(width)])[:, 0]
    y_coords = np.array([transform * (0, row) for row in range(height)])[:, 1]

# 延迟加载每张图为 Dask 数组
layers = []
for tif in tif_files:
    with rasterio.open(tif) as src:
        d = da.from_array(src.read(1), chunks=(1024, 1024))  # 分块读入
        layers.append(d)

# 拼接成三维 Dask 数组：time, y, x
data_cube = da.stack(layers, axis=0)

# 时间轴
time_coords = pd.to_datetime([f"{y}-01-01" for y in years])

# 构建 xarray 数据集
ds = xr.Dataset(
    data_vars={
        "SUM": (["time", "y", "x"], data_cube),
        "COUNT": (["time", "y", "x"], da.where(data_cube != 0, 1, 0).astype(np.int16)),
    },
    coords={
        "time": time_coords,
        "y": y_coords,
        "x": x_coords,
    },
    attrs={
        "title": "Global STC with Dask",
        "cube": "true",
        "summary": "Memory-efficient global raster cube",
        "spatial_reference": str(profile['crs']),
    }
)

# 写入 .nc（自动用 Dask 按块写入）
output_nc = os.path.join(folder, "arcgis_cube_dask.nc")
ds.to_netcdf(output_nc, engine='netcdf4', compute=True)

print("✅ 使用 Dask 构建完成，输出文件为：", output_nc)
