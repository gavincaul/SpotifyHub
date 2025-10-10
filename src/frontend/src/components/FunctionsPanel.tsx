import React from "react";
import "./FunctionsPanel.css";

export type FunctionsPanelProps = {
  title?: string;
  headerRight?: any;
  stickyHeader?: boolean;
  children?: any;
  className?: string;
  style?: any;
};

export default function FunctionsPanel({
  title = "Functions",
  headerRight,
  stickyHeader = true,
  children,
  className = "",
  style,
}: FunctionsPanelProps) {
  return (
    <div className={"fp-wrap " + className} style={style}>
      <div className={"fp-header" + (stickyHeader ? " fp-header--sticky" : "") }>
        <div className="fp-title">{title}</div>
        {headerRight ? <div className="fp-header-right">{headerRight}</div> : null}
      </div>
      <div className="fp-body">{children}</div>
    </div>
  );
}
