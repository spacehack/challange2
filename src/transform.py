from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt


def scale(pointpx: np.ndarray, corner_ur: np.ndarray, corner_ul: np.ndarray, corner_ll: np.ndarray, imagesize: np.ndarray):
    """
    Scale `pointpx` into the longitude/latitude coordinate space.

    Parameters
    ----------
    pointpx : np.ndarray
        X and Y value of the pixel to be scaled.
    corner_ur : np.ndarray
        The upper-right corner in (long, lat) space.
    corner_ul : np.ndarray
        The upper-left corner in (long, lat) space.
    corner_ll : np.ndarray
        The lower-right corner in (long, lat) space.
    imagesize : np.ndarray
        The X and Y size of the input-image in pixels.

    Returns
    -------
    point : np.ndarray
        The scaled point.
    """
    realsize = np.array([np.linalg.norm(corner_ur - corner_ul), np.linalg.norm(corner_ul - corner_ll)])
    scale = realsize / imagesize
    assert abs((scale[0] - scale[1]) / scale[1]) < 1.0, f"Scale is too different: x-scale={scale[0]} y-scale={scale[1]}"
    M_scale = np.array([[scale[0], 0], [0, scale[1]]])
    return M_scale @ pointpx


def calc_angle(v1, v2):
    return np.arccos((v1 @ v2 / (np.linalg.norm(v1) * np.linalg.norm(v2))))


def rotate(point: np.ndarray, corner_ur: np.ndarray, corner_ul: np.ndarray, corner_ll: np.ndarray) -> np.ndarray:
    """
    Rotate `point` to fit the rotation of the longitude/latitude coordinate-space.

    Parameters
    ----------
    point : np.ndarray
        X and Y value of the point.
    corner_ur : np.ndarray
        The upper-right corner in (long, lat) space.
    corner_ul : np.ndarray
        The upper-right corner in (long, lat) space.
    corner_ll : np.ndarray
        The lower-left corner in (long, lat) space.

    Returns
    -------
    point : np.ndarray
        The rotated point.
    """
    # find out what pair of corner to use to determine the roataion
    anglex = -calc_angle(corner_ul - corner_ur, np.array([-1, 0]))
    angley = -calc_angle(corner_ll - corner_ul, np.array([0, -1]))
    angles = np.array([anglex, angley])
    angle = angles[np.argmax(np.abs(angles))]
    M_rotation = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    return M_rotation @ point


def translate(point: np.ndarray, corner_ll: np.ndarray) -> np.ndarray:
    """
    Translate `point` to fit the 
    
    Parameters
    ----------
    point : np.ndarray
    corner_ll : np.ndarray

    Returns
    -------
    point : np.ndarray
        Translated point.
    """
    return point + corner_ll

def transform_old(pointpx, corner_ur, corner_ul, corner_ll, imagesize):
    x_deg_len = corner_ur[0] - corner_ul[0]
    y_deg_len = corner_ul[1] - corner_ll[1]
    deg_per_pix_xdir = x_deg_len / imagesize[0]
    deg_per_pix_ydir = y_deg_len / imagesize[1]

    x = pointpx[0]
    rec_ul_lon = (x * deg_per_pix_xdir) + corner_ul[0]
    lat = -1 * ((imagesize[1] - pointpx[1]) * deg_per_pix_ydir) + corner_ul[1]
    return np.array([rec_ul_lon, lat])

def transform(pointpx, corner_ur, corner_ul, corner_ll, imagesize):
    """
    Transform `pointpx` from pixel-coordinate-space into (long, lat)-coordinate-space.

    Parameters
    ----------
    pointpx : np.ndarray
        The image-point with x, y pixel coordinates.
    corner_ur : np.ndarray
        The upper-right corner in (long, lat) space.
    corner_ul : np.ndarray
        The upper-left corner in (long, lat) space.
    corner_ll : np.ndarray
        The lower-left corner in (long, lat) space.
    imagesize : np.ndarray
        The (x, y) size of the image in pixels.

    Returns
    -------
    point : np.ndarray
        The point in lat/long coordinate space.
    """
    if not 0 <= pointpx[0] <= imagesize[0]:
        print(f"[WARNING] point x coordinate (={pointpx[0]}) not in image-width (={imagesize[0]})")
    if not 0 <= pointpx[1] <= imagesize[1]:
        print(f"[WARNING] point y coordinate (={pointpx[1]}) not in image-height (={imagesize[1]})")

    point = scale(pointpx,
                  corner_ur=corner_ur,
                  corner_ul=corner_ul,
                  corner_ll=corner_ll,
                  imagesize=imagesize)
    point = rotate(point, corner_ur, corner_ul, corner_ll)
    point = translate(point, corner_ll)
    return point


