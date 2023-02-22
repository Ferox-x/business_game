import { combineReducers, createStore } from "redux"
import noticeReducer from "./notifications_redux"
import userReducer from "./user_redux"

const rootReducer = combineReducers({
	notice: noticeReducer,
	user: userReducer,
})

export const store = createStore(rootReducer)
