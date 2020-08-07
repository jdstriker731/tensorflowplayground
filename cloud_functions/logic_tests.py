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
CORRECT_TUP = ('bosticc@google.com', 'coolest_man_alive')

storage_client = storage.Client()
datastore_client = datastore.Client('step-2020-johndallard')


# This functions tests for a blank dataset name of the file, and if there is no
# dataset name none should be returned from the function
def test_get_user_and_dataset_name_slashes_at_end(this_file):
    multiple_slashes_at_end = 'bosticc@google.com///'
    correct_tuple = ('bosticc@google.com', 'No dataset found')
    assert this_file.get_user_and_dataset_name(
        multiple_slashes_at_end) == (correct_tuple)


# This functions tests for multiple slashes between the dataset name and user n
# ame.
def test_get_user_and_dataset_name_too_many_slashes(this_file):
    slash_name_1 = 'bosticc@google.com//coolest_man_alive/original_images/my.jpg'
    correct_tuple = ('bosticc@google.com', 'coolest_man_alive')
    assert this_file.get_user_and_dataset_name(slash_name_1) == (
        correct_tuple)


# This function tests to make sure if a slash is at the end of the file then re
# turn the last name in the file as the photo name
def test_photo_name_blank_photo_name(this_file):
    blank_name = 'bosticc/coolest_man_alive/original_images/myles.jpg/'
    assert this_file.get_photo_name(blank_name) == 'myles.jpg'

# This function tests to make sure the function works properly with a normal in
# put.
def test_photo_name_normal_input(this_file):
    blank_name = 'bosticc/coolest_man_alive/original_images/myles.jpg'
    assert this_file.get_photo_name(blank_name) == 'myles.jpg'


def test_too_many_slashes_name(this_file):
    slash_name_1 = 'bosticc@google.com//coolest_man_alive/original_images/my.jpg'
    assert this_file.get_blob_upload_components(slash_name_1) == (
        CORRECT_TUP)

# This function tests to make sure if a slash is at the end of the file then re
# turn the last name in the file as the photo name.


def test_blank_photo_name(this_file):
    slash_at_end = 'bosticc@google.com//coolest_man_alive/original_images/my.jpg/'
    assert this_file.get_blob_upload_components(slash_at_end) == (
        CORRECT_TUP)
