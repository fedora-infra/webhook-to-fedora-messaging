import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { userManager } from "../config/oidc.js";
import md5 from "crypto-js/md5";

export const loadUserData = createAsyncThunk("auth/loadUserData", async () => {
  const user = await userManager.getUser();
  return user && !user.expired ? user.profile : null;
});

const authData = createSlice({
  name: "auth",
  initialState: {
    user: null,
    disp: "https://seccdn.libravatar.org/avatar/40f8d096a3777232204cb3f796c577b7?s=30",
    status: "idle",
  },
  reducers: {
    wipeUserData: (auth) => {
      auth.user = null;
      auth.disp = "https://seccdn.libravatar.org/avatar/40f8d096a3777232204cb3f796c577b7?s=30";
      auth.status = "idle";
      console.log("WIPED");
    },
  },
  extraReducers: (plan) => {
    plan
      .addCase(loadUserData.pending, (auth) => {
        auth.status = "load";
      })
      .addCase(loadUserData.fulfilled, (auth, action) => {
        auth.user = action.payload;
        auth.disp = action.payload
          ? `https://seccdn.libravatar.org/avatar/${md5(action.payload.email.trim().toLowerCase()).toString()}?s=30&d=retro`
          : "https://seccdn.libravatar.org/avatar/40f8d096a3777232204cb3f796c577b7?s=30";
        auth.status = "pass";
      })
      .addCase(loadUserData.rejected, (auth) => {
        auth.user = null;
        auth.disp = "https://seccdn.libravatar.org/avatar/40f8d096a3777232204cb3f796c577b7?s=30";
        auth.status = "fail";
      });
  },
});

export const { wipeUserData } = authData.actions;

export default authData.reducer;
