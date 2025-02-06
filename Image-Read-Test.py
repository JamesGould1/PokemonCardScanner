from operator import contains

import pytest
from flaskr.BasicImageRead import *

def text_scanned_from_image_contains_id_no():
    result = main(r"Processed_Files/drifbloomMissingCorner.jpeg")
    assert "061" in result
