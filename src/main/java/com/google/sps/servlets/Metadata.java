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

import com.google.auto.value.AutoValue;

/**
 * A class that defines an entity that could be
 * placed withing some type of external storage
 * system (ex: Datastore, Firestore, SQL)
 */
@AutoValue
public abstract class Metadata {

  public static Metadata of(String user, String dataset, String model, String visualization, long numberOfImages, long timestamp) {
    return new AutoValue_Metadata(user, dataset, model, visualization, numberOfImages, timestamp);
  }

  public abstract String user();

  public abstract String dataset();

  public abstract String model();

  public abstract String visualization();

  public abstract long numberOfImages();

  public abstract long timestamp();
}
