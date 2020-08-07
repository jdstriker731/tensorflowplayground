# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock
import extract_embedding
import os
import tempfile
import numpy as np
CORRECT_TUP = ('bosticc@google.com', 'coolest_man_alive', 'my.jpg')


# This functions tests for multiple slashes between the dataset name and user n
# ame.


def test_too_many_slashes_name(capsys):
    slash_name_1 = 'bosticc@google.com//coolest_man_alive/original_images/my.jpg'
    assert extract_embedding.get_blob_upload_components(slash_name_1) == (
        CORRECT_TUP)

# This function tests to make sure if a slash is at the end of the file then re
# turn the last name in the file as the photo name.


def test_blank_photo_name(capsys):
    slash_at_end = 'bosticc@google.com//coolest_man_alive/original_images/my.jpg/'
    assert extract_embedding.get_blob_upload_components(slash_at_end) == (
        CORRECT_TUP)
