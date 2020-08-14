import React from 'react';
import { Atlas, ImageParams, AtlasGeometry } from './threeVisualizer.js';
import renderer from 'react-test-renderer';
import * as three from 'three';

function createTestGeometry() {
  const testPoints = [
    {
      'x': 1.0,
      'y': 1.0,
      'z': 1.0
    },
    {
      'x': 0.0,
      'y': 0.0,
      'z': 0.0
    }
  ];

  const testImageParams = new ImageParams(10);
  const testAtlas = new Atlas(testImageParams, 2, 1, 2);

  const testAtlasGeometry = new AtlasGeometry(testAtlas, testPoints);

  return testAtlasGeometry;
}

test('AtlasGeometry correctly pushes vertices in expected case', () => {
  const testAtlasGeometry = createTestGeometry();

  const expectedVertices = [
    new three.Vector3(1.0, 1.0, 1.0),
    new three.Vector3(21.0, 1.0, 1.0),
    new three.Vector3(21.0, 11.0, 1.0),
    new three.Vector3(1.0, 11.0, 1.0),

    new three.Vector3(0.0, 0.0, 0.0),
    new three.Vector3(20.0, 0.0, 0.0),
    new three.Vector3(20.0, 10.0, 0.0),
    new three.Vector3(0.0, 10.0, 0.0)
  ];

  expect(testAtlasGeometry.vertices).toBe(expectedVertices);
});

test('AtlasGeometry pushes correct faceVertexUVs', () => {
  const testAtlasGeometry = createTestGeometry();

  const expectedFaceVertexUvs = [
    [
      three.Vector2(0.0, 0.0),
      three.Vector2(0.5, 0.0),
      three.Vector2(0.5, 1.0)
    ],

    [
      three.Vector2(0.0, 0.0),
      three.Vector2(0.5, 1.0),
      three.Vector2(0.0, 1.0)
    ],

    [
      three.Vector2(0.5, 0.0),
      three.Vector2(1.0, 0.0),
      three.Vector2(1.0, 1.0)
    ],

    [
      three.Vector2(0.5, 0.0),
      three.Vector2(1.0, 1.0),
      three.Vector2(0.5, 1.0)
    ]
  ];

  expect(testAtlasGeometry.faceVertexUvs[0]).toBe(expectedFaceVertexUvs);
});

test('AtlasGeometry pushes correct faces', () => {
  const testAtlasGeometry = createTestGeometry();

  const expectedFaces = [
    new three.Face3(0, 1, 2),
    new three.Face3(0, 2, 3),
    new three.Face3(0, 1, 2),
    new three.Face3(0, 2, 3)
  ];

  expect(testAtlasGeometry.faces).toBe(expectedFaces);
});
