import React, { useMemo, useState } from "react";
import "./FunctionItems.css";
import SourceInput from "./SourceInput.tsx";

// Lightweight, flexible function items system for per-page tools
// Keep types permissive for this mixed TS/JS codebase.

export type FunctionField = {
  name: string;
  label: string;
  type?: "text" | "number" | "toggle" | "select" | "source";
  placeholder?: string;
  options?: Array<{ label: string; value: any }>;
  defaultValue?: any;
  accept?: 'playlist' | 'track' | 'album' | 'any';
};

export type FunctionItem = {
  id: string;
  title: string;
  description?: string;
  fields?: FunctionField[];
  run: (values: Record<string, any>) => Promise<any> | any;
  danger?: boolean;
  disabled?: boolean;
  ctaLabel?: string;
};

export type FunctionGroup = {
  group: string;
  items: FunctionItem[];
};

export type FunctionListProps = {
  items?: FunctionItem[]; // flat list (backwards compatible)
  groups?: FunctionGroup[]; // grouped rendering
  onResult?: (id: string, result: any) => void;
  className?: string;
  style?: any;
};

function useInitialValues(fields?: FunctionField[]) {
  return useMemo(() => {
    const init: Record<string, any> = {};
    (fields || []).forEach((f) => {
      if (typeof f.defaultValue !== "undefined") init[f.name] = f.defaultValue;
      else init[f.name] = f.type === "toggle" ? false : "";
    });
    return init;
  }, [fields]);
}

function FunctionItemCard({ item, onResult }: { item: FunctionItem; onResult?: (id: string, result: any) => void }) {
  const { id, title, description, fields, run, danger, disabled, ctaLabel } = item;
  const [values, setValues] = useState(useInitialValues(fields));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");

  const setField = (name: string, v: any) => setValues((prev) => ({ ...prev, [name]: v }));

  const onSubmit = async (e?: any) => {
    e?.preventDefault?.();
    setLoading(true);
    setError("");
    setOk("");
    try {
      const res = await run(values);
      setOk("Done");
      onResult?.(id, res);
    } catch (err: any) {
      console.error("Function item error", err);
      setError(err?.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={"fi-card" + (danger ? " fi-danger" : "") + (disabled ? " fi-disabled" : "") }>
      <div className="fi-head">
        <div className="fi-title">{title}</div>
        {description ? <div className="fi-desc">{description}</div> : null}
      </div>
      {!!(fields && fields.length) && (
        <form className="fi-form" onSubmit={onSubmit}>
          {fields.map((f) => (
            <div className="fi-field" key={f.name}>
              <label className="fi-label" htmlFor={`${id}-${f.name}`}>{f.label}</label>
              {(() => {
                const commonProps: any = {
                  id: `${id}-${f.name}`,
                  disabled: disabled || loading,
                };
                switch (f.type) {
                  case "number":
                    return (
                      <input
                        {...commonProps}
                        type="number"
                        className="fi-input"
                        placeholder={f.placeholder}
                        value={values[f.name] ?? ""}
                        onChange={(e) => setField(f.name, e.target.valueAsNumber)}
                      />
                    );
                  case "toggle":
                    return (
                      <label className="fi-toggle">
                        <input
                          {...commonProps}
                          type="checkbox"
                          checked={!!values[f.name]}
                          onChange={(e) => setField(f.name, e.target.checked)}
                        />
                        <span className="fi-toggle-slider" />
                      </label>
                    );
                  case "select":
                    return (
                      <select
                        {...commonProps}
                        className="fi-input"
                        value={values[f.name] ?? (f.options && f.options[0] ? f.options[0].value : "")}
                        onChange={(e) => setField(f.name, e.target.value)}
                      >
                        {(f.options || []).map((opt, i) => (
                          <option key={i} value={opt.value}>
                            {opt.label}
                          </option>
                        ))}
                      </select>
                    );
                  case "source":
                    return (
                      <SourceInput
                        value={values[f.name] ?? ""}
                        onChange={(val) => setField(f.name, val)}
                        placeholder={f.placeholder}
                        accept={f.accept || 'any'}
                        onDropAccepted={(data) => {
                          if (typeof data === 'object' && data.id) {
                            setField(f.name, data.id);
                          } else if (typeof data === 'string') {
                            setField(f.name, data);
                          }
                        }}
                      />
                    );
                  case "text":
                  default:
                    return (
                      <input
                        {...commonProps}
                        type="text"
                        className="fi-input"
                        placeholder={f.placeholder}
                        value={values[f.name] ?? ""}
                        onChange={(e) => setField(f.name, e.target.value)}
                      />
                    );
                }
              })()}
            </div>
          ))}
        </form>
      )}
      <div className="fi-actions">
        <button
          type="button"
          className={"fi-btn " + (danger ? "fi-btn-danger" : "fi-btn-primary")}
          disabled={disabled || loading}
          onClick={onSubmit}
        >
          {loading ? "Running..." : (ctaLabel || "Run")}
        </button>
        {error ? <div className="fi-status fi-error">{error}</div> : null}
        {ok ? <div className="fi-status fi-ok">{ok}</div> : null}
      </div>
    </div>
  );
}

export default function FunctionList({ items, groups, onResult, className = "", style }: FunctionListProps) {
  const flatItems = useMemo(() => items || ([] as FunctionItem[]), [items]);
  const grouped = useMemo(() => groups || (flatItems.length ? [{ group: "", items: flatItems }] : []), [groups, flatItems]);
  const [activeId, setActiveId] = useState(null);

  const closeActive = () => setActiveId(null);

  return (
    <div className={"fi-wrap " + className} style={style}>
      {activeId && (
        <div className="fi-expanded-block">
          {(() => {
            const item = grouped.flatMap((g) => g.items).find((i) => i.id === activeId);
            if (!item) return null;
            return (
              <>
                <div className="fi-inline-bar">
                  <div className="fi-inline-title">{item.title}</div>
                  <button className="fi-close" onClick={closeActive} aria-label="Close function">×</button>
                </div>
                <div className="fi-collapsible fi-collapsible--open">
                  <FunctionItemCard item={item} onResult={(id, res) => { onResult?.(id, res); }} />
                </div>
              </>
            );
          })()}
        </div>
      )}

      <div className="fi-groups">
        {grouped.map((g, gi) => (
          <div key={g.group + gi} className="fi-group">
            {g.group ? <div className="fi-group-title">— {g.group} —</div> : null}
            <div className="fi-tile-grid">
              {g.items.map((item) => (
                <button
                  key={item.id}
                  className="fi-tile"
                  onClick={() => setActiveId(item.id)}
                >
                  <div className="fi-tile-title">{item.title}</div>
                  {item.description ? (
                    <div className="fi-tile-desc">{item.description}</div>
                  ) : null}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
