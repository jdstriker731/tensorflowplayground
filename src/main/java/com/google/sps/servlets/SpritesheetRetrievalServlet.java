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

import com.google.appengine.api.blobstore.BlobKey;
import com.google.appengine.api.blobstore.BlobstoreService;
import com.google.appengine.api.blobstore.BlobstoreServiceFactory;
import com.google.appengine.api.datastore.DatastoreService;
import com.google.appengine.api.datastore.DatastoreServiceFactory;
import com.google.appengine.api.datastore.Entity;
import com.google.appengine.api.datastore.PreparedQuery;
import com.google.appengine.api.datastore.Query;
import com.google.appengine.api.datastore.Query.SortDirection;
import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import com.google.gson.Gson;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.logging.Logger;
import javax.servlet.ServletException;
import com.google.common.base.Joiner; 

/** Servlet that returns some example content. TODO: modify this file to handle comments data */
@WebServlet("/spritesheet-retrieval")
public class SpritesheetRetrievalServlet extends HttpServlet {
   
  // The ID of your GCS bucket
  private static final String BUCKET_NAME = "spritesheet_json";
  private static final Logger log = Logger.getLogger(SpritesheetRetrievalServlet.class.getName());

  @Override
  public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException, ServletException {

    // Get current user logged in to webapp 
    UserService userService = UserServiceFactory.getUserService();
    String userEmail = userService.getCurrentUser().getEmail();
    
    // Get the name of the dataset they want to visualize
    String datasetName = request.getParameter("dataset"); 

    String[] spritesheetFilePaths = {BUCKET_NAME, userEmail, datasetName, "spritesheets", "spritesheet.png"}; 
    String userSpritesheetFilePath = joinFilePaths(spritesheetFilePaths);

    log.info("OH HAI THAR! Downloading: " + userSpritesheetFilePath);

    try {
      BlobstoreService blobstoreService = BlobstoreServiceFactory.getBlobstoreService();
      BlobKey blobKey = blobstoreService.createGsBlobKey("/gs/" + userSpritesheetFilePath);
      blobstoreService.serve(blobKey, response);
      log.info("KTHNXBAI" + userSpritesheetFilePath);
    } catch(IOException e) {
      log.info(e.toString());
    }
  }

  /** Creates the path leading to the spritesheet.png file needed for their visualization */
  public static String joinFilePaths(String[] paths) {
    return Joiner.on(File.separator).join(paths);
  }
}
