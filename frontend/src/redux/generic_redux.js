import { combineReducers, createStore } from "redux"
import noticeReducer from "./notifications_redux"
import userReducer from "./user_redux"
import chatReducer from "./chat_redux"

const rootReducer = combineReducers({
	notice: noticeReducer,
	user: userReducer,
	chat: chatReducer,
})

export const store = createStore(rootReducer)
