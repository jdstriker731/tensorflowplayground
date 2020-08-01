import * as THREE from 'three';
import React from 'react';
import { TrackballControls } from 'three/examples/jsm/controls/TrackballControls.js';

const IMAGE_SIZE = 64;

class Image {
  constructor(size) {
    this.width = size;
    this.height = size;
  }
}

class Atlas {
  constructor(image, numImages, numRows, numColumns) {
    this.image = image;
    this.width = image.width * numColumns;
    this.height = image.height * numRows;
    this.numImages = numImages;
  }
}

class Point {
  constructor(x, y, z) {
    function randomInt() {
      const val = Math.random() * 700;
      return Math.random() > 0.5 ? -val : val;
    }

    if (x == undefined) {
      this.x = randomInt();
    } else {
      this.x = x;
    }

    if (y == undefined) {
      this.y = randomInt();
    } else {
      this.y = y;
    }

    if (z == undefined) {
      this.z = -400;
    } else {
      this.z = z;
    }
  }
}

class AtlasGeometry extends THREE.Geometry {
  constructor(atlas, points) {
    super();

    for (var i = 0; i < atlas.numImages; i++) {
      // Create x, y, z coords for this subimage
      const coords = points[i];

      this.vertices.push(
        new THREE.Vector3(coords.x, coords.y, coords.z),
        new THREE.Vector3(coords.x + atlas.image.width, coords.y, coords.z),
        new THREE.Vector3(
          coords.x + atlas.image.width,
          coords.y + atlas.image.height,
          coords.z
        ),
        new THREE.Vector3(coords.x, coords.y + atlas.image.height, coords.z)
      );

      // Add the first face (the lower-right triangle)
      var faceOne = new THREE.Face3(
        this.vertices.length - 4,
        this.vertices.length - 3,
        this.vertices.length - 2
      );

      // Add the second face (the upper-left triangle)
      var faceTwo = new THREE.Face3(
        this.vertices.length - 4,
        this.vertices.length - 2,
        this.vertices.length - 1
      );

      // Add those faces to the geometry
      this.faces.push(faceOne, faceTwo);

      // Identify this subimage's offset in the x dimension
      // An xOffset of 0 means the subimage starts flush with
      // the left-hand edge of the atlas
      var xOffset = (i % 10) * (atlas.image.width / atlas.width);

      // Identify the subimage's offset in the y dimension
      // A yOffset of 0 means the subimage starts flush with
      // the top edge of the atlas
      var yOffset = Math.floor(i / 10) * (atlas.image.height / atlas.height);

      // Use the xOffset and yOffset (and the knowledge that
      // each row and column contains only 10 images) to specify
      // the regions of the current image
      this.faceVertexUvs[0].push([
        new THREE.Vector2(xOffset, yOffset),
        new THREE.Vector2(xOffset + 0.1, yOffset),
        new THREE.Vector2(xOffset + 0.1, yOffset + 0.1)
      ]);

      // Map the region of the image described by the lower-left,
      // upper-right, and upper-left vertices to `faceTwo`
      this.faceVertexUvs[0].push([
        new THREE.Vector2(xOffset, yOffset),
        new THREE.Vector2(xOffset + 0.1, yOffset + 0.1),
        new THREE.Vector2(xOffset, yOffset + 0.1)
      ]);
    }
  }
}

export class ThreeRenderer extends React.Component {
  constructor(props) {
    super(props);

    this.dataset = props.dataset;
    
    this.canvasWidth = props.canvasWidth;
    this.canvasHeight = props.canvasHeight;

    this.camera = undefined;
    this.scene = undefined;
    this.controls = undefined;
    this.material = undefined;
    this.renderer = undefined;
    this.canvas = undefined;
    this.light = undefined;
  }

  // Loads json object for dataset and returns array of points
  async initPoints(material) {
    var numImages = 0;
    const numRows = 1;

    const json_url = "/coordinates-retrieval?dataset=".concat(this.dataset);
    const result = await fetch(json_url);
    const out = await result.json();

    const points = out['points'].map((point_json) => {
      const {x, y, z} = point_json;
      return new Point(x, y, z);
    });
    
    numImages = points.length;
    const numColumns = numImages;

    const atlas = new Atlas(new Image(IMAGE_SIZE), numImages, numRows, numColumns);

    const geometry = new AtlasGeometry(atlas, points);

    const mesh = new THREE.Mesh(geometry, this.material);
    mesh.position.set(0, 0, 0);
    this.scene.add(mesh);

    const component = this;
    function render3d() {
      component.renderer.render(component.scene, component.camera);
      requestAnimationFrame(render3d);
      component.controls.update();
    }
  
    render3d();
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
    const camera = new THREE.PerspectiveCamera(
      fov,
      aspect,
      nearClippingPlane,
      farClippingPlane
    );
    camera.position.z = 500;

    return camera;
  }

  componentDidMount() {
    this.renderer = new THREE.WebGLRenderer({antialias: true, canvas: this.canvas});
    this.renderer.setSize(800, 800);

    this.camera = this.createCamera();
    this.canvas = this.createCanvas();
    this.scene = new THREE.Scene();

    this.light = new THREE.PointLight(0xffffff, 0.7, 0);
    this.light.position.set(1, 1, 100);
    this.scene.add(this.light);

    this.controls = new TrackballControls(this.camera, this.renderer.domElement);

    this.loader = new THREE.TextureLoader();

    const img_query = '/spritesheet-retrieval?dataset='.concat(this.dataset);
    this.material = new THREE.MeshBasicMaterial({
      map: this.loader.load(img_query)
    });

    this.material.side = THREE.DoubleSide;

    // Create list of (random) points to map images to
    // Later on, this will be t-SNE coordinates
    this.initPoints();
  }

  render(){
    return(
      <div ref={ref => (this.mount = ref)} />
    )
  }
}
