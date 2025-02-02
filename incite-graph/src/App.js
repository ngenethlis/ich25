
import React, { useState, useEffect, useRef } from "react";
import ReactFlow, { Controls, Background, useReactFlow } from "reactflow";
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
// Convert JSON to React Flow nodes & edges
const generateGraph = (data) => {
  const sortedData = data.sort((a, b) => b.num_out - a.num_out);
  const radiusStep = 150;
  const totalNodes = sortedData.length;

  const nodes = sortedData.map((node, index) => {
    const angle = (index / totalNodes) * 2 * Math.PI;
    const radius = radiusStep * Math.min(index, 2);
    const x = 300 + radius * Math.cos(angle);
    const y = 200 + radius * Math.sin(angle);

    return {
      id: node.name,
      data: { label: node.name },
      position: { x, y }, // Ensure position is defined
    };
  });

  const edges = data.flatMap((node) =>
    node.out_references.map((ref) => ({
      id: `${node.name}-${ref}`,
      source: node.name,
      target: ref,
      animated: true,
      markerEnd: { type: "arrowclosed" }, // Add arrowhead to the edge
    }))
  );

  return { nodes, edges };
};// Calculate node influence based on incoming references
const calculateNodeInfluence = (data) => {
  const maxInReferences = Math.max(...data.map((node) => node.num_in));
  return data.map((node) => ({
    ...node,
    influence: node.num_in / maxInReferences, // Normalize influence to [0, 1]
  }));
};

// Generate CSS gradient based on node positions and influence
const generateBackgroundGradient = (nodes) => {
  let gradient = "radial-gradient(circle, ";

  nodes.forEach((node) => {
    if (node.position && node.position.x !== undefined && node.position.y !== undefined) {
      const { x, y } = node.position;
      const darkness = 100 - Math.floor(node.influence * 50); // Darker for higher influence
      gradient += `rgba(0, 0, 0, ${node.influence * 0.3}) ${x}px ${y}px, `;
    } else {
      console.error("Node missing position:", node);
    }
  });

  gradient = gradient.slice(0, -2) + ")"; // Remove trailing comma and close gradient

  console.log("Final Gradient:", gradient); // Log the final gradient
  return gradient;
};

const App = () => {
  const [graph, setGraph] = useState({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState(null);
  const [backgroundGradient, setBackgroundGradient] = useState("");

  useEffect(() => {
    const { nodes, edges } = generateGraph(jsonData);
    setGraph({ nodes, edges });

    // Calculate node influence and generate background gradient
    const nodesWithInfluence = calculateNodeInfluence(jsonData);
    const gradient = generateBackgroundGradient(nodesWithInfluence);
    console.log("Generated Gradient:", gradient); // Log the gradient
    setBackgroundGradient(gradient);
  }, []);

  // Handle node clicks
  const handleNodeClick = (event, node) => {
    const nodeData = jsonData.find((item) => item.name === node.id);
    setSelectedNode(nodeData); // Update state with the clicked node's data
  };

  return (
    <div style={{ display: "flex", height: "100vh", flexDirection: "row" }}>
      {/* React Flow container */}
      <div
        style={{
          flex: 1,
          position: "relative",
          background: backgroundGradient || "white", // Fallback to white if gradient is empty
        }}
      >
        <h1 style={{ textAlign: "center" }}>Interactive Graph</h1>
        <ReactFlow
          nodes={graph.nodes}
          edges={graph.edges}
          onNodeClick={handleNodeClick} // Attach click handler
        >
          <Controls position="top-left" /> {/* Add controls */}
          <Background /> {/* Add a background */}
        </ReactFlow>
      </div>      {/* Sidebar to display the selected node's data */}
      {selectedNode && (
        <div
          style={{
            width: "30%",
            backgroundColor: "#f4f4f4",
            padding: "20px",
            position: "absolute",
            right: 0,
            top: 0,
            height: "100%",
            overflowY: "auto",
            boxShadow: "-2px 0 5px rgba(0, 0, 0, 0.1)",
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
              color: "plum",
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
