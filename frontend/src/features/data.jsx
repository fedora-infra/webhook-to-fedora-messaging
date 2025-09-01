import { configureStore } from "@reduxjs/toolkit";

import authReducer from "./auth.jsx";
import unitReducer from "./part.jsx";

export const data = configureStore({
  reducer: {
    area: unitReducer,
    auth: authReducer,
  },
});
