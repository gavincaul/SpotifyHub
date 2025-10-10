import { apiGateway } from "../middleware/apiGateway.js";

export const BaseAPI = {
  get: (endpoint, config) => apiGateway.get(endpoint, config),
  post: (endpoint, config) => apiGateway.post(endpoint, config),
  put: (endpoint, config) => apiGateway.put(endpoint, config),
  delete: (endpoint, config) => apiGateway.delete(endpoint, config),
};