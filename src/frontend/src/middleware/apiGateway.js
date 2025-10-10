class APIGateway {
  constructor(baseURL = "http://localhost:4000") {
    this.baseURL = baseURL;
    this.middlewares = [];
    this.setupDefaultMiddlewares();
  }

  use = (middleware) => {
    this.middlewares.push(middleware);
  };

  setupDefaultMiddlewares = () => {
    this.use(this.loggingMiddleware);
    this.use(this.errorHandlingMiddleware);
    this.use(this.authMiddleware);
  };

  // Default Middlewares
  loggingMiddleware = async (requestConfig, next) => {
    const { url, method = "GET" } = requestConfig;
    console.log(`🚀 API Request: ${method} ${url}`);
    const startTime = Date.now();

    try {
      const result = await next(requestConfig);
      const duration = Date.now() - startTime;
      console.log(`✅ API Response: ${url} (${duration}ms)`, result);
      return result;
    } catch (error) {
      const duration = Date.now() - startTime;
      console.error(`❌ API Error: ${url} (${duration}ms)`, error);
      throw error;
    }
  };

  errorHandlingMiddleware = async (requestConfig, next) => {
    const response = await next(requestConfig);
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}`;
      let errorPayload = null;

      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorData.message || errorMessage;
        errorPayload = errorData;
      } catch {
        errorMessage = response.statusText || errorMessage;
      }

      const error = new Error(errorMessage);
      error.status = response.status;
      error.statusText = response.statusText;

      error.payload = errorPayload;
      if (
        errorMessage.includes("authentication expired") ||
        errorMessage.includes("not logged in")
      ) {
        window.dispatchEvent(
          new CustomEvent("spotifyAuthError", {
            detail: {
              isAuthError: true, // Add this property
              message: errorMessage,
            },
          })
        );
      }
      throw error;
    }

    return response;
  };

  authMiddleware = async (requestConfig, next) => {
    const token = localStorage.getItem("auth_token");
    if (token) {
      requestConfig.headers = {
        ...requestConfig.headers,
        Authorization: `Bearer ${token}`,
      };
    }
    return next(requestConfig);
  };

  // Main request handler with dynamic config
  request = async (requestConfig) => {
    const {
      endpoint,
      method = "GET",
      pathParams = [],
      queryParams = {},
      body,
      headers = {},
      ...otherOptions
    } = requestConfig;
    // Build URL dynamically
    let url = `${this.baseURL}${endpoint}`;

    // Add path parameters
    if (pathParams && pathParams.length > 0) {
      // If endpoint already has path parameters, append them properly
      if (!url.endsWith("/")) {
        url += "/";
      }
      url += pathParams.join("/");
    }

    // Add query parameters
    const queryString = new URLSearchParams();
    Object.entries(queryParams).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        if (Array.isArray(value)) {
          value.forEach((v) => queryString.append(key, v));
        } else if (typeof value === "boolean") {
          queryString.append(key, value.toString());
        } else {
          queryString.append(key, value);
        }
      }
    });

    const queryStringResult = queryString.toString();
    if (queryStringResult) {
      url += `?${queryStringResult}`;
    }

    // Build final fetch config
    const config = {
      method,
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
      ...otherOptions,
    };

    // Add body for methods that support it
    if (body && ["POST", "PUT", "PATCH"].includes(method)) {
      // If body is FormData, send it as-is (browser sets Content-Type automatically)

      if (body instanceof FormData) {
        console.log("File detected, using FormData");
        config.body = body;
        delete config.headers["Content-Type"]; // Let browser set multipart/form-data boundary
      } else {
        config.body = JSON.stringify(body);
      }
    }
    const finalRequestConfig = { url, ...config };

    // Execute middleware chain
    const executeMiddleware = async (index, reqConfig) => {
      if (index >= this.middlewares.length) {
        return fetch(reqConfig.url, reqConfig);
      }

      const middleware = this.middlewares[index];
      return middleware(reqConfig, (nextConfig) =>
        executeMiddleware(index + 1, { ...reqConfig, ...nextConfig })
      );
    };

    const response = await executeMiddleware(0, finalRequestConfig);

    if (response.headers.get("content-type")?.includes("application/json")) {
      return await response.json();
    }

    return await response.text();
  };

  // Convenience methods with dynamic config
  get = async (endpoint, config = {}) => {
    return this.request({ endpoint, method: "GET", ...config });
  };

  post = async (endpoint, config = {}) => {
    return this.request({ endpoint, method: "POST", ...config });
  };

  put = async (endpoint, config = {}) => {
    return this.request({ endpoint, method: "PUT", ...config });
  };

  delete = async (endpoint, config = {}) => {
    return this.request({ endpoint, method: "DELETE", ...config });
  };
}

export const apiGateway = new APIGateway();
