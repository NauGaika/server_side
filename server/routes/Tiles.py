# -*- coding: utf-8 -*-
from flask import Blueprint, request
import json
import cv2
import math
import time
import numpy as np
import itertools as IT
import os
import requests
import random

tiles_api = Blueprint('tiles_api', __name__)

@tiles_api.route('/api/tiles/', methods=['GET','POST'])
def tiles_test():
    """Возвращает все пункты меню 'name', 'title'"""
    user_files = json.loads(request.form['json'])
    cur_img = user_files['curImg']
    part = user_files['part']
    # print(user_files)
    UPLOAD_FOLDER = "/home/naugaika/Yandex.Disk/Мир стекла и зеркала/sitenuxt/sevsteklo/static/img/tiles/"
    img = requests.get(user_files['src'])
    with open(os.path.join(UPLOAD_FOLDER, 'tile.png'), 'wb') as f:
        f.write(img.content)
    bg = cv2.imread(UPLOAD_FOLDER + cur_img, 1)
    masks = {
        'wl': cv2.imread(UPLOAD_FOLDER + 'wallleft.png', 1),
        'wr': cv2.imread(UPLOAD_FOLDER + 'wallright.png', 1),
        'ws': cv2.imread(UPLOAD_FOLDER + 'wallstraight.png', 1),
        'f': cv2.imread(UPLOAD_FOLDER + 'floor.png', 1),
    }
    shadow = cv2.imread(UPLOAD_FOLDER + 'shadow.png', 1)
    light = cv2.imread(UPLOAD_FOLDER + 'light.png', 1)
    tile_dimensions = (int(user_files['width']), int(user_files['height']))
    # tile_dimensions_2 = (700, 460)
    # tile_dimensions_3 = (900, 900)
    # tile_dimensions_4 = (1500, 600)
    # tile_dimensions_5 = (700, 700)
    tile = cv2.imread(UPLOAD_FOLDER + 'tile.png', 1)
    # tile_2 = cv2.imread('2.jpg', 1)
    # tile_3 = cv2.imread('3.jpg', 1)
    # tile_4 = cv2.imread('4.jpg', 1)
    # tile_5 = cv2.imread('5.jpg', 1)
    #
    def overlay_transparent(background, overlay, x, y):

        background_width = background.shape[1]
        background_height = background.shape[0]

        if x >= background_width or y >= background_height:
            return background

        h, w = overlay.shape[0], overlay.shape[1]

        if x + w > background_width:
            w = background_width - x
            overlay = overlay[:, :w]

        if y + h > background_height:
            h = background_height - y
            overlay = overlay[:h]

        if overlay.shape[2] < 4:
            overlay = np.concatenate(
                [
                    overlay,
                    np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
                ],
                axis = 2,
            )

        overlay_image = overlay[..., :3]
        mask = overlay[..., 3:] / 255.0

        background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

        return background

    def to_rgba(img):
        b_channel, g_channel, r_channel = cv2.split(img)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        img = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        return img

    def get_max_el(pts):
        max_p = np.max(pts, 0)
        min_p = np.min(pts, 0)
        # min_p = pts[:, pts].min()
        leng = max_p - min_p

        return leng.astype(np.int)

    def create_img_by_length(width, height, tile, tile_dimensions, pts):
        """Создает сразу набор плиток на стену."""
        dim_elem = get_max_el(pts)
        count_of_width = width / tile_dimensions[0]
        count_of_height = height / tile_dimensions[1]
        koef_width = dim_elem[0] / count_of_width / tile_dimensions[0]
        koef_height = dim_elem[1] / count_of_height / tile_dimensions[1]
        if koef_width > koef_height:
            tile_width = tile_dimensions[0] * koef_width
            tile_height = tile_dimensions[1] * koef_width
        else:
            tile_width = tile_dimensions[0] * koef_height
            tile_height = tile_dimensions[1] * koef_height
        tile_width = int(tile_width)
        tile_height = int(tile_height)
        tile = cv2.resize(
            tile,
            (tile_width, tile_height),
            interpolation=cv2.INTER_NEAREST)
        img_width = int(count_of_width * tile_width)
        img_height = int(count_of_height * tile_height)
        canvas = np.zeros((img_height, img_width, 3), np.uint8)
        for numer_column in range(math.ceil(count_of_height)):
            for number_line in range(math.ceil(count_of_width)):
                input_height_start = tile_height * numer_column
                input_width_start = tile_width * number_line
                input_height_finish = input_height_start + tile_height
                input_width_finish = input_width_start + tile_width
                _tile_height = tile_height
                _tile_width = tile_width
                if input_width_finish > img_width:
                    _tile_width = tile_width - (input_width_finish - img_width)
                    input_width_finish = img_width
                if input_height_finish > img_height:
                    _tile_height = _tile_height - input_height_finish + img_height
                    input_height_finish = input_height_start + _tile_height
                canvas_region = canvas[input_height_start: input_height_finish, input_width_start: input_width_finish]
                tile_region = tile[0: _tile_height, 0: _tile_width]
                canvas[input_height_start: input_height_finish,
                       input_width_start: input_width_finish] = tile[
                        0: _tile_height, 0: _tile_width]
        canvas = to_rgba(canvas)
        return canvas

    def deform_img_to_point(img, pts2, bg, target):
        """Преобразует данное изображение к точкам"""
        max_width = max(img.shape[0], bg[0])
        max_height = max(img.shape[1], bg[1])
        # new_arr = np.zeros((max_width, max_height, 4), np.uint8)

        pts1 = np.float32([
            [0, 0],
            [img.shape[1], 0],
            [img.shape[1], img.shape[0]],
            [0, img.shape[0]]
        ])
        if target:
            img = cv2.circle(img, tuple(pts1[0]), 3, (0,0,255), -1)
            img = cv2.circle(img, tuple(pts1[1]), 3, (0,0,255), -1)
            img = cv2.circle(img, tuple(pts1[2]), 3, (0,0,255), -1)
            img = cv2.circle(img, tuple(pts1[3]), 3, (0,0,255), -1)
            cv2.imshow('1.jpg', img)
        # new_arr[: img.shape[0], : img.shape[1]] = img
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        res = cv2.warpPerspective(img, matrix, (max_height, max_width))
        if target:
            cv2.imshow('5.jpg', res)
        # cv2.imshow('1.jpg', new_arr)
        return res

    def add_mask(img, mask):
        img = img[0:mask.shape[0], 0:mask.shape[1]]
        img = img.astype(np.float) / 255
        mask = mask.astype(np.float) / 255
        img_r, img_g, img_b, img_a = cv2.split(img)
        mask_r, mask_g, mask_b = cv2.split(mask)
        new_img_a = (mask_r + mask_g + mask_b) / 3
        new_img_a = np.minimum(img_a, new_img_a)
        img = cv2.merge((img_r * 255, img_g * 255, img_b * 255, new_img_a * 255))
        return img

    def add_light(img, light, intens=1):
        n_s = light.astype(np.float32) / 255
        n_i = img.astype(np.float32) / 255
        n_i = n_i[0:n_s.shape[0], 0:n_s.shape[1]]
        r_s, g_s, b_s = cv2.split(n_s)
        r_i, g_i, b_i, b_a = cv2.split(n_i)
        n_b_i = 1 - (1 - b_s * intens) * (1 - b_i)
        n_g_i = 1 - (1 - g_s * intens) * (1 - g_i)
        n_r_i = 1 - (1 - r_s * intens) * (1 - r_i)
        n_a_i = b_a
        img = cv2.merge((n_r_i * 255, n_g_i * 255, n_b_i * 255, n_a_i * 255))
        return img

    def add_shadow(img, shadow):
        n_s = shadow.astype(np.float32) / 255
        n_i = img.astype(np.float32) / 255
        n_i = n_i[0:n_s.shape[0], 0:n_s.shape[1]]
        r_s, g_s, b_s = cv2.split(n_s)
        r_i, g_i, b_i, b_a = cv2.split(n_i)
        n_b_i = b_s * b_i
        n_g_i = g_s * g_i
        n_r_i = r_s * r_i
        n_a_i = b_a
        img = cv2.merge((n_r_i * 255, n_g_i * 255, n_b_i * 255, n_a_i * 255))
        return img

    def make_img(bg, tile, tile_dimensions, width, height, pts, mask, shadow, light, intens, target=False):
        pts2 = pts
        img = create_img_by_length(width, height, tile, tile_dimensions, pts)
        # cv2.imshow('1.jpg', img)
        img = deform_img_to_point(img, pts2, bg.shape, target)
        if not target:
            img = add_shadow(img, shadow)
            img = add_mask(img, mask)
            img = add_light(img, light, intens=intens)
        img = overlay_transparent(bg, img, 0, 0)
        if target:
            img = cv2.circle(img, tuple(pts[0]), 3, (0,0,255), -1)
            img = cv2.circle(img, tuple(pts[1]), 3, (0,0,255), -1)
            img = cv2.circle(img, tuple(pts[2]), 3, (0,0,255), -1)
            img = cv2.circle(img, tuple(pts[3]), 3, (0,0,255), -1)
        return img
    #
    # # start_time = time.clock()
    if part == "f":
        pts = np.float32([[114, 400], [686, 404], [996, 610], [-191, 610]])
        img = make_img(bg, tile, tile_dimensions, 3700, 4000, pts, masks['f'], shadow, light, 1)
    if part == "ws":
        pts = np.float32([[110, 19], [700, 19], [700, 388], [110, 391]])
        img = make_img(bg, tile, tile_dimensions, 4500, 2700, pts, masks['ws'], shadow, light, 0.5)
    # #
    if part == "wl":
        pts = np.float32([[-182, -120], [110, 19], [110, 388], [-182, 580]])
        img = make_img(bg, tile, tile_dimensions, 3700, 2700, pts, masks['wl'], shadow, light, 1)
    # #
    if part == "wr":
        pts = np.float32([[689, 18], [800, -48], [800, 463], [689, 389]])
        img = make_img(bg, tile, tile_dimensions, 3700, 2700, pts, masks['wr'], shadow, light, 1)
    # # cv2.imshow('test.png', img)
    cv2.imwrite(UPLOAD_FOLDER + 'test.png', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return 'test.png?' + str(random.randint(0,1000000))
