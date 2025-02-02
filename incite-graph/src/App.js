
import React, { useState, useEffect, useRef } from "react";
import ReactFlow, { Controls, useReactFlow } from "reactflow";
import "reactflow/dist/style.css";
import MermaidGraph from "./MermaidGraph"
import mermaid from "mermaid";
// Sample JSON data
const jsonData = [
  {
    "name": "Deep Learning for NLP",
    "url": "https://example.com/deep-nlp",
    "authors": ["John Doe", "Jane Smith"],
    "keywords": ["deep learning", "NLP", "transformers"],
    "publication_date": "2023-06-15",
    "out_references": ["Attention Mechanisms", "Language Models"],
    "num_out": 2,
    "in_references": [],
    "num_in": 0
  },
  {
    "name": "Attention Mechanisms",
    "url": "https://example.com/attention",
    "authors": ["Alice Brown"],
    "keywords": ["attention", "neural networks"],
    "publication_date": "2021-05-10",
    "out_references": ["Sequence Modelling"],
    "num_out": 1,
    "in_references": ["Deep Learning for NLP"],
    "num_in": 1
  },
  {
    "name": "Language Models",
    "url": "https://example.com/language-models",
    "authors": ["David Green"],
    "keywords": ["NLP", "GPT", "BERT"],
    "publication_date": "2022-11-20",
    "out_references": ["Transformer Networks"],
    "num_out": 1,
    "in_references": ["Deep Learning for NLP"],
    "num_in": 1
  },
  {
    "name": "Transformer Networks",
    "url": "https://example.com/transformers",
    "authors": ["Emily White"],
    "keywords": ["transformers", "self-attention"],
    "publication_date": "2019-12-01",
    "out_references": ["Neural Machine Translation"],
    "num_out": 1,
    "in_references": ["Language Models"],
    "num_in": 1
  },
  {
    "name": "Neural Machine Translation",
    "url": "https://example.com/nmt",
    "authors": ["Sophia Johnson", "Mark Lee"],
    "keywords": ["machine translation", "deep learning"],
    "publication_date": "2018-08-30",
    "out_references": [],
    "num_out": 0,
    "in_references": ["Transformer Networks"],
    "num_in": 1
  },
  {
    "name": "Graph Neural Networks",
    "url": "https://example.com/gnn",
    "authors": ["Chris Brown"],
    "keywords": ["GNN", "graph theory"],
    "publication_date": "2020-04-22",
    "out_references": ["Deep Graph Learning"],
    "num_out": 1,
    "in_references": [],
    "num_in": 0
  },
  {
    "name": "Deep Graph Learning",
    "url": "https://example.com/deep-graph",
    "authors": ["Anna Williams"],
    "keywords": ["graph learning", "deep learning"],
    "publication_date": "2021-09-14",
    "out_references": [],
    "num_out": 0,
    "in_references": ["Graph Neural Networks"],
    "num_in": 1
  },
  {
    "name": "Bayesian Learning Methods",
    "url": "https://example.com/bayesian",
    "authors": ["Robert Wilson"],
    "keywords": ["Bayesian inference", "probability"],
    "publication_date": "2017-07-19",
    "out_references": ["Probabilistic Models"],
    "num_out": 1,
    "in_references": [],
    "num_in": 0
  },
  {
    "name": "Probabilistic Models",
    "url": "https://example.com/probabilistic",
    "authors": ["Laura Martinez"],
    "keywords": ["probability", "statistics", "ML"],
    "publication_date": "2016-11-05",
    "out_references": [],
    "num_out": 0,
    "in_references": ["Bayesian Learning Methods"],
    "num_in": 1
  },
  {
    "name": "Reinforcement Learning",
    "url": "https://example.com/rl",
    "authors": ["Tom Harris"],
    "keywords": ["RL", "Q-learning", "policy gradient"],
    "publication_date": "2019-03-08",
    "out_references": ["Markov Decision Processes"],
    "num_out": 1,
    "in_references": [],
    "num_in": 0
  },
  {
    "name": "Markov Decision Processes",
    "url": "https://example.com/mdp",
    "authors": ["Rachel Adams"],
    "keywords": ["MDP", "decision theory"],
    "publication_date": "2015-02-14",
    "out_references": [],
    "num_out": 0,
    "in_references": ["Reinforcement Learning"],
    "num_in": 1
  },
  {
    "name": "Computer Vision with CNNs",
    "url": "https://example.com/cnn-vision",
    "authors": ["James Carter"],
    "keywords": ["CNN", "computer vision"],
    "publication_date": "2021-10-25",
    "out_references": ["Image Recognition"],
    "num_out": 1,
    "in_references": [],
    "num_in": 0
  },
  {
    "name": "Image Recognition",
    "url": "https://example.com/image-recognition",
    "authors": ["Maria Gonzalez"],
    "keywords": ["image classification", "deep learning"],
    "publication_date": "2020-06-17",
    "out_references": [],
    "num_out": 0,
    "in_references": ["Computer Vision with CNNs"],
    "num_in": 1
  },
  {
    "name": "Ethics in AI",
    "url": "https://example.com/ai-ethics",
    "authors": ["Olivia Thompson"],
    "keywords": ["AI ethics", "bias in AI"],
    "publication_date": "2022-01-09",
    "out_references": ["Fairness in Machine Learning"],
    "num_out": 1,
    "in_references": [],
    "num_in": 0
  },
  {
    "name": "Fairness in Machine Learning",
    "url": "https://example.com/fairness-ml",
    "authors": ["Daniel Wright"],
    "keywords": ["fairness", "machine learning"],
    "publication_date": "2019-12-29",
    "out_references": [],
    "num_out": 0,
    "in_references": ["Ethics in AI"],
    "num_in": 1
  }

];
// Function to generate Mermaid graph definition from JSON data
const generateMermaidGraph = (data) => {
  let mermaidDefinition = "graph TD;\n";

  data.forEach((node) => {
    const sanitizedNodeName = node.name.replace(/[^a-zA-Z0-9]/g, "_"); // Sanitize node names
    node.out_references.forEach((ref) => {
      const sanitizedRef = ref.replace(/[^a-zA-Z0-9]/g, "_"); // Sanitize reference names
      mermaidDefinition += `    ${sanitizedNodeName} --> ${sanitizedRef};\n`;
    });
  });

  return mermaidDefinition;
};

