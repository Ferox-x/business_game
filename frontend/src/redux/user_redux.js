const defaultState = {
	user: {},
	isAuthenticated: false,
	isPlayer: false,
	isCoordinator: false,
}

export default function userReducer(state = defaultState, action) {
	switch (action.type) {
		case "SET_USER":
			const setUserState = {
				user: {
					...action.payload,
				},
				isAuthenticated: true,
			}
			localStorage.setItem("userState", JSON.stringify(setUserState))
			return setUserState

		case "SET_COORDINATOR":
			const coordinatorState = {
				user: {
					...action.payload,
				},
				isAuthenticated: true,
				isCoordinator: true,
				isPlayer: false,
			}
			localStorage.setItem("userState", JSON.stringify(coordinatorState))
			return coordinatorState

		case "SET_PLAYER":
			const playerState = {
				user: {
					...action.payload,
				},
				isAuthenticated: true,
				isCoordinator: false,
				isPlayer: true,
			}
			localStorage.setItem("userState", JSON.stringify(playerState))
			return playerState

		case "SET_PLAYER_ATTRIBUTES":
			const playerStateAttributes = {
				...state,
				attributes: { ...action.payload },
			}
			localStorage.setItem("userState", JSON.stringify(playerStateAttributes))
			return playerStateAttributes

		case "CLEAR_USER":
			localStorage.removeItem("userState")
			return defaultState

		default:
			const userState = localStorage.getItem("userState")
			if (userState) {
				return JSON.parse(userState)
			}
			return state
	}
}
