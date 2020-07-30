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
 
package com.google.sps.servlets;
 
import java.io.IOException;
import java.io.InputStream;
import java.util.Collection;
import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.datastore.Query.SortDirection;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;
import java.nio.file.Files;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.BlobInfo;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import java.nio.file.Paths;
import com.google.common.collect.ImmutableList;

/** Servlet for uploading files. */
@WebServlet("/upload")
@MultipartConfig
public class UploadServlet extends HttpServlet {

  // The ID of your GCP project
  private static final String PROJECT_ID = "step-2020-johndallard";

  // The ID of your GCS bucket
  private static final String BUCKET_NAME = "embedding-visualizer-bucket";

  @Override
  public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {
    //  Get all the Dataset Entities
    Query query = new Query("MetaData").addSort("timestamp", SortDirection.ASCENDING);

    /* Get current user logged in to webapp */
    UserService userService = UserServiceFactory.getUserService();

    DatastoreService datastore = DatastoreServiceFactory.getDatastoreService();
    PreparedQuery results = datastore.prepare(query);

    /*  Get metadata (for comparison and eventual storage) */
    String userEmail = userService.getCurrentUser().getEmail();
    String datasetName = request.getParameter("dataset-namer");
    long timestamp = System.currentTimeMillis();


    for (Entity entity : results.asIterable()) {
      String email = (String) entity.getProperty("user-email");
      String dataset = (String) entity.getProperty("dataset-name");

      if (email.equals(userEmail)) {
        if (dataset.equals(datasetName)) {
          // This dataset already exists for the user
          response.sendRedirect("/already_exists.html");
        }
      }
    }

    /* Upload images from form to GCP bucket */

    int imageCount = 0;

    Storage storage = StorageOptions.newBuilder().setProjectId(PROJECT_ID).build().getService();

    // Create new directory within user's subdirectory for this dataset
    String userDirectory = userEmail + "/";
    String newDatasetDir = userDirectory + datasetName + "/";
    String userImagesDir = newDatasetDir + "original_images/";
    String userThumbnailsDir = newDatasetDir + "thumbnails/";
    String userSpritesheetDir = newDatasetDir + "spritesheets/";
    String userEmbeddingsDir = newDatasetDir + "embeddings/";
    ImmutableList<String> directories = ImmutableList.of(userImagesDir, userThumbnailsDir, userSpritesheetDir, userEmbeddingsDir);

    BlobId blobId = BlobId.of(BUCKET_NAME, userDirectory);
    BlobInfo blobInfo = BlobInfo.newBuilder(blobId).build();
    storage.create(blobInfo);

    directories.forEach(pathway -> createBucketSubDirectory(pathway, storage, BUCKET_NAME));
      

    Collection<Part> parts = request.getParts();
      
    for (Part part : parts) {
      if (!"file-upload-dialog".equals(part.getName())) continue;
      InputStream inputStream = part.getInputStream();

      String fileName = Paths.get(part.getSubmittedFileName()).getFileName().toString(); // MSIE fix.
      //The ID of your GCS object
      String objectName = userImagesDir + fileName;

      blobId = BlobId.of(BUCKET_NAME, objectName);
      blobInfo = BlobInfo.newBuilder(blobId).build();
      storage.create(blobInfo, inputStream);
      imageCount++;
    }
    
    /* Store metadata in Datastore */
    Entity datasetEntity = new Entity("MetaData");
    datasetEntity.setProperty("user-email", userEmail);
    datasetEntity.setProperty("dataset-name", datasetName);
    datasetEntity.setProperty("model", "DELG");
    datasetEntity.setProperty("visualizer-type", "t-SNE");
    datasetEntity.setProperty("image-count", imageCount);
    datasetEntity.setProperty("timestamp", timestamp);
    datastore.put(datasetEntity);

    /* Redirect user */
    response.sendRedirect("/index.html");
  }

  private void createBucketSubDirectory(String path, Storage storageLocation, String bucket) {
    BlobId blobId = BlobId.of(bucket, path);
    BlobInfo blobInfo = BlobInfo.newBuilder(blobId).build();
    storageLocation.create(blobInfo);
  }
}