const App = () => {
  const [mermaidGraph, setMermaidGraph] = useState("");
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    const graphDefinition = generateMermaidGraph(jsonData);
    setMermaidGraph(graphDefinition); // Set the generated graph definition
  }, []);

  // Handle node clicks
  const handleNodeClick = (nodeId) => {
    const nodeData = jsonData.find((node) => node.name.replace(/[^a-zA-Z0-9]/g, "_") === nodeId);
    setSelectedNode(nodeData); // Update state with the clicked node's data
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <h1 style={{ textAlign: "center" }}>Mermaid Diagram</h1>
      <div style={{ flex: 1, overflow: "auto" }}>
        <MermaidGraph graphDefinition={mermaidGraph} onNodeClick={handleNodeClick} />
      </div>

      {/* Display selected node data */}
      {selectedNode && (
        <div
          style={{
            position: "fixed",
            right: 0,
            top: 0,
            width: "30%",
            height: "100%",
            backgroundColor: "#f4f4f4",
            padding: "20px",
            boxShadow: "-2px 0 5px rgba(0, 0, 0, 0.1)",
            overflowY: "auto",
          }}
        >
          <h2>Node Details</h2>
          <div>
            <h3>Name: {selectedNode.name}</h3>
            <p><strong>Authors:</strong> {selectedNode.authors.join(", ")}</p>
            <p><strong>Keywords:</strong> {selectedNode.keywords.join(", ")}</p>
            <p><strong>Publication Date:</strong> {selectedNode.publication_date}</p>
            <p><strong>URL:</strong> <a href={selectedNode.url} target="_blank" rel="noopener noreferrer">{selectedNode.url}</a></p>
            <p><strong>Out References:</strong> {selectedNode.out_references.join(", ") || "None"}</p>
            <p><strong>In References:</strong> {selectedNode.in_references.join(", ") || "None"}</p>
          </div>
          <button
            onClick={() => setSelectedNode(null)}
            style={{
              marginTop: "20px",
              padding: "10px",
              background: "#ff6347",
              border: "none",
              color: "white",
              cursor: "pointer",
              borderRadius: "5px",
            }}
          >
            Close
          </button>
        </div>
      )}
    </div>
  );
};

export default App;
