'''A module that performs math on ellipses.
'''

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Ellipse:
    '''An ellipse, possibly shifted and rotated about its center.

    The canonical equation for an ellipse represented by an instance is

    (
      (x - ellipse.center_x) cos(ellipse.rotation)
      - (y - ellipse.center_y) sin(ellipse.rotation)
    )^2 / ellipse.radius_x^2
    +
    (
      (x - ellipse.center_x) sin(ellipse.rotation)
      + (y - ellipse.center_y) cos(ellipse.rotation)
    )^2 / ellipse.radius_y^2
    = 1

    Example:

    ellipse = Ellipse(
        center_x=10, center_y=5, radius_x=3, radius_y=2, rotation=math.pi/4
    )
    '''

    '''The x coordinate of the center of the ellipse.'''
    center_x: float = 0

    '''The y coordinate of the center of the ellipse.'''
    center_y: float = 0

    '''The length of the radius along the x-axis (before rotating).'''
    radius_x: float = 1

    '''The length of the radius along the y-axis (before rotating).'''
    radius_y: float = 1

    '''The counterclockwise angle (in radians) by which this ellipse is rotated.'''
    rotation: float = 0

    def evaluate_parametric(self, t):
        '''
        Given a parameter t, return the point lying on the ellipse that is at t
        radians counterclockwise from the point(x_radius, 0), or its rotated image if
        this ellipse is rotated.

        I.e., if the ellipse is rotated by pi/8, and t=pi/8, then this will give
        the point at pi/4 from the horizontal axis _after_ rotating, which is the
        point at an angle of pi/8 from the rotated point (self.radius_x, 0).
        '''
        x = (
            self.center_x
            + self.radius_x * math.cos(t) * math.cos(self.rotation)
            - self.radius_y * math.sin(t) * math.sin(self.rotation)
        )
        y = (
            self.center_y
            + self.radius_x * math.cos(t) * math.sin(self.rotation)
            + self.radius_y * math.sin(t) * math.cos(self.rotation)
        )
        return (x, y)

    def contains(self, x, y):
        '''
        Return true if the ellipse contains the given point in its interior
        or on its boundary.
        '''
        # translate the test point (and implicitly the ellipse) to the center
        x_dev = x - self.center_x
        y_dev = y - self.center_y

        # rotate in the reverse direction of the ellipse's rotation
        cos_rotation = math.cos(-self.rotation)
        sin_rotation = math.sin(-self.rotation)
        rotated_x = x_dev * cos_rotation - y_dev * sin_rotation
        rotated_y = x_dev * sin_rotation + y_dev * cos_rotation

        # now test as if it were an unrotated, untranslated ellipse
        return (rotated_x / self.radius_x) ** 2 + (rotated_y / self.radius_y) ** 2 <= 1

    def bounding_box(self):
        '''Compute the axis-aligned bounding box of the ellipse.'''
        x_rad = (
            self.radius_x ** 2 * math.cos(self.rotation) ** 2
            + self.radius_y ** 2 * math.sin(self.rotation) ** 2
        )
        y_rad = (
            self.radius_x ** 2 * math.sin(self.rotation) ** 2
            + self.radius_y ** 2 * math.cos(self.rotation) ** 2
        )

        x_sqrt = math.sqrt(x_rad)
        y_sqrt = math.sqrt(y_rad)
        return (
            (-x_sqrt + self.center_x, x_sqrt + self.center_x),
            (-y_sqrt + self.center_y, y_sqrt + self.center_y),
        )
