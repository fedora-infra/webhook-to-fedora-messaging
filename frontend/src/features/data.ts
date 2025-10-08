import { configureStore } from "@reduxjs/toolkit";

import authReducer from "./auth.ts";
import unitReducer from "./part.ts";

export const data = configureStore({
  reducer: {
    area: unitReducer,
    auth: authReducer,
  },
});

export type RootState = ReturnType<typeof data.getState>;
export type AppDispatch = typeof data.dispatch;
