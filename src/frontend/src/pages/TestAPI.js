import React, { useState } from "react";
import { useApi } from "../middleware/apiClient.js";
import { stripURL } from "../utils/utils.js";
import Header from "../components/Header.tsx";

const TestAPI = () => {
  // scalable query parameters
  // eslint-disable-next-line no-unused-vars
  const {
    loading,
    error,
    // eslint-disable-next-line
    get,
    // eslint-disable-next-line
    put,
    // eslint-disable-next-line
    delete: delete_,
    // eslint-disable-next-line
    post,
    resetError,
  } = useApi();
  const MAX_LIST_ITEMS = 6;

  const [params, setParams] = useState({
    //raw: { type: "boolean", value: false },
    //total: { type: "number", value: 10 },
    //file: { type: "file", value: null },
    //image_url: { type: "string", value: "" },
    //track_id: { type: "string", value: "" },
    //a1: { type: "string", value: "" },
    //a2: { type: "string", value: "" },
    //position: { type: "number", value: "" },
    /*artists: {
      type: "list",
      value: Array(MAX_LIST_ITEMS).fill(""),
      subtype: "string", // "number" | "string" | "boolean"
    },
    /*time_range: {
      type: "dropdown",
      value: "short_term",
      options: [
        "short_term: (4 weeks)",
        "medium_term: (6 months)",
        "long_term: (~ 1 year)",
      ],
    },*/
    /*search_type: {
      type: "dropdown",
      value: "track",
      options: ["track", "album", "artist", "playlist"],
    },*/
  });

  let curr_url =
    "https://open.spotify.com/track/4j4pPKE3xAblPIbhxScC1j?si=22418374f24649ab";
  let input_count = 0;
  let APICall = "/me/library";
  let APIMethod = get;
  let letbody = false;

  const [inputs, setInputs] = useState(Array(input_count).fill(""));

  const [response, setResponse] = useState("");

  const handleInputChange = (index, value) => {
    const newInputs = [...inputs];
    newInputs[index] = value;
    setInputs(newInputs);
  };
  const handleListItemChange = (paramKey, idx, val) => {
    setParams((prev) => {
      const old = prev[paramKey] || { type: "list", value: [] };
      const newArr = [...(old.value || [])];
      newArr[idx] = val;
      return { ...prev, [paramKey]: { ...old, value: newArr } };
    });
  };

  const handleClick = async () => {
    const cleanedInputs = inputs.map((input) => stripURL(input));
    // This validation doesn't make sense with your current setup
    for (let i = 0; i < input_count; i++) {
      if (!cleanedInputs[i]) {
        setResponse(`Please enter input ${i + 1}`);
        return;
      }
    }

    try {
      let body = null;
      let headers = {};
      let data = null;

      // file upload case (FormData)
      if (params.file && params.file.value) {
        body = new FormData();
        body.append("image", params.file.value);

        Object.entries(params).forEach(([key, meta]) => {
          if (key === "file") return;
          if (meta.type === "boolean" && meta.value) body.append(key, true);
          else if (meta.type === "number" && !isNaN(meta.value))
            body.append(key, meta.value);
          else if (meta.type === "string" && meta.value?.trim() !== "")
            body.append(key, stripURL(meta.value.trim()));
          else if (meta.type === "dropdown" && meta.value)
            body.append(key, meta.value.split(":")[0].trim());
          else if (meta.type === "list" && Array.isArray(meta.value)) {
            const arr =
              meta.subtype === "number"
                ? meta.value
                    .filter((it) => {
                      // Skip blanks, nulls, undefined
                      if (it === "" || it === undefined || it === null)
                        return false;
                      // If it's supposed to be a number but not a valid number, skip
                      if (meta.subtype === "number" && isNaN(Number(it)))
                        return false;
                      return true;
                    })
                    .map((it) => (meta.subtype === "number" ? Number(it) : it))
                : meta.value.filter((it) => it != null && it !== "");
            if (arr.length > 0) {
              if (params.file && params.file.value)
                body.append(key, JSON.stringify(arr));
              else body[key] = arr;
            }
          }
        });
      } else if (params.image_url && params.image_url.value) {
        // URL case: send JSON body with "url" field
        body = { url: params.image_url?.value.trim() };
        headers["Content-Type"] = "application/json";
      } else {
        // No file: plain object body (or queryParams)
        body = {};
        Object.entries(params).forEach(([key, meta]) => {
          if (meta.type === "boolean" && meta.value) body[key] = true;
          else if (meta.type === "number" && !isNaN(meta.value))
            body[key] = meta.value === "" ? undefined : Number(meta.value);
          else if (meta.type === "string" && meta.value?.trim() !== "")
            body[key] = stripURL(meta.value.trim());
          else if (meta.type === "dropdown" && meta.value)
            body[key] = meta.value.split(":")[0].trim();
          else if (meta.type === "list" && Array.isArray(meta.value)) {
            const arr =
              meta.subtype === "number"
                ? meta.value
                    .filter((it) => {
                      // Skip blanks, nulls, undefined
                      if (it === "" || it === undefined || it === null)
                        return false;
                      // If it's supposed to be a number but not a valid number, skip
                      if (meta.subtype === "number" && isNaN(Number(it)))
                        return false;
                      return true;
                    })
                    .map((it) => (meta.subtype === "number" ? Number(it) : it))
                : meta.value.filter((it) => it != null && it !== "");

            if (arr.length > 0) {
              if (params.file && params.file.value)
                body.append(key, JSON.stringify(arr));
              else body[key] = arr;
            }
          }
        });
      }

      const callArgs = {
        pathParams: cleanedInputs.filter((input) => input.trim() !== ""),
        headers,
      };

      if (
        (params.file && params.file.value) ||
        (params.image_url && params.image_url.value) ||
        letbody
      )
        callArgs.body = body;
      else callArgs.queryParams = body;

      data = await APIMethod(APICall, callArgs);

      console.log("Received response:", data);
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error("Request failed:", err);
      setResponse("Error: " + err.message);
    }
  };

  return (
    <div className="app-container">
      <Header />
      <div style={{ padding: "20px", fontFamily: "Arial" }}>
        <h2>Test API</h2>

        {/* input_count inputs (none by default) */}
        {input_count > 0 &&
          inputs.map((value, index) => (
            <input
              key={index}
              type="text"
              placeholder={`Album ID`}
              value={value}
              onChange={(e) => handleInputChange(index, e.target.value)}
              style={{ marginRight: "10px", marginBottom: "5px" }}
            />
          ))}

        {/* params rendering */}
        <div>
          {Object.entries(params).map(([key, meta]) => {
            if (meta.type === "boolean") {
              return (
                <label key={key} style={{ marginRight: "10px" }}>
                  <input
                    type="checkbox"
                    checked={meta.value}
                    onChange={(e) =>
                      setParams({
                        ...params,
                        [key]: { ...meta, value: e.target.checked },
                      })
                    }
                  />
                  {key}
                </label>
              );
            } else if (meta.type === "file") {
              return (
                <label key={key} style={{ marginRight: "10px" }}>
                  {key}:
                  <input
                    type="file"
                    onChange={(e) =>
                      setParams({
                        ...params,
                        [key]: { ...meta, value: e.target.files[0] },
                      })
                    }
                    style={{ marginLeft: "5px" }}
                  />
                </label>
              );
            } else if (meta.type === "number") {
              return (
                <label key={key} style={{ marginRight: "10px" }}>
                  {key}:
                  <input
                    type="number"
                    value={meta.value}
                    onChange={(e) =>
                      setParams({
                        ...params,
                        [key]: { ...meta, value: Number(e.target.value) },
                      })
                    }
                    style={{ marginLeft: "5px" }}
                  />
                </label>
              );
            } else if (meta.type === "string") {
              return (
                <label key={key} style={{ marginRight: "10px" }}>
                  {key}:
                  <input
                    type="text"
                    value={meta.value}
                    onChange={(e) =>
                      setParams({
                        ...params,
                        [key]: { ...meta, value: e.target.value },
                      })
                    }
                    style={{ marginLeft: "5px" }}
                  />
                </label>
              );
            } else if (meta.type === "dropdown") {
              return (
                <label key={key} style={{ marginRight: "10px" }}>
                  {key}:
                  <select
                    value={meta.value}
                    onChange={(e) =>
                      setParams({
                        ...params,
                        [key]: { ...meta, value: e.target.value },
                      })
                    }
                    style={{ marginLeft: "5px" }}
                  >
                    {meta.options?.map((opt) => (
                      <option key={opt} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>
                </label>
              );
            } else if (meta.type === "list") {
              // render MAX_LIST_ITEMS fixed inputs only
              return (
                <div key={key} style={{ marginTop: "12px" }}>
                  <div style={{ marginBottom: "6px" }}>
                    <strong>{key}</strong> (up to {MAX_LIST_ITEMS} values)
                  </div>

                  <div
                    style={{
                      display: "flex",
                      gap: "8px",
                      flexWrap: "wrap",
                      marginBottom: "8px",
                    }}
                  >
                    {meta.value.map((val, idx) => (
                      <input
                        key={idx}
                        type="text"
                        placeholder={`${meta.subtype} ${idx + 1}`}
                        value={val}
                        onChange={(e) =>
                          handleListItemChange(key, idx, e.target.value)
                        }
                        style={{ width: "120px", padding: "6px" }}
                      />
                    ))}
                  </div>

                  <button
                    onClick={() =>
                      setParams((prev) => ({
                        ...prev,
                        [key]: {
                          ...meta,
                          value: Array(MAX_LIST_ITEMS).fill(""),
                        },
                      }))
                    }
                  >
                    Clear
                  </button>
                </div>
              );
            }

            return null;
          })}
        </div>

        <button
          onClick={handleClick}
          style={{ marginTop: "10px" }}
          disabled={loading}
        >
          {loading ? "Loading..." : "Fetch"}
        </button>

        {error && (
          <div style={{ color: "red", marginTop: "10px" }}>
            Error: {error} <button onClick={resetError}>Reset</button>
          </div>
        )}

        <pre
          style={{
            marginTop: "20px",
            padding: "10px",
            backgroundColor: "#f0f0f0",
            whiteSpace: "pre-wrap",
          }}
        >
          {response}
        </pre>
        <div>{curr_url}</div>
      </div>
    </div>
  );
};

export default TestAPI;
