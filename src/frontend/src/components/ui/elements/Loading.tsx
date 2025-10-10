// src/components/ui/Loading.tsx
import React from "react";
import "./Loading.css";

type LoadingProps = {
  message?: string;
};
export default function Loading({ message = "Loading..." }: LoadingProps) {
  return (
    <div className="loading-overlay">
      <div className="lds-ring">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
      <p>{message}</p>
    </div>
  );
}
