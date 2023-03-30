const genericUrls = {
	mainPage: "/",
	login: "/login",
	logout: "/logout",
	signUp: "/signup",
	recoveryPassword: "/recovery_password",
}

const playerUrls = {
	profilePlayer: "/profile",
	profilePlayerEdit: "/profile/edit",
	games: "/games",
	userGameList: "/player/games",
}

const coordinatorUrls = {
	profileCoordinator: "/profile/coordinator",
	settingAttribute: "/profile/coordinator/attributes",
	profileCoordinatorEdit: "/profile/coordinator/edit",
	createGame: "/create/game",
	playersList: "/players/list",
	coordinatorGame: "/coordinator/game",
}

const otherUrls = {
	businessGame: "/business/game",
	fillingData: "/filling/data",
	connectGame: "/connect/game",
	viewUserProfile: "/view/user/profile",
	userResults: "/user/results",
	lobby: "/lobby",
	userLobby: "/user/lobby",
	president: "/president",
	chat: "/chat",
	watchActiveGame: "/watch/active/game",
}

export const urls = {
	...genericUrls,
	...playerUrls,
	...coordinatorUrls,
	...otherUrls,
}
