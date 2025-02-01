import React, { useEffect, useRef, useState } from "react";
import mermaid from "mermaid";

const MermaidGraph = ({ graphDefinition }) => {
  const graphContainerRef = useRef(null);

  useEffect(() => {
    // Initialize Mermaid and render the graph
    mermaid.initialize({ startOnLoad: true });

    // Ensure Mermaid processes the content
    if (graphContainerRef.current) {
      mermaid.contentLoaded();
    }
  }, [graphDefinition]);

  return (
    <div
      ref={graphContainerRef}
      className="mermaid"
      style={{ width: "100%", height: "100%" }}
    >
      {graphDefinition}
    </div>
  );
};

export default MermaidGraph;
