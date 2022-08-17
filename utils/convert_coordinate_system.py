import math


def tile2geographic(xtile, ytile, zoom):
    """
    タイル座標から地図座標 (緯度経度) に変換
    tile coordinate system -> geographic coordinate system
    https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python

    Args:
        xtile (int): x方向タイル座標
        ytile (int): y方向タイル座標
        zoom (int): ズームレベル

    Returns:
        tuple: タイルの左上の地図座標(経度, 緯度)

    Note:
        タイルの右下の地図座標を計算するためには
        xtile += 1
        ytile += 1

        タイルの中心の地図座標を計算するためには
        xtile += 0.5
        ytile += 0.5
    """
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lon_deg, lat_deg)


def geographic2tile(lon_deg, lat_deg, zoom):
    """
    地図座標 (緯度経度) からタイル座標に変換
    geographic coordinate system -> tile coordinate system
    https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python

    Args:
        lon_deg (float): 経度
        lat_deg (float): 緯度
        zoom (int): ズームレベル

    Returns:
        tuple: (x方向タイル座標, y方向タイル座標)
    """
    n = 2.0 ** zoom
    lat_rad = math.radians(lat_deg)
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def geographic2image(bbox, img_size, lon, lat):
    """
    地図座標 (緯度経度) を画像座標 (ピクセル) に変換
    geographic coordinate system -> image coordinate system

    Args:
        bbox (tuple): 対象画像の地図座標のバウンディングボックス
                      (左下の経度, 左下の緯度, 右上の経度, 右上の緯度)
        img_size (tuple): 対象画像サイズ (width, height)
        lon (float): 経度
        lat (float): 緯度

    Returns:
        tuple: 画像座標 (x, y)
    """
    pix_per_deg = (
        img_size[0] / (bbox[2] - bbox[0]),
        img_size[1] / (bbox[3] - bbox[1])
    )
    pixel = (
        int((lon - bbox[0]) * pix_per_deg[0]),
        int((bbox[3] - lat) * pix_per_deg[1])
    )
    return pixel
