"""画像処理系のモジュール"""
import cv2
import numpy as np


# 顔検出モデル
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def _byte2img(image_byte: bytes) -> np.ndarray:
    """画像のバイナリデータをcv2で扱える形にする

    Parameters
    ----------
    image_byte : bytes
        画像のバイナリデータ

    Returns
    -------
    np.ndarray
        cv2で利用可能なデータ型
    """
    return cv2.imdecode(np.frombuffer(image_byte, dtype="uint8"), cv2.IMREAD_UNCHANGED)


def _mosaic(img: np.ndarray, ratio: int | float = 0.1) -> np.ndarray:
    """モザイク処理

    Notes
    -----
        <https://note.nkmk.me/python-opencv-mosaic/>から利用

    Parameters
    ----------
    img : np.ndarray
        _byte2imgの出力
    ratio : float, optional
        縮小率, by default 0.1

    Returns
    -------
    np.ndarray
        モザイクの適用後画像
    """
    small = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, img.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)


def _mosaic_area(
    img: np.ndarray, x: np.integer, y: np.integer, width: np.integer, height: np.integer, ratio: int | float = 0.1
):
    """モザイクを指定の範囲に適用

    Parameters
    ----------
    img : np.ndarray
        _byte2imgの出力
    x : np.integer
        顔の検出基準位置（x座標）
    y : np.integer
        顔の検出基準位置（y座標）
    width : np.integer
        幅
    height : np.integer
        高さ
    ratio : int | float, optional
        縮小率, by default 0.1

    Returns
    -------
    Any
        モザイクの適用後画像
    """

    dst = img.copy()
    dst[y : y + height, x : x + width] = _mosaic(dst[y : y + height, x : x + width], ratio)
    return dst


def face_mosaic(image_byte: bytes) -> bytes:
    """画像（バイナリデータ）の顔にモザイクをかけた結果を取得

    Parameters
    ----------
    image_byte : bytes
        画像のバイナリデータ

    Returns
    -------
    bytes
        モザイク適用後のバイナリデータ
    """
    img = _byte2img(image_byte)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray)

    for x, y, w, h in faces:
        dst_face = _mosaic_area(img, x, y, w, h)
    _, img_png = cv2.imencode(".png", dst_face)
    return img_png.tobytes()
