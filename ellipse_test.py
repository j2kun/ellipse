import math
from assertpy import assert_that
from ellipse import *


EPSILON = 1e-8


def test_unrotated_ellipse_contains_point():
    ellipse = Ellipse(
        center_x=1, center_y=1, radius_x=2, radius_y=3
    )

    # some points on the x axis
    assert_that(ellipse.contains(1, 1)).is_true()
    assert_that(ellipse.contains(1, 2)).is_true()
    assert_that(ellipse.contains(1, 3)).is_true()
    assert_that(ellipse.contains(1, 4)).is_true()
    assert_that(ellipse.contains(1, 5)).is_false()

    # some points on the y axis
    assert_that(ellipse.contains(1, 1)).is_true()
    assert_that(ellipse.contains(2, 1)).is_true()
    assert_that(ellipse.contains(3, 1)).is_true()
    assert_that(ellipse.contains(4, 1)).is_false()

    # some off the main axes
    assert_that(ellipse.contains(3, 4)).is_false()
    assert_that(ellipse.contains(3, 3)).is_false()


def test_rotated_ellipse_contains_point():
    ellipse = Ellipse(
        center_x=1, center_y=1, radius_x=2, radius_y=4,
        rotation=math.pi / 6
    )

    # rotated image of (1, 1) + (0, 4) about the center
    expected_x = 1 - 2
    expected_y = 1 + 2 * math.sqrt(3)
    print((expected_x, expected_y))
    print(ellipse.evaluate_parametric(math.pi / 4))
    assert_that(
        ellipse.contains(expected_x + 0.01, expected_y - 0.01)
    ).is_true()

    # rotated image of (1, 1) + (2, 0) about the center
    expected_x = 1 + math.sqrt(3)
    expected_y = 1 + 1
    assert_that(
        ellipse.contains(expected_x - 0.01, expected_y - 0.01)
    ).is_true()


def test_rotated_ellipse_does_not_contain_point():
    ellipse = Ellipse(
        center_x=1, center_y=1, radius_x=2, radius_y=4,
        rotation=math.pi / 6
    )

    assert_that(ellipse.contains(5, 5)).is_false()
    assert_that(ellipse.contains(-3, -3)).is_false()
    assert_that(ellipse.contains(-5, 5)).is_false()
    assert_that(ellipse.contains(5, -5)).is_false()

    # rotated image of (1, 1) + (0, 4) about (1, 1)
    expected_x = 1 - 2
    expected_y = 1 + 2 * math.sqrt(3)

    # slightly perturbed so it's not in the ellipse
    assert_that(
        ellipse.contains(expected_x - 0.01, expected_y + 0.01)
    ).is_false()

    # same for (1, 1) + (2, 0)
    expected_x = 1 + math.sqrt(3)
    expected_y = 1 + 1
    assert_that(
        ellipse.contains(expected_x + 0.01, expected_y + 0.01)
    ).is_false()


def test_evaluate_parametric_unrotated():
    ellipse = Ellipse(center_x=1, center_y=1, radius_x=2, radius_y=4)

    expected_x = 2
    expected_y = 1 + 2 * math.sqrt(3)
    actual_x, actual_y = ellipse.evaluate_parametric(math.pi / 3)

    assert_that(actual_x).is_close_to(expected_x, EPSILON)
    assert_that(actual_y).is_close_to(expected_y, EPSILON)


def test_evaluate_parametric_rotated():
    ellipse = Ellipse(
        center_x=1, center_y=1,
        radius_x=2, radius_y=4,
        rotation=math.pi/6)

    expected_x = 1 - math.sqrt(3) / 2
    expected_y = 1 + 1/2 + 3
    actual_x, actual_y = ellipse.evaluate_parametric(math.pi / 3)

    assert_that(actual_x).is_close_to(expected_x, EPSILON)
    assert_that(actual_y).is_close_to(expected_y, EPSILON)


def test_bounding_box():
    for theta in [x / 100 for x in range(int(3.15 * 2 * 100))]:
        ellipse = Ellipse(center_x=1, center_y=1, radius_x=3, radius_y=2, rotation=theta)

        compare_bounding_box_against_parametric(ellipse, ellipse.bounding_box())


def compare_bounding_box_against_parametric(ellipse, bounding_box):
    x_min, x_max = bounding_box[0]
    y_min, y_max = bounding_box[1]

    boundary_points = [
        ellipse.evaluate_parametric(t / 1000) for t in
        range(int(1000 * 3.15 * 2))
    ]

    expected_x_min = min([x for (x, y) in boundary_points])
    expected_x_max = max([x for (x, y) in boundary_points])
    expected_y_min = min([y for (x, y) in boundary_points])
    expected_y_max = max([y for (x, y) in boundary_points])

    # we choose a smaller epsilon because the error in the
    # expected boundary point calculation depends on the
    # fineness of the range of evaluated points
    epsilon = 1e-3
    assert_that(x_min).is_close_to(expected_x_min, epsilon)
    assert_that(x_max).is_close_to(expected_x_max, epsilon)
    assert_that(y_min).is_close_to(expected_y_min, epsilon)
    assert_that(y_max).is_close_to(expected_y_max, epsilon)
