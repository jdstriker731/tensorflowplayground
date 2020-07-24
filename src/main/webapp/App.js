import React from "react";
import EmbeddingForm from "./Form";
import "./styles.scss";

const DATASET_CREATE_STRING = "Create a dataset";
const items = [
  {
    index: 0,
    title: "Model",
    values: ["DeLF", "other"]
  },
  {
    index: 1,
    title: "Visualizer",
    values: ["t-SNE", "PCA"]
  },
  {
    index: 2,
    title: "Dataset",
    values: ["Dataset 1", "Dataset 2", DATASET_CREATE_STRING]
  }
];

export default function App() {
  return (
    <div className="App">
      <EmbeddingForm items={items} />
    </div>
  );
}
