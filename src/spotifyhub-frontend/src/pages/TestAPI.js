import React, { useState } from "react";
import { useApi } from "../middleware/apiClient.js";
import { stripURL } from "../middleware/utils.js";

const TestAPI = () => {
  // scalable query parameters
  const [params, setParams] = useState({

  });
  let input_count = 1;
  let APICall = "/artist/genres";



  const [inputs, setInputs] = useState(Array(input_count).fill(""));

  const { loading, error, get, resetError } = useApi();
  const [response, setResponse] = useState("");

  const paramNames = Object.keys(params);

  const handleInputChange = (index, value) => {
    const newInputs = [...inputs];
    newInputs[index] = value;
    setInputs(newInputs);
  };

  const handleParamChange = (param, value) => {
    setParams({ ...params, [param]: value });
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
    console.log(cleanedInputs);

    try {
      // You're building queryParams but not using them
      const queryParams = {};
      Object.entries(params).forEach(([key, value]) => {
        if (value) queryParams[key] = true;
      });

      // Use the actual inputs for pathParams
      const data = await get(APICall, {
        pathParams: cleanedInputs.filter((input) => input.trim() !== ""),
        queryParams: queryParams,
      });

      console.log("Received response:", data);
      setResponse(JSON.stringify(data, null, 2));
    } catch (err) {
      console.error("Request failed:", err);
      setResponse("Error: " + err.message);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Test API</h2>

      {/* Input for album_id */}
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

      {/* Checkbox query params */}
      <div>
        {paramNames.map((param) => (
          <label key={param} style={{ marginRight: "10px" }}>
            <input
              type="checkbox"
              checked={params[param]}
              onChange={(e) => handleParamChange(param, e.target.checked)}
            />
            {param.charAt(0).toUpperCase() + param.slice(1)}
          </label>
        ))}
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
      <div>
https://open.spotify.com/artist/5Z3IWpvwOvoaWodujHw7xh?si=468645aeb12b44ff      </div>
    </div>
  );
};

export default TestAPI;
