def pytest_addoption(parser):
    parser.addoption(
        "--image-name",
        action="store",
        required=True,
        help="Name of the RBD image to create"
    )
    parser.addoption(
        "--image-size",
        action="store",
        required=True,
        help="Size of the RBD image to create"
    )
