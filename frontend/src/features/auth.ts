import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { MD5 as md5 } from "crypto-js";

import { userManager } from "../config/oidc.ts";
import type { Profile } from "oidc-client";

type AuthDataState = {
  user: Profile | null
  disp: string
  status: string
}

const initialState: AuthDataState = {
  user: null,
  disp: "https://seccdn.libravatar.org/avatar/40f8d096a3777232204cb3f796c577b7?s=30",
  status: "idle",
}

export const loadUserData = createAsyncThunk("auth/loadUserData", async () => {
  const user = await userManager.getUser();
  return user && !user.expired ? user.profile : null;
});

const authData = createSlice({
  name: "auth",
  initialState: initialState,
  reducers: {
    wipeUserData: (auth: AuthDataState) => {
      auth.user = null;
      auth.disp = "https://seccdn.libravatar.org/avatar/40f8d096a3777232204cb3f796c577b7?s=30";
      auth.status = "idle";
    },
  },
  extraReducers: (plan) => {
    plan
      .addCase(loadUserData.pending, (auth: AuthDataState) => {
        auth.status = "load";
      })
      .addCase(loadUserData.fulfilled, (auth: AuthDataState, action: { payload: Profile | null }) => {
        auth.user = action.payload;
        auth.disp = action.payload && action.payload.email
          ? `https://seccdn.libravatar.org/avatar/${md5(action.payload.email.trim().toLowerCase()).toString()}?s=30&d=retro`
          : "https://seccdn.libravatar.org/avatar/40f8d096a3777232204cb3f796c577b7?s=30";
        auth.status = "pass";
      })
      .addCase(loadUserData.rejected, (auth: AuthDataState) => {
        auth.user = null;
        auth.disp = "https://seccdn.libravatar.org/avatar/40f8d096a3777232204cb3f796c577b7?s=30";
        auth.status = "fail";
      });
  },
});

export const { wipeUserData } = authData.actions;

export default authData.reducer;
