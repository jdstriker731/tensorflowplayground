# Logic tests
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

import file_path_utils as fp

NAME = 'bosticc@google.com/coolest_man_alive/original_images/myles_hun.jpg'
PHOTO_NAME = 'myles.jpg'
PREFIX = 'bosticc@google.com/coolest_man_alive/original_images/'
CORRECT_TUP = ('bosticc@google.com', 'coolest_man_alive')


# This functions tests for a blank dataset name of the file, and if there is no
# dataset name none should be returned from the function
def test_get_user_and_dataset_name_slashes_at_end():
    multiple_slashes_at_end = 'bosticc@google.com///'
    correct_tuple = ('bosticc@google.com', 'No dataset found')
    assert fp.get_user_and_dataset_name(multiple_slashes_at_end) == correct_tuple


# This functions tests for multiple slashes between the dataset name and user n
# ame.
def test_get_user_and_dataset_name_too_many_slashes():
    extra_slash = 'aj@google.com//coolest_man_alive/original_images/my.jpg'
    correct_tuple = ('aj@google.com', 'coolest_man_alive')
    assert fp.get_user_and_dataset_name(extra_slash) == (correct_tuple)


# This function tests to make sure the function works properly with a normal in
# put.
def test_user_name_normal_input():
    blank_name = 'bosticc@google.com/coolest_man_alive/original_images/myles.jpg'
    correct_tuple = ('bosticc@google.com', 'coolest_man_alive')
    assert fp.get_user_and_dataset_name(blank_name) == correct_tuple


# This function tests to make sure if a slash is at the end of the file then re
# turn the last name in the file as the photo name
def test_photo_name_blank_photo_name():
    blank_name = 'bosticc/coolest_man_alive/original_images/myles.jpg/'
    assert fp.get_photo_name(blank_name) == PHOTO_NAME


# This function tests to make sure the function works properly with a normal in
# put.
def test_photo_name_normal_input():
    blank_name = 'bosticc/coolest_man_alive/original_images/myles.jpg'
    assert fp.get_photo_name(blank_name) == PHOTO_NAME

