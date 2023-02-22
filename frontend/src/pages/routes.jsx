import React from "react"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import { urls } from "../urls"
import MainPage from "./flatpages/mainPage/mainPage"
import Login from "./auth/login/login"
import Logout from "./auth/logout"
import Registration from "./auth/signup/registration"
import RecoveryPassword from "./auth/recoveryPassword/recoveryPassword"
import EditProfile from "./profileEdit/editProfile"
import Error404 from "./errors/error404"
import { RequireAuthCoordinator, RequireAuthPlayer } from "./permissions"
import PlayerProfile from "./profile/playerProfile"
import CoordinatorProfile from "./profile/coordinatorProfile"
import ProfileEditCoordinator from "./profileEdit/profileEditCoordinator/profileEditCoordinator"
import CreateGame from "./createGame/createGame"
import PlayersList from "./playersList/playersList"
import TokensCheck from "./auth/tokensCheck"

function Urls(props) {
	return (
		<BrowserRouter>
			<Routes>
				<Route path={urls.mainPage} element={<MainPage />} />
				<Route path={urls.login} element={<Login />} />
				<Route path={urls.logout} element={<Logout />} />
				<Route path={urls.signUp + "/:code"} element={<Registration />} />
				<Route path={urls.signUp} element={<Registration />} />
				<Route path={urls.recoveryPassword} element={<RecoveryPassword />} />
				#
				<Route
					path={urls.profilePlayer}
					element={<RequireAuthPlayer children={<PlayerProfile />} />}
				/>
				<Route
					path={urls.profileCoordinator}
					element={<RequireAuthCoordinator children={<CoordinatorProfile />} />}
				/>
				<Route
					path={urls.profilePlayerEdit}
					element={<RequireAuthPlayer children={<EditProfile />} />}
				/>
				<Route
					path={urls.profileCoordinatorEdit}
					element={<ProfileEditCoordinator />}
				/>
				<Route path={"*"} element={<Error404 />} />
				<Route path={urls.createGame} element={<CreateGame />} />
				<Route path={urls.playersList} element={<PlayersList />} />
			</Routes>
			<TokensCheck />
		</BrowserRouter>
	)
}

export default Urls
