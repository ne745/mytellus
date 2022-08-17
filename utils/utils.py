import numpy as np
from skimage.draw import polygon

from convert_coordinate_system import tile2geographic, geographic2image


def calc_tile_bbox(tile, tile_size):
    """
    タイル座標からバウンディングボックスを計算
    https://tools.ietf.org/html/rfc7946#section-5

    Args:
        tile (dict): タイル座標
        tile_size (dict): タイル座標のサイズ

    Returns:
        tuple: 地図座標のバウンディングボックス
               (左下の経度, 左下の緯度, 右上の経度, 右上の緯度)
    """
    right, top = tile2geographic(
        tile['x'] + tile_size['x'], tile['y'], tile['z'])
    left, bottom = tile2geographic(
        tile['x'], tile['y'] + tile_size['y'], tile['z'])
    return (left, bottom, right, top)


def generate_mask_from_polygon(points, bbox, img_size):
    """
    ポリゴンから画像を生成

    Args:
        points (list): [経度, 緯度] のリスト
        bbox (tuple): 対象画像の四隅の地図座標
                      (左下の経度, 左下の緯度, 右上の経度, 右上の緯度)
        img_size (dict): 対象画像サイズ

    Return:
        numpy.ndarray: ポリゴンの内部を 1 としたマスク画像
    """
    pixels = []
    size = (img_size['width'], img_size['height'])
    for p in points:
        pixels.append(geographic2image(bbox, size, p[0], p[1]))
    pixels = np.array(pixels)
    size = (img_size['height'], img_size['width'])
    poly_img = np.zeros(size, dtype=np.uint8)
    rr, cc = polygon(pixels[:, 1], pixels[:, 0], poly_img.shape)
    poly_img[rr, cc] = 1
    return poly_img


def generate_mask_image(features, bbox, img_size):
    """
    GeoJSON で指定された領域をマスクする画像を生成

    Args:
        features (list): GeoJSON 形式の座標データ
                         ['geometry']['coordinates'][0][:] に [経度, 緯度] が格納
        bbox (tuple): 対象画像の四隅の地図座標
                      (左下の経度, 左下の緯度, 右上の経度, 右上の緯度)
        img_size (dict): 対象画像サイズ

    Returns:
        np.ndarray: マスク画像
    """
    # features には複数の GeoJSON データが格納されているため
    # 一つずつ取り出してマスク画像を生成
    masks = []
    for feature in features:
        points = feature['geometry']['coordinates'][0]
        masks.append(generate_mask_from_polygon(points, bbox, img_size))

    # マスクを重ね合わせる
    mask = np.zeros_like(masks[0])
    for i, m in enumerate(masks):
        mask = mask + np.where((m > 0), 1, 0)
#     return np.where((mask > 0), 0, 1).astype(np.uint8)
    return mask


def filter_mask(src_image, mask_image):
    """
    マスク処理

    Args:
        src_image: ソース画像
        mask_image: マスク画像

    Returns:
        np.ndarray: マスク処理された画像
    """
    # (h, w) -> (h, w, c)
    mask_image = np.repeat(mask_image[:, :, None], src_image.shape[-1], axis=2)
    return src_image * mask_image
