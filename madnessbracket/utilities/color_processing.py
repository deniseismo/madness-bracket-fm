import wcag_contrast_ratio as contrast
from colormath.color_objects import sRGBColor

from madnessbracket import cache


def convert_from_hex_to_rgb(hex_color):
    """
    converts a hex color into an RGB one
    """
    rgb_color = sRGBColor.new_from_rgb_hex(hex_color)
    return rgb_color.get_upscaled_value_tuple()


def convert_from_rgb_to_hex(rgb_color):
    """
    converts an RGB color to hex
    """
    hex_color = sRGBColor.get_rgb_hex(rgb_color)
    return hex_color


def get_a_color_in_between(color_1, color_2):
    """
    :param: color_1: rgb_color
    :param: color_2: rgb_color
    get a color that is a halfway between two colors
    """
    red_1, green_1, blue_1 = color_1
    red_2, green_2, blue_2 = color_2
    color_in_between = ((red_1 + red_2) / 2, (green_1 +
                                              green_2) / 2, (blue_1 + blue_2) / 2)
    return color_in_between


def get_luminance(rgb_r, rgb_g, rgb_b):
    """
    luminance © https://www.w3.org/TR/WCAG20-TECHS/G17.html
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B where R, G and B
    """
    luminance = 0.2126 * rgb_r + 0.7152 * rgb_g + 0.0722 * rgb_g
    return luminance


def get_contrast_color_by_luminance(luminance):
    """
    figure out whether the appropriate contrast color for the given luminance is black or white
    © https://www.w3.org/TR/WCAG20-TECHS/G17.html
    If L ≥ 0.175: black
    If L ≤ 0.1833: white
    0.1791  cutoff middle
    """
    if luminance >= 0.179:
        return "black"
    else:
        return "white"


def get_contrast_color_for_hex_color(hex_color):
    """
    a shortcut function that returns a contrast color for a given hex color
    used for getting the appropriate text color for a given background
    combines three other functions
    """
    rgb_color = convert_from_hex_to_rgb(hex_color)
    luminance = get_luminance(*rgb_color)
    contrast_color = get_contrast_color_by_luminance(luminance)
    return contrast_color


@cache.memoize(timeout=3600)
def get_contrast_color_for_two_color_gradient(color_1, color_2):
    """
    calculate the most appropriate contrast color for a two-colored gradient background
    :param: color_1: hex color
    :param: color_2: hex color
    """
    if not color_2 or not color_2:
        print("no colors provided")
        return None
    if isinstance(color_1, str) and isinstance(color_2, str):
        print("converting hex to rgb")
        color_1_rgb = convert_from_hex_to_rgb(color_1)
        color_2_rgb = convert_from_hex_to_rgb(color_2)
    else:
        color_1_rgb, color_2_rgb = color_1, color_2
    # calculate a color in between the two for better results
    color_in_between = get_a_color_in_between(color_1_rgb, color_2_rgb)
    # downscale values
    color_1_rgb = sRGBColor(*color_1_rgb, is_upscaled=True).get_value_tuple()
    color_in_between = sRGBColor(
        *color_in_between, is_upscaled=True).get_value_tuple()
    gradient_colors = [color_1_rgb, color_in_between]

    color_black = (0, 0, 0)
    color_white = (1, 1, 1)
    black_contrast = sum([get_contrast_ratio(color, color_black)
                          for color in gradient_colors])
    white_contrast = sum([get_contrast_ratio(color, color_white)
                          for color in gradient_colors])
    if white_contrast >= black_contrast:
        return "white"
    else:
        return "black"


def get_contrast_ratio(color_1, color_2):
    return contrast.rgb(color_1, color_2)
