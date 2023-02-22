const defaultState = []

export default function noticeReducer(state = defaultState, action) {
	switch (action.type) {
		case "ADD_NOTICE":
			return [...state, action.payload]
		case "DELETE_NOTICE":
			return state.filter((notice) => notice.id !== action.payload.noticeID)
		default:
			return state
	}
}
