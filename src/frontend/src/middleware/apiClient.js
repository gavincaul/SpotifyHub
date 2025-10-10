import { useState, useCallback } from "react";
import { apiGateway } from "./apiGateway.js";

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const callApi = useCallback(async (apiCall, ...args) => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiCall(...args);
      return result;
    } catch (err) {
      setError(`[${err.status}]: ${err.message}`);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Methods that accept dynamic config objects
  const get = useCallback(
    (endpoint, config = {}) => callApi(apiGateway.get, endpoint, config),
    [callApi]
  );

  const post = useCallback(
    (endpoint, config = {}) => callApi(apiGateway.post, endpoint, config),
    [callApi]
  );

  const put = useCallback(
    (endpoint, config = {}) => callApi(apiGateway.put, endpoint, config),
    [callApi]
  );

  const delete_ = useCallback(
    (endpoint, config = {}) => callApi(apiGateway.delete, endpoint, config),
    [callApi]
  );

  const request = useCallback(
    (config) => callApi(apiGateway.request, config),
    [callApi]
  );

  return {
    loading,
    error,
    get,
    post,
    put,
    delete: delete_,
    request,
    resetError: () => setError(null),
  };
};
