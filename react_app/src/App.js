import React from 'react';
import EmbeddingForm from './Form';
import styles from './App.scss';

const items = [
  {
    index: 0,
    title: "Model",
    values: ["DeLF"]
  },
  {
    index: 1,
    title: "Visualizer",
    values: ["t-SNE"]
  },
  {
    index: 2,
    title: "Dataset",
    values: ["Dataset 1", "Dataset 2"]
  }
];

export default function App() {
  return (
    <div className="App">
      <EmbeddingForm menuItems={items} />
    </div>
  );
}
