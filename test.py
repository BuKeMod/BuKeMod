import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from shapely.geometry import Point
from pyproj import Proj, transform



import rasterio

# ระบุ path ของ GeoTIFF ต้นฉบับ
original_image_path = './img/Task-of-2023-12-19T112104744Z-orthophoto.tif'

# เปิด GeoTIFF ด้วย rasterio
with rasterio.open(original_image_path, 'r') as src:
    # ดึงข้อมูล CRS ออกมา
    source_crs = src.crs.to_string()

# ตอนนี้ source_crs จะเป็นสตริงที่ระบุ CRS ของ GeoTIFF ต้นฉบับ
print(f"Coordinate Reference System of the original image: {source_crs}")

###########





# กำหนดพิกัดตั้งต้น (CRS) ของ GeoTIFF ที่มีอยู
# source_crs = 'EPSG:รหัสของระบบพิกัดที่ใช้ใน GeoTIFF ปัจจุบัน'

# กำหนดพิกัดที่ต้องการเปลี่ยนไป (WGS 84, EPSG:4326)
target_crs = 'EPSG:4326'

# ระบุพิกัดลองจิจูด (longitude) และละติจูด (latitude) ที่ต้องการ
lon, lat = 11154797.404812675, 1889592.4682372971

# สร้าง Point geometry จากพิกัดที่ต้องการ
point = Point(lon, lat)

# ใช้ pyproj เพื่อเปลี่ยนระบบพิกัดของ Point จาก WGS 84 เป็น CRS ของ GeoTIFF ปัจจุบัน
source_proj = Proj(init=source_crs)
target_proj = Proj(init=target_crs)
lon, lat = transform(target_proj, source_proj, lon, lat)

# เปลี่ยนระบบพิกัดของ Point และระบุ coordinates ใหม่
point = Point(lon, lat)
geom = {'type': 'Point', 'coordinates': (point.x, point.y)}

# เปิด GeoTIFF ด้วย rasterio
with rasterio.open('1.tif', 'r') as src:

    # หาพิกัดที่ต้องการเปลี่ยนไปในรูปแบบของ GeoTIFF
    lon, lat = point.x, point.y
    x, y = transform(source_proj, src.crs, lon, lat)

    # คำนวณพิกัดและขนาดใหม่หลังจากการเปลี่ยนระบบพิกัด
    transform, width, height = calculate_default_transform(
        src.crs, target_crs, src.width, src.height, *src.bounds)
    print(f"Transform: {transform}")
    # สร้าง GeoTIFF ใหม่ที่มีระบบพิกัดที่เปลี่ยนแล้ว
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': target_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    # สร้างไฟล์ GeoTIFF ใหม่
    with rasterio.open('1.tif', 'w', **kwargs) as dst:
        # เปลี่ยนระบบพิกัดของ GeoTIFF
        reproject(
            source=rasterio.band(src, 1),
            destination=rasterio.band(dst, 1),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=target_crs,
            resampling=Resampling.nearest
        )

# ตอนนี้ไฟล์ GeoTIFF ใหม่ถูกสร้างขึ้นแล้วในระบบพิกัด EPSG:4326
