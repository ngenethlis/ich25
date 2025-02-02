import React, { useEffect, useRef } from "react";
import mermaid from "mermaid";

const MermaidGraph = ({ graphDefinition }) => {
  const graphRef = useRef(null);

  useEffect(() => {
    if (graphRef.current && graphDefinition) {
      // Initialize Mermaid
      mermaid.initialize({ startOnLoad: true });

      // Render the graph
      mermaid.contentLoaded();
    }
  }, [graphDefinition]);

  return (
    <div ref={graphRef} className="mermaid">
      {graphDefinition}
    </div>
  );
};

export default MermaidGraph;
