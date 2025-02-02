import React, { useState, useEffect, useRef } from 'react';
import ReactFlow, { Controls, Background, useReactFlow } from "reactflow";
import "reactflow/dist/style.css";
// import MermaidGraph from "./MermaidGraph"
// import mermaid from "mermaid";

import './App.css';

function App() {
    const [activeTab, setActiveTab] = useState('home');
    const [inputText, setInputText] = useState('');
    const [displayType, setDisplayType] = useState('cards');
    const [cards, setCards] = useState([]);
    const [error, setError] = useState('');
    const [selectedCard, setSelectedCard] = useState(null);
    const [graph, setGraph] = useState({ nodes: [], edges: [] });
    const [selectedNode, setSelectedNode] = useState(null);
    const [backgroundGradient, setBackgroundGradient] = useState("");
    const [graphDatas, setGraphDatas] = useState([]);

    const toggleFavorite = (cardName) => {
        setCards((prevCards) =>
            prevCards.map((card) =>
                card.name === cardName ? { ...card, isFavorite: !card.isFavorite } : card
            )
        );
    }; 
 
 
    const processInputData = (data) => {
        const inReferencesMap = new Map();
        data.forEach((node) => {
            node.out_references.forEach((ref) => {
                if (!inReferencesMap.has(ref)) {
                    inReferencesMap.set(ref, []);
                }
                inReferencesMap.get(ref).push(node.name);
            });
        });

        const transformedData = data.map((node) => ({
            name: node.name,
            url: node.url,
            authors: node.authors,
            publication_date: node.publication_date,
            out_references: node.out_references,
            num_out: node.num_out,
            in_references: inReferencesMap.get(node.name) || [],
            num_in: inReferencesMap.get(node.name)?.length || 0,
        }));
        return transformedData;
    };

    const generateGraph = (data) => {
        const sortedData = data.sort((a, b) => b.num_out - a.num_out);
        const totalNodes = sortedData.length;
        const radiusStep = 100 + 5 * totalNodes;
        const nodes = sortedData.map((node, index) => {
            const angle = (index/totalNodes) * 2 * Math.PI;
            const radius = radiusStep * Math.min(index, 2);
            const x = 300 + radius * Math.cos(angle);
            const y = 200 + radius * Math.sin(angle);

            return {
                id: node.name,
                data: { label: node.name },
                position: { x, y },
            };
        });

        const edges = data.flatMap((node) =>
            node.out_references.map((ref) => ({
                id: `${node.name}-${ref}`,
                source: node.name,
                target: ref,
                animated: true,
                markerEnd: { type: "arrowclosed" },
            }))
        );

        return { nodes, edges };
    };

    const calculateNodeInfluence = (data) => {
        const maxInReferences = Math.max(...data.map((node) => node.num_in));
        return data.map((node) => ({
            ...node,
            influence: node.num_in / maxInReferences,
        }));
    };

    const generateBackgroundGradient = (nodes) => {
        let gradient = "radial-gradient(circle, ";
            nodes.forEach((node) => {
                if (node.position && node.position.x !== undefined && node.position.y !== undefined) {
                    const { x, y } = node.position;
                    const darkness = 100 - Math.floor(node.influence * 50);
                    gradient += `rgba(0, 0, 0, ${node.influence * 0.3}) ${x}px ${y}px, `;
                } else {
                    console.error("Node missing position:", node);
                }
            });

            gradient = gradient.slice(0, -2) + ")";
        console.log("Final Gradient:", gradient);
        return gradient;
    };

    const isValidCardData = (data) => {
        return (
            data.name &&
            data.url &&
            data.authors &&
            data.content &&
            data.publication_date &&
            data.coi &&
            data.future_research &&
            data.method_issues &&
            data.num_out !== undefined &&
            data.out_references &&
            data.summary
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await fetch('https://legible-locust-innocent.ngrok-free.app/get_graph', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: inputText }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const responseData = await response.json();
            const graphDatas = responseData.graph;
            setGraphDatas(graphDatas);

         const processedData = processInputData(graphDatas);
         const { nodes, edges } = generateGraph(processedData);
         setGraph({ nodes, edges });
         const nodesWithInfluence = calculateNodeInfluence(graphDatas);
         const gradient = generateBackgroundGradient(nodesWithInfluence);
         console.log("Generated Gradient:", gradient);
         setBackgroundGradient(gradient);

           //  if (!isValidCardData(graphData)) {
           //          throw new Error('Invalid JSON structure. Missing required fields.');
           //      }
            console.debug(graphDatas);
            for (let graphDatax in graphDatas) {
                let graphData = graphDatas[graphDatax];
                console.debug(graphData);
                const newCard = {
                    name: graphData.name,
                    url: graphData.url,
                    authors: [graphData.authors],
                    publication_date: graphData.publication_date,
                    out_references: graphData.out_references,
                    num_out: graphData.num_out,
                    summary: graphData.summary,
                    method_issues: graphData.method_issues,
                    coi: graphData.coi,
                    future_research: graphData.future_research,
                };

                setCards([...cards, newCard]);
            }
            setInputText('');
        } catch (err) {
            setError('Invalid JSON format or missing required fields');
            console.error('JSON Parse Error:', err);
        }
    };

    const NodeDetail = ({ node, onClose }) => {
        if (!node) return null;
        return (
            <div className="node-detail-overlay" onClick={onClose}>
            <div className="node-detail-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={onClose}>x</button>
            <h2>{node.name}</h2>
            <div className="detail-section">
            <label>Authors:</label>
            <p>{node.authors}</p>
            </div>
            <div className="detail-section">
            <label>Publication Date:</label>
            <p>{node.publication_date}</p>
            </div>
            <div className="detail-section">
            <label>Summary:</label>
            <p>{node.summary}</p>
            </div>
            <div className="detail-section">
            <label>URL:</label>
            <a href={node.url} target="_blank" rel="noopener noreferrer">
            {node.url}
            </a>
            </div>
            </div>
            </div>
        );
    };

     const handleNodeClick = (event, node) => {
         const nodeData = graphDatas.find((item) => item.name === node.id);
         setSelectedNode(nodeData);
     };
 
     const handleReferenceClick = (referenceName) => {
         const referencedNode = graphDatas.find((item) => item.name === referenceName);
         if (referencedNode) {
             setSelectedNode(referencedNode);
         }
     };
    const CardDetail = ({ card, onClose }) => {
        return (
            <div className="card-detail-overlay" onClick={onClose}>
            <div className="card-detail-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={onClose}>
            ×
            </button>
            <h2>{card.name}</h2>
            <div className="detail-section">
            <label>Authors:</label>
            <p>{card.authors}</p>
            </div>
            <div className="detail-section">
            <label>Publication Date:</label>
            <p>{card.publication_date}</p>
            </div>
            <div className="detail-section">
            <label>Summary:</label>
            <p>{card.summary}</p>
            </div>
            <div className="detail-section">
            <label>URL:</label>
            <a href={card.url} target="_blank" rel="noopener noreferrer">
            {card.url}
            </a>
            </div>
            <div className="detail-section">
            <label>Methodological Issues:</label>
            <p>{card.method_issues}</p>
            </div>
            <div className="detail-section">
            <label>Outgoing References ({card.num_out}):</label>
            <p>{card.out_references.join(', ') || 'None'}</p>
            </div>
            </div>
            </div>
        );
    };

    const favoritesCount = cards.filter(card => card.isFavorite).length;

    return (
        <div className="container">
        <div className="header">
        <h1 className="title">InCite</h1>
        <div className="nav-bar">
        {['home', 'gaps', 'collections'].map((tab) => (
            <button
            key={tab}
            className={`nav-button ${activeTab === tab ? 'active-tab' : ''}`}
            onClick={() => setActiveTab(tab)}
            >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
            {tab === 'collections' && ` (${favoritesCount})`}
            </button>
        ))}
        </div>
        </div>

        {activeTab === 'collections' ? (
            // Collections View
            <div className="card-container">
            {[0, 1].map((colIndex) => (
                <div key={colIndex} className="column">
                {cards
                    .filter(card => card.isFavorite)
                    .filter((_, index) => index % 2 === colIndex)
                    .map((card, index) => (
                        <div
                        key={index}
                        className="card"
                        onClick={() => setSelectedCard(card)}
                        >
                        <div className="card-header">
                        <h3 className="card-title">{card.name}</h3>
                        <button
                        className={`favorite-button ${card.isFavorite ? 'favorited' : ''}`}
                        onClick={(e) => {
                            e.stopPropagation();
                            toggleFavorite(card.name);
                        }}
                        >
                        {card.isFavorite ? '⭐' : '☆'}
                        </button>
                        </div>
                        <div className="card-authors">{card.authors}</div>
                        {/*<div className="card-keywords">{card.keywords.join(', ')}</div>*/}
                        <div className="card-meta">
                        <span>📅 {card.publication_date}</span>
                        <span>🔗 {card.num_out} references</span>
                        </div>
                        </div>
                    ))}
                </div>
            ))}
            </div>
        ) : (
            // Regular View
            <>
            {/* Prompt Input */}
            <form onSubmit={handleSubmit} className="input-container">
            <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter prompt..."
            className="input-field"
            />
            <button type="submit" className="submit-button">
            Submit
            </button>
            </form>
            {error && <div className="error-message">{error}</div>}

            {/* Display Type Selector */}
            <div className="display-selector">
            <button
            className={`display-button ${displayType === 'cards' ? 'active-display' : ''}`}
            onClick={() => setDisplayType('cards')}
            >
            Cards
            </button>
            <button
            className={`display-button ${displayType === 'graph' ? 'active-display' : ''}`}
            onClick={() => setDisplayType('graph')}
            >
            Graph
            </button>
            </div>

            {/* Content Area */}
            {displayType === 'cards' ? (
                <div className="card-container">
                {[0, 1].map((colIndex) => (
                    <div key={colIndex} className="column">
                    {cards
                        .filter((_, index) => index % 2 === colIndex)
                        .map((card, index) => (
                            <div
                            key={index}
                            className="card"
                            onClick={() => setSelectedCard(card)}
                            >
                            <div className="card-header">
                            <h3 className="card-title">{card.name}</h3>
                            <button
                            className={`favorite-button ${card.isFavorite ? 'favorited' : ''}`}
                            onClick={(e) => {
                                e.stopPropagation();
                                toggleFavorite(card.name);
                            }}
                            >
                            {card.isFavorite ? '⭐' : '☆'}
                            </button>
                            </div>
                            <div className="card-authors">{card.authors}</div>
                            {/* <div className="card-content">{card.content.join(', ')}</div>*/}
                            <div className="card-meta">
                            <span>📅 {card.publication_date}</span>
                            <span>🔗 {card.num_out} references</span>
                            </div>
                            </div>
                        ))}
                    </div>
                ))}
                </div>
            ) : (
                <div className="graph-container">
                <ReactFlow
                nodes = {graph.nodes}
                edges = {graph.edges}
                onNodeClick={handleNodeClick}
                fitView
                >
                <Background/>
                <Controls/>
                </ReactFlow>
                </div>
            )}
            </>
        )}

        {/* Card Detail Overlay */}
        {selectedCard && (
            <CardDetail card={selectedCard} onClose={() => setSelectedCard(null)} />
        )}

        {selectedNode && (
            <NodeDetail node={selectedNode} onClose={() => setSelectedNode(null)} />
        )}
        </div>
    );
}

export default App;
