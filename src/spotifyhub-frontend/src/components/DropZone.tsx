import React, { useCallback, useState } from "react";
import "./DropZone.css";

export type DropZoneProps = {
  onDropData?: (data: any, raw: DataTransfer) => void;
  className?: string;
  style?: React.CSSProperties;
  children?: React.ReactNode; // custom inner content
  placeholder?: React.ReactNode; // shown when no children
};

function parseDataTransfer(dt: DataTransfer) {
  // Try common types in order of richness
  // 1) application/json
  try {
    const json = dt.getData("application/json");
    if (json) return JSON.parse(json);
  } catch {}

  // 2) text/plain
  const text = dt.getData("text/plain");
  if (text) {
    try { return JSON.parse(text); } catch {}
    return text;
  }

  // 3) text/uri-list
  const uri = dt.getData("text/uri-list");
  if (uri) return { uri };

  return null;
}

export default function DropZone({ onDropData, className = "", style, children, placeholder }: DropZoneProps) {
  const [over, setOver] = useState(false);

  const onDragEnter = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setOver(true);
  }, []);

  const onDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "copy";
    setOver(true);
  }, []);

  const onDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setOver(false);
  }, []);

  const onDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setOver(false);
    const payload = parseDataTransfer(e.dataTransfer);
    onDropData?.(payload, e.dataTransfer);
  }, [onDropData]);

  return (
    <div
      className={"dz " + (over ? "dz-over " : "") + className}
      style={style}
      onDragEnter={onDragEnter}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
      role="button"
      tabIndex={0}
    >
      <div className="dz-inner">
        {children || placeholder || <span className="dz-placeholder">Drop here</span>}
      </div>
    </div>
  );
}