def visualize():
    """ Visualize the transformation steps on example input. """
    # corner1 = np.array([26.49, 3.82])
    # corner2 = np.array([25.54, 3.83])
    # corner3 = np.array([25.54, 3.75])
    # corner4 = np.array([26.49, 3.74])
    # corners = np.column_stack((corner1, corner2, corner3, corner4))
    # imagesize = np.array([52224, 5064]) // 10
    from numpy import array
    a = eval("""(
        [array([ 1213.25018311, 50283.76699829]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 1069.20169067, 47749.85971069]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 5774.96826172, 44479.32678223]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 1445.67004395, 42035.75231934]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2532.        , 41902.60980225]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 5623.76196289, 39992.25012207]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([  910.7706604 , 33793.68363953]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2962.61135864, 30680.63146973]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2440.19158936, 26486.56188965]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 3830.57794189, 24590.31072235]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2597.1034317 , 23808.47906494]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 2532.        , 10459.66265869]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 4220.        , 10395.95028687]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([4807.8203125 , 7929.60699463]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([4726.63311768, 5713.96124268]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([ 844.        , 4983.78283691]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])],
        [array([3738.62582397, 2790.93508911]), array([  3.73, 116.53]), array([  3.64, 116.53]), array([  3.62, 115.59]), array([ 5064, 52224])])""")
    points = np.array([x[0] for x in a])
    corner_ur = [x[1] for x in a][0]
    corner_ul = [x[2] for x in a][0]
    corner_ll = [x[3] for x in a][0]
    imagesize = [x[4] for x in a][0]
    corners = np.column_stack((corner_ur, corner_ul, corner_ll))

    # --- plot corners --- #
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Corners")
    plt.xlabel("latitude")
    plt.ylabel("longitude")
    plt.show()

    nxs, nys = imagesize[0] + 1, imagesize[1] + 1
    xs, ys = np.mgrid[0:nxs:40 * 1j, 0:nys:40 * 1j]
    xs, ys = xs.flatten(), ys.flatten()
    v = np.random.random(xs.size) * 50

    # --- plot pixels --- #
    #plt.scatter(xs, ys, s=v)
    v = np.random.random(len(points)) * 50
    plt.scatter(points[:, 0], points[:, 1], s=v)
    plt.title("Pixels")
    plt.show()


    #points = np.column_stack((xs, ys))

    # --- Calc scaled points --- #
    points_scaled = np.array([scale(p,
                                    corner_ur=corner_ur,
                                    corner_ul=corner_ul,
                                    corner_ll=corner_ll,
                                    imagesize=imagesize) for p in points])
    plt.scatter(points_scaled[:, 0], points_scaled[:, 1], s=v)
    plt.xlim((0, 1.0))
    plt.ylim((0, 1.0))
    #plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Scaled")
    plt.xlabel("latitude")
    plt.ylabel("longitude")
    plt.show()

    # --- Calc rotation --- #
    points_rotated = np.array([rotate(p,
                                      corner_ur=corner_ur,
                                      corner_ul=corner_ul,
                                      corner_ll=corner_ll) for p in points_scaled])
    plt.scatter(points_rotated[:, 0], points_rotated[:, 1], s=v)
    plt.scatter(points_scaled[:, 0], points_scaled[:, 1], s=v, c='#FF0000AA')
    plt.xlim((0, 1.0))
    plt.ylim((0, 1.0))
    #plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Scaled and rotated")
    plt.xlabel("latitude")
    plt.ylabel("longitude")
    plt.show()

    # --- Calc Translation --- #
    points_translated = np.array([translate(p,
                                            corner_ll=corner_ll) for p in points_rotated])
    plt.scatter(points_translated[:, 0], points_translated[:, 1], s=v)
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.title("Complete transformation")
    plt.xlabel("latitude")
    plt.ylabel("longitude")
    plt.xlim((3.5, 3.5+1.3))
    plt.ylim((115.4, 116.7))
    plt.show()

    # --- Calc all together --- #
    points_transformed = np.array([transform(p, corner_ur, corner_ul, corner_ll, imagesize) for p in points])
    plt.scatter(corners[0], corners[1], s=np.linspace(30, 100, 4))
    plt.scatter(points_transformed[:, 0], points_transformed[:, 1], s=v)
    plt.xlim((3.5, 3.5 + 1.3))
    plt.ylim((115.4, 116.7))
    plt.title("Complete transformation -- all at once")
    plt.xlabel("latitude")
    plt.ylabel("longitude")
    plt.show()


