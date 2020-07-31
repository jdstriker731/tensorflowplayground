// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package com.google.sps;

public class Metadata {
  private final String user;
  private final String dataset;
  private final String model;
  private final String visualization;
  private final int numberOfImages;
  private final int timestamp;

  public Metadata(String user, String dataset, String model, String visualization, int numImages, int timestamp) {
    this.user = user;
    this.dataset = dataset;
    this.model = model;
    this.visualization = visualization;
    this.numberOfImages = numImages;
    this.timestamp = timestamp;
  }

  public String getUser() {
    return user;
  }

  public String getDataset() {
    return dataset;
  }

  public String getModel() {
    return model;
  }

  public String getVisualization() {
    return visualization;
  }

  public int getNumberOfImages() {
    return numberOfImages;
  }

  public int getTimestamp() {
    return timestamp;
  }
}