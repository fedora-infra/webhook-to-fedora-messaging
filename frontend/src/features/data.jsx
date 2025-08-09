import { configureStore } from "@reduxjs/toolkit";

import unitReducer from "./part.jsx";
import authReducer from "./auth.jsx";

export const data = configureStore({
  reducer: {
    area: unitReducer,
    auth: authReducer,
  },
});
