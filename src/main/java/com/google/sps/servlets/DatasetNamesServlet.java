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

import com.google.sps.servlets.Metadata;
import com.google.sps.servlets.MetadataStore;
import com.google.sps.servlets.DatastoreMetadataStore;

@WebServlet("/dataset-names")
public class DatasetNamesServlet extends HttpServlet {

  private static final Gson GSON = new Gson();

  // Instance of DatastoreMetadatastore class 
  private static final MetadataStore DATASTORE_STORAGE = new DatastoreMetadataStore();

  @Override
  public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
    // Get current user logged in to webapp
    UserService userService = UserServiceFactory.getUserService();
    String userEmail = userService.getCurrentUser().getEmail();

    // Get the logged in user's datasets
    List<String> userDatasets = DATASTORE_STORAGE.getUsersDatasets(userEmail);

    // Convert userDatasets to exportable json format
    String json = GSON.toJson(userDatasets);

    // Send the JSON as the response.
    response.setContentType("application/json;");
    response.getWriter().println(json);
  }
}
