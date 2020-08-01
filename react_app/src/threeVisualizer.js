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
  }

  // Loads json object for dataset and initiates Atlas object
  initAtlas() {
    const json_url = "/coordinates-retrieval?dataset=".concat(this.dataset);
    var numImages = 0;
    const numRows = 1;

    fetch(json_url)
    .then(result => result.json())
    .then(out => {
        numImages = out['points'].length;
      });

    const image = new Image(IMAGE_SIZE);
    const numColumns = numImages;

    return new Atlas(image, numImages, numRows, numColumns);
  }

  // Loads json object for dataset and returns array of points
  initPoints() {
    const json_url = "/coordinates-retrieval?dataset=".concat(this.dataset);
    var points = []

    fetch(json_url)
    .then(result => result.json())
    .then(out => {
      for (const point of out['points']){
        const x = point['x'];
        const y = point['y'];
        const z = point['z'];

        points.push(new Point(x, y, z));
      }
    });

    return points;
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
    const canvas = this.createCanvas();
    const renderer = new THREE.WebGLRenderer({antialias: true, canvas});
    renderer.setSize(800, 800);

    const scene = new THREE.Scene();
    const camera = this.createCamera();

    const light = new THREE.PointLight(0xffffff, 0.7, 0);
    light.position.set(1, 1, 100);
    scene.add(light);

    const controls = new TrackballControls(camera, renderer.domElement);

    const loader = new THREE.TextureLoader();
    loader.setCrossOrigin('anonymous');

    const query = '/spritesheet-retrieval?dataset='.concat(this.dataset);

    // Load an image file into a custom material
    const material = new THREE.MeshBasicMaterial({
      map: loader.load(query)
    });

    material.side = THREE.DoubleSide;

    // Identify the total number of cols & rows in the image atlas
    const atlas = this.initAtlas();

    // Create list of (random) points to map images to
    // Later on, this will be t-SNE coordinates
    const points = this.initPoints();

    // ------ CREATING CUSTOM GEOMETRY -------
    const geometry = new AtlasGeometry(atlas, points);

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(0, 0, 0);
    scene.add(mesh);

    function render() {
      renderer.render(scene, camera);
      requestAnimationFrame(render);
      controls.update();
    }

    render();
  }

  render(){
    return(
      <div ref={ref => (this.mount = ref)} />
    )
  }
}
