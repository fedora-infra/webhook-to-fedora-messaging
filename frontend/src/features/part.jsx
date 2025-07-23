import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { apiCall } from "./api.js";

export const keepServices = createAsyncThunk("area/keepServices", async (_, { rejectWithValue }) => {
  try {
    return await apiCall({ method: "GET", path: "/services" });
  } catch (err) {
    return rejectWithValue(err.toString());
  }
});

const makeunit = createSlice({
  name: "area",
  initialState: {
    services: [],
    creation: false,
    flagarea: false,
    flaghead: "",
    flagbody: "",
    flagstat: false,
    revoking: false,
    updating: false,
    reviving: false,
    binduuid: "",
    prevdata: {
      name: "",
      desc: "",
      type: "",
      user: "",
    },
    nextdata: {
      name: "",
      desc: "",
      type: "",
      user: "",
    },
    tintmode: "auto",
  },
  reducers: {
    keepFlagHead: (area, data) => {
      area.flaghead = data.payload;
    },
    keepFlagBody: (area, data) => {
      area.flagbody = data.payload;
    },
    wipeServices: (area) => {
      area.services = [];
    },
    showCreation: (area) => {
      area.creation = true;
    },
    hideCreation: (area) => {
      area.creation = false;
    },
    showFlagArea: (area) => {
      area.flagarea = true;
    },
    hideFlagArea: (area) => {
      area.flagarea = false;
    },
    passFlagStat: (area) => {
      area.flagstat = true;
    },
    failFlagStat: (area) => {
      area.flagstat = false;
    },
    showRevoking: (area) => {
      area.revoking = true;
    },
    hideRevoking: (area) => {
      area.revoking = false;
    },
    showUpdating: (area) => {
      area.updating = true;
    },
    hideUpdating: (area) => {
      area.updating = false;
    },
    showReviving: (area) => {
      area.reviving = true;
    },
    hideReviving: (area) => {
      area.reviving = false;
    },
    prepBindUuid: (area, data) => {
      area.binduuid = data.payload;
    },
    prepPrevData: (area, data) => {
      area.prevdata = data.payload;
    },
    prepNextData: (area, data) => {
      area.nextdata = data.payload;
    },
    prepTintMode: (area, data) => {
      area.tintmode = data.payload;
    },
  },
  extraReducers: (plan) => {
    plan.addCase(keepServices.fulfilled, (area, action) => {
      area.services = [...action.payload];
    });
  },
});

export const {
  keepFlagHead,
  keepFlagBody,
  wipeServices,
  showCreation,
  hideCreation,
  showFlagArea,
  hideFlagArea,
  passFlagStat,
  failFlagStat,
  showRevoking,
  hideRevoking,
  showUpdating,
  hideUpdating,
  showReviving,
  hideReviving,
  prepBindUuid,
  prepPrevData,
  prepNextData,
  prepTintMode,
} = makeunit.actions;

export default makeunit.reducer;
