import * as three from 'three';
import React from 'react';
import { TrackballControls } from 'three/examples/jsm/controls/TrackballControls.js';

const IMAGE_SIZE = 64;

// Class to represent a single image in the dataset with width and height
export class ImageParams {
  constructor(size) {
    this.width = size;
    this.height = size;
  }
}

// An atlas represents a spritesheet image, and is used to iterate over each image
// in the dataset.
export class Atlas {
  constructor(image, numImages, numRows, numColumns) {
    this.image = image;
    this.width = image.width * numColumns;
    this.height = image.height * numRows;
    this.numImages = numImages;
  }
}

// Class to represent a point in 3D space with x, y, and z coords
export class Point {
  constructor(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }
}

// Atlas geometry is the geometry that holds all the images in a dataset
// It is textured with the spritesheet to create a mesh
export class AtlasGeometry extends three.Geometry {
  constructor(atlas, points) {
    super();

    for (var i = 0; i < atlas.numImages; i++) {
      // Create x, y, z coords for this subimage
      // Coords technically don't represent the center of the image
      // However this doesn't affect output because all images are the same size
      const coords = points[i];

      // 3D vertices of the image thumbnails
      this.vertices.push(
        new three.Vector3(coords.x, coords.y, coords.z),
        new three.Vector3(coords.x + atlas.image.width, coords.y, coords.z),
        new three.Vector3(
          coords.x + atlas.image.width,
          coords.y + atlas.image.height,
          coords.z
        ),
        new three.Vector3(coords.x, coords.y + atlas.image.height, coords.z)
      );

      // Add the first face (the lower-right triangle)
      var faceOne = new three.Face3(
        this.vertices.length - 4,
        this.vertices.length - 3,
        this.vertices.length - 2
      );

      // Add the second face (the upper-left triangle)
      var faceTwo = new three.Face3(
        this.vertices.length - 4,
        this.vertices.length - 2,
        this.vertices.length - 1
      );

      // Add those faces to the geometry
      this.faces.push(faceOne, faceTwo);

      // Identify this subimage's offset in the x dimension
      // An xOffset of 0 means the subimage starts flush with
      // the left-hand edge of the atlas
      var xOffset = i * (atlas.image.width / atlas.width);

      // Identify the subimage's offset in the y dimension
      // A yOffset of 0 means the subimage starts flush with
      // the top edge of the atlas
      var yOffset = 0;

      // Use the xOffset and yOffset (and the knowledge that
      // each row and column contains only 10 images) to specify
      // the regions of the current image
      this.faceVertexUvs[0].push([
        new three.Vector2(xOffset, yOffset),
        new three.Vector2(xOffset + (1.0 / atlas.numImages), yOffset),
        new three.Vector2(xOffset + (1.0 / atlas.numImages), yOffset + 1.0)
      ]);

      // Map the region of the image described by the lower-left,
      // upper-right, and upper-left vertices to `faceTwo`
      this.faceVertexUvs[0].push([
        new three.Vector2(xOffset, yOffset),
        new three.Vector2(xOffset + (1.0 / atlas.numImages), yOffset + 1.0),
        new three.Vector2(xOffset, yOffset + 1.0)
      ]);
    }
  }
}

// Class to render AtlasGeometry and allow for interactivity
export class ThreeRenderer extends React.Component {
  // Set defaults and declare members
  constructor(props) {
    super(props);

    this.dataset = props.dataset;
    
    this.canvasWidth = props.canvasWidth;
    this.canvasHeight = props.canvasHeight;

    this.render3dFn_ = this.render3d.bind(this);

    this.camera = undefined;
    this.scene = undefined;
    this.controls = undefined;
    this.material = undefined;
    this.renderer = undefined;
    this.canvas = undefined;
    this.light = undefined;
  }

  // Loads JSON data from 
  async loadPointsJson() {
    const json_url = '/coordinates-retrieval?dataset='.concat(this.dataset);
    const result = await fetch(json_url);
    const out = await result.json();

    return out;
  }

  parsePoints(jsonData) {
    const points = jsonData['points'].map((point_json) => {
      const {x, y, z} = point_json;
      return new Point(x, y, z);
    });

    return points;
  }

  // Loads json object for dataset and renders the object
  initPoints(json) {
    var numImages = 0;
    const numRows = 1;

    const points = this.parsePoints(json);
    
    numImages = points.length;
    const numColumns = numImages;

    const atlas = new Atlas(new ImageParams(IMAGE_SIZE), numImages, numRows, numColumns);

    const geometry = new AtlasGeometry(atlas, points);

    const mesh = new three.Mesh(geometry, this.material);
    mesh.position.set(0, 0, 0);
    this.scene.add(mesh);
  
    this.render3dFn_();
  }

  // Renders the elements in 3D space
  render3d() {
    this.renderer.render(this.scene, this.camera);
    requestAnimationFrame(this.render3dFn_);
    this.controls.update();
  }

  // Appends a new canvas element to this.mount
  createCanvas() {
    const canvas = document.createElement('canvas');
    this.mount.appendChild(canvas);
    canvas.style.height = this.canvasHeight;
    canvas.style.width = this.canvasWidth;
    
    return canvas;
  }

  // Creates a new Three.js camera object
  createCamera() {
    const fov = 90;
    const aspect = 2; // the canvas default
    const nearClippingPlane = 0.1;
    const farClippingPlane = 10000;
    const camera = new three.PerspectiveCamera(
      fov,
      aspect,
      nearClippingPlane,
      farClippingPlane
    );
    camera.position.z = 500;

    return camera;
  }

  // Handle Three render code when the component mounts to the react DOM
  componentDidMount() {
    this.canvas = this.createCanvas();

    this.renderer = new three.WebGLRenderer({antialias: true, canvas: this.canvas});
    this.renderer.setSize(800, 800);

    this.camera = this.createCamera();
    this.scene = new three.Scene();
    this.light = new three.PointLight(0xffffff, 0.7, 0);
    this.light.position.set(1, 1, 100);
    this.scene.add(this.light);

    this.controls = new TrackballControls(this.camera, this.renderer.domElement);

    this.loader = new three.TextureLoader();

    const img_query = '/spritesheet-retrieval?dataset='.concat(this.dataset);
    this.material = new three.MeshBasicMaterial({
      map: this.loader.load(img_query)
    });

    this.material.side = three.DoubleSide;

    // Initialize points and render
    const jsonOut = this.loadPointsJson();
    this.initPoints(jsonOut);
  }

  render(){
    return(
      <div ref={ref => (this.mount = ref)} />
    )
  }
}
