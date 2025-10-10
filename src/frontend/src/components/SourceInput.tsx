import React, { useRef, useState, useCallback } from 'react';
import './SourceInput.css';

type SourceType = 'playlist' | 'track' | 'album' | 'any';

interface SourceInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
  /**
   * The type of source this input accepts
   * @default 'any'
   */
  accept?: SourceType;
  /**
   * Whether to show a clear button
   * @default true
   */
  clearable?: boolean;
  /**
   * Callback when a valid drop occurs
   */
  onDropAccepted?: (data: any) => void;
  /**
   * Callback when an invalid drop is attempted
   */
  onDropRejected?: (data: any) => void;
}

export default function SourceInput({
  value,
  onChange,
  placeholder = 'Enter or drop a source here',
  className = '',
  accept = 'any',
  clearable = true,
  onDropAccepted,
  onDropRejected,
}: SourceInputProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);

    // Try to get JSON data first
    try {
      const jsonData = e.dataTransfer.getData('application/json');
      if (jsonData) {
        const data = JSON.parse(jsonData);
        if (accept === 'any' || data.type === accept) {
          onChange(data.id);
          onDropAccepted?.(data);
          return;
        } else {
          onDropRejected?.(data);
          return;
        }
      }
    } catch (error) {
      // If JSON parsing fails, try text/plain
      const textData = e.dataTransfer.getData('text/plain');
      if (textData) {
        onChange(textData);
        onDropAccepted?.(textData);
        return;
      }
    }

    onDropRejected?.(null);
  }, [accept, onChange, onDropAccepted, onDropRejected]);

  const handleClear = useCallback(() => {
    onChange('');
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, [onChange]);

  return (
    <div 
      className={`source-input-container ${isDragOver ? 'drag-over' : ''} ${className}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <input
        ref={inputRef}
        type="text"
        className="source-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
      {clearable && value && (
        <button 
          type="button" 
          className="clear-button"
          onClick={handleClear}
          aria-label="Clear input"
        >
          ✕
        </button>
      )}
      {isDragOver && (
        <div className="drop-hint">
          Drop {accept === 'any' ? 'source' : accept} here
        </div>
      )}
    </div>
  );
}
