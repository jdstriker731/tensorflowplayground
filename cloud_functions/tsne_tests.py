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
from google.cloud import storage, datastore
import create_spritesheet
import os
import tempfile
import numpy as np

NAME = 'bosticc@google.com/coolest_man_alive/original_images/myles_hun.jpg'
PREFIX = 'bosticc@google.com/coolest_man_alive/original_images/'

storage_client = storage.Client()
datastore_client = datastore.Client('step-2020-johndallard')


# This functions tests for a blank dataset name of the file, and if there is no
# dataset name none should be returned from the function
def test_slashes_at_end(capsys):
    multiple_slashes_at_end = 'bosticc@google.com///'
    correct_tuple = ('bosticc@google.com', 'No dataset found')
    assert create_spritesheet.get_user_and_dataset_name(
        multiple_slashes_at_end) == (correct_tuple)

# This functions tests for multiple slashes between the dataset name and user n
# ame.


def test_too_many_slashes_name(capsys):
    slash_name_1 = 'bosticc@google.com//coolest_man_alive/original_images/my.jpg'
    correct_tuple = ('bosticc@google.com', 'coolest_man_alive')
    assert create_spritesheet.get_user_and_dataset_name(slash_name_1) == (
        correct_tuple)