class TestData(NamedTuple):
    corner1: np.ndarray
    corner2: np.ndarray
    corner3: np.ndarray
    corner4: np.ndarray
    imagesize: np.ndarray


def test_data_case_0():
    corner1 = np.array([26.49, 3.82])
    corner2 = np.array([25.54, 3.83])
    corner3 = np.array([25.54, 3.75])
    corner4 = np.array([26.49, 3.74])
    imagesize = np.array([52224, 5064]) // 10
    return TestData(corner1=corner1,
                    corner2=corner2,
                    corner3=corner3,
                    corner4=corner4,
                    imagesize=imagesize)


def test_data_case_1():
    """
    Product	M1282472090RE
    Pds dataset name	LRO-L-LROC-2-EDR-V1.0
    Pds volume name	LROLRC_0035
    Instrument host	LRO
    Instrument	LROC
    Original product	nacr001ddcd5
    Product version	v1.8
    Mission phase name	THIRD EXTENDED SCIENCE MISSION
    Rationale desc	TARGET OF OPPORTUNITY
    Data quality	0
    Nac preroll start time	(DOY:152) 2018-06-01T06:00:23
    Start time	(DOY:152) 2018-06-01T06:00:23
    Stop time	(DOY:152) 2018-06-01T06:00:52
    Spacecraft clock partition	1
    Nac spacecraft clock preroll count	549525622:64684
    Spacecraft clock start count	549525623:36862
    Spacecraft clock stop count	549525652:59738
    Target name	MOON
    Orbit number	40257
    Slew angle	0.00887697075602033
    Lro node crossing	A
    Lro flight direction	-X
    Nac line exposure duration	0.000559466666666667
    Nac frame	RIGHT
    Nac dac reset	190
    Nac channel a offset	12
    Nac channel b offset	74
    Instrument mode code	7
    Compand select code	3
    Mode compression	true
    Mode test	false
    Nac temperature scs	7.899
    Nac temperature fpa	19.374
    Nac temperature fpga	-8.109
    Nac temperature telescope	8.132
    Image lines	52224
    Line samples	5064
    Sample bits	8
    Scaled pixel width	0.84
    Scaled pixel height	0.88
    Resolution	0.856571977678108
    Emission angle	1.16
    Incidence angle	27.61
    Phase angle	26.45
    North azimuth	87.76
    Sub solar azimuth	179.78
    Sub solar latitude	-1.33
    Sub solar longitude	331.3
    Sub spacecraft latitude	0.14
    Sub spacecraft longitude	358.82
    Solar distance	152038784.5
    Solar longitude	306.07
    Center latitude	0.14
    Center longitude	358.87
    Upper right latitude	0.91
    Upper right longitude	358.9
    Lower right latitude	-0.61
    Lower right longitude	358.98
    Lower left latitude	-0.62
    Lower left longitude	358.84
    Upper left latitude	0.9
    Upper left longitude	358.76
    Spacecraft altitude	83.76
    Target center distance	1821.08
    """

    return TestData(corner1=np.array([0.91, 358.9]),
                    corner2=np.array([-0.61, 358.98]),
                    corner3=np.array([-0.62, 358.84]),
                    corner4=np.array([358.84, 358.76]),
                    imagesize=np.array([52224, 5064]))
