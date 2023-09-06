import io

import cv2
import kornia.feature as KF
import numpy as np
import torch
from PIL import Image
from kornia_moons.feature import *


def to_Image(uploaded_file):
    image = Image.open(io.BytesIO(uploaded_file)).convert('RGB')
    return image


def load_Image(path: str):
    return Image.open(path).convert('RGB')


def sift_matching(fname1, fname2):
    img1 = cv2.cvtColor(cv2.imread(fname1), cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(cv2.imread(fname2), cv2.COLOR_BGR2RGB)

    # OpenCV SIFT
    sift = cv2.SIFT_create(8000)
    kps1, descs1 = sift.detectAndCompute(img1, None)
    kps2, descs2 = sift.detectAndCompute(img2, None)

    # Converting to kornia for matching via AdaLAM
    lafs1 = laf_from_opencv_SIFT_kpts(kps1)
    lafs2 = laf_from_opencv_SIFT_kpts(kps2)
    dists, idxs = KF.match_adalam(
        torch.from_numpy(descs1), torch.from_numpy(descs2), lafs1, lafs2, hw1=img1.shape[:2], hw2=img2.shape[:2]
    )

    # Converting back to kornia via to use OpenCV MAGSAC++
    tentatives = cv2_matches_from_kornia(dists, idxs)
    src_pts = np.float32([kps1[m.queryIdx].pt for m in tentatives]).reshape(-1, 2)
    dst_pts = np.float32([kps2[m.trainIdx].pt for m in tentatives]).reshape(-1, 2)

    F, inliers_mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.USAC_MAGSAC, 0.25, 0.999, 100000)

    # Drawing matches using kornia_moons
    draw_LAF_matches(
        lafs1,
        lafs2,
        idxs,
        img1,
        img2,
        inliers_mask,
        draw_dict={"inlier_color": (0.2, 1, 0.2), "tentative_color": None, "feature_color": None, "vertical": False},
    )
    print(f"{inliers_mask.sum()} inliers found")
    return


def to_dict(data):
    if len(data) == 0:
        return {"empty": "0"}
    bbox = data[0]
    dict_schema = {
        "x1": float(bbox[0]),
        "y1": float(bbox[1]),
        "x2": float(bbox[2]),
        "y2": float(bbox[3])
    }
    return dict_schema
