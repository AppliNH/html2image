from html2image import Html2Image
from PIL import Image

import pytest

OUTPUT_PATH = "tests_output"


def test_bad_browser():
    with pytest.raises(ValueError):
        Html2Image(browser='watergoupil')


def test_good_browser():
    Html2Image(browser='cHrOme')


def test_screenshot_url():
    hti = Html2Image(output_path=OUTPUT_PATH)

    paths = hti.screenshot(url='https://www.python.org', save_as="pyorg.png")
    img = Image.open(paths[0])
    assert (1920, 1080) == img.size  # default size


def test_screenshot_multiple_urls():
    hti = Html2Image(output_path=OUTPUT_PATH)
    paths = hti.screenshot(
        url=['https://www.python.org', "https://www.example.org/"],
        save_as="mixed_urls.png",
    )

    for path in paths:
        img = Image.open(path)
        assert (1920, 1080) == img.size  # default size


def test_screenshot_url_custom_size():
    hti = Html2Image(output_path=OUTPUT_PATH)

    test_size = (334, 485)

    paths = hti.screenshot(
        url='https://www.python.org',
        save_as="pyorg_custom_size.png",
        size=test_size,
    )

    img = Image.open(paths[0])
    assert test_size == img.size  # default size


def test_screenshot_url_custom_sizes():
    hti = Html2Image(output_path=OUTPUT_PATH)

    test_sizes = [
        (100, 100),
        (100, 1000),
        (100, 200),
    ]

    paths = hti.screenshot(
        url=[
            'https://www.python.org',
            'https://www.wikipedia.org/',
            'https://www.example.org/',
        ],
        save_as="mixed_urls_custom_sizes.png",
        size=test_sizes,
    )

    for wanted_size, path in zip(test_sizes, paths):
        img = Image.open(path)
        assert wanted_size == img.size


def test_screenshot_url_sizes_missing_custom_names():
    hti = Html2Image(output_path=OUTPUT_PATH)

    test_sizes = [
        (100, 100),
        (100, 1000),
    ]

    paths = hti.screenshot(
        url=[
            'https://www.python.org',
            'https://www.wikipedia.org/',
            'https://www.example.org/',
        ],
        save_as=[
            "python_100_100.png",
            "wikipedia_100_1000.png",
            "example_100_1000.png",
        ],
        size=test_sizes,
    )

    for wanted_size, path in zip(test_sizes, paths):
        img = Image.open(path)
        assert wanted_size == img.size


def test_screenshot_string():
    hti = Html2Image(output_path=OUTPUT_PATH)

    html = "Hello"
    css = "body{background: blue; font-size: 50px;}"

    paths = hti.screenshot(
        html_str=html, css_str=css, save_as="blue_big_hello.png"
    )

    img = Image.open(paths[0])
    pixels = img.load()

    assert (1920, 1080) == img.size  # default size

    # check colors at top left corner
    assert pixels[0, 0] == (0, 0, 255, 255)  # blue + no transparency


def test_screenshot_string_different_sizes():
    hti = Html2Image(output_path=OUTPUT_PATH)

    test_sizes = [
        (100, 100),
        (100, 1000),
        (100, 200),
    ]

    html = "Hello"

    paths = hti.screenshot(
        html_str=[html]*3,
        save_as="from_string_custom_size.png",
        size=test_sizes
    )

    for wanted_size, path in zip(test_sizes, paths):
        img = Image.open(path)
        assert wanted_size == img.size


def test_screenshot_other_svg():
    hti = Html2Image(output_path=OUTPUT_PATH)

    paths = hti.screenshot(
        other_file='./examples/star.svg', save_as="star_svg.png"
    )

    img = Image.open(paths[0])
    pixels = img.load()

    assert (1920, 1080) == img.size  # default size

    # check colors at top left corner
    assert pixels[0, 0] == (0, 0, 0, 0)  # full transparency no color


def test_screenshot_file():
    hti = Html2Image(output_path=OUTPUT_PATH)

    paths = hti.screenshot(
        html_file="./examples/blue_page.html",
        css_file="./examples/blue_background.css",
        save_as="from_file.png",
    )

    img = Image.open(paths[0])
    pixels = img.load()

    assert (1920, 1080) == img.size  # default size

    # check colors at top left corner
    assert pixels[0, 0] == (0, 0, 255, 255)  # blue + no transparency


def test_screenshot_file_different_sizes():
    hti = Html2Image(output_path=OUTPUT_PATH)

    test_sizes = [
        (100, 100),
        (100, 1000),
        (100, 200),
    ]

    paths = hti.screenshot(
        html_file=["./examples/blue_page.html"]*3,
        save_as="from_file_custom_size.png",
        size=test_sizes
    )

    for wanted_size, path in zip(test_sizes, paths):
        img = Image.open(path)
        assert wanted_size == img.size


def test_extend_size_param():
    hti = Html2Image(output_path=OUTPUT_PATH)

    assert hti._extend_size_param([(50, 50)], 1) \
        == [(50, 50)]

    assert hti._extend_size_param([(50, 50)], 3) \
        == [(50, 50), (50, 50), (50, 50)]

    assert hti._extend_size_param([(50, 50), (70, 60), (80, 90)], 5) \
        == [(50, 50), (70, 60), (80, 90), (80, 90), (80, 90)]

    assert hti._extend_size_param([], 3) \
        == [(1920, 1080), (1920, 1080), (1920, 1080)]


def test_extend_save_as_param():
    hti = Html2Image(output_path=OUTPUT_PATH)

    assert hti._extend_save_as_param(['a.png', 'b.png'], 2) == \
        ['a.png', 'b.png']

    assert hti._extend_save_as_param(['a.png', 'b.png'], 4) == \
        ['a.png', 'b_0.png', 'b_1.png', 'b_2.png']

    assert hti._extend_save_as_param(['a.png', 'b.png'], 0) == \
        ['a.png', 'b.png']

    assert hti._extend_save_as_param(['a.png', 'b.png', None, 65], 2) == \
        ['a.png', 'b.png']
