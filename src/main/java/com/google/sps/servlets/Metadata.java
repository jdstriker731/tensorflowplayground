// Copyright 2020 Google LLC
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

package com.google.sps.servlets;

public class Metadata {
  private final String user;
  private final String dataset;
  private final String model;
  private final String visualization;
  private final long numberOfImages;
  private final long timestamp;

  /**
   * Creates a new metadata entry.
   *
   * @param user The identifier for who this dataset information belongs to.
   * @param dataset The name of the dataset this metadata corresponds to.
   * @param model The model used to generate embeddings for each image.
   * @param visualization The type of visualization used for the dataset.
   * @param numberOfImages The number of images this corresponding dataset has.
   * @param timestamp The time when this metadata was created.
   */
  public Metadata(String user, String dataset, String model, String visualization, long numImages, long timestamp) {
    this.user = user;
    this.dataset = dataset;
    this.model = model;
    this.visualization = visualization;
    this.numberOfImages = numImages;
    this.timestamp = timestamp;
  }

  /**
   * Returns the email of the user for this metadata
   */
  public String getUser() {
    return user;
  }

  /**
   * Returns the dataset name for metadata
   */
  public String getDataset() {
    return dataset;
  }

  /**
   * Returns the model for this metadata
   */
  public String getModel() {
    return model;
  }

  /**
   * Returns the type of visualization for this metadata
   */
  public String getVisualization() {
    return visualization;
  }

  /**
   * Returns the number of images for this metadata
   */
  public long getNumberOfImages() {
    return numberOfImages;
  }

  /**
   * Returns the timestamp for this metadata
   */
  public long getTimestamp() {
    return timestamp;
  }
}
