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
import PlayersList from "./playersList/playersList"
import TokensCheck from "./auth/tokensCheck"
import BusinessGame from "./businessGame/businessGame"
import UserEnterData from "./userEnterData/userEnterData"
import CoordinatorCreateGame from "./coordinatorCreateGame/coordinatorCreateGame"
import ViewUserProfile from "./viewUserProfile/viewUserProfile"
import GamesList from "./gamesList/gamesList"
import UserGameList from "./gamesList/userGameList/userGameList"
import ProfileEditCoordinator from "./profileEdit/profileEditCoordinator/profileEditCoordinator"
import SettingAttribute from "./settingsAttribute/settingAttribute"
import CreateGame from "./createGame/createGame"
import CoordinatorGame from "./businessGame/coordinatorGame"
import Game from "./businessGame/game"

function Urls(props) {
	return (
		<BrowserRouter>
			<Routes>
				# Общие ссылки
				<Route path={urls.mainPage} element={<MainPage />} />
				<Route path={urls.login} element={<Login />} />
				<Route path={urls.logout} element={<Logout />} />
				<Route path={urls.signUp + "/:code"} element={<Registration />} />
				<Route path={urls.signUp} element={<Registration />} />
				<Route path={urls.recoveryPassword} element={<RecoveryPassword />} />
				# Ссылки только для игрока
				<Route
					path={urls.profilePlayer}
					element={<RequireAuthPlayer children={<PlayerProfile />} />}
				/>
				<Route
					path={urls.profilePlayerEdit}
					element={<RequireAuthPlayer children={<EditProfile />} />}
				/>
				<Route
					path={urls.games}
					element={<RequireAuthPlayer children={<GamesList />} />}
				/>
				<Route
					path={urls.userGameList}
					element={<RequireAuthPlayer children={<UserGameList />} />}
				/>
				# Ссылки только для координатора
				<Route
					path={urls.profileCoordinator}
					element={<RequireAuthCoordinator children={<CoordinatorProfile />} />}
				/>
				<Route
					path={urls.profileCoordinatorEdit}
					element={<RequireAuthCoordinator children={<ProfileEditCoordinator />} />}
				/>
				<Route
					path={urls.settingAttribute}
					element={<RequireAuthCoordinator children={<SettingAttribute />} />}
				/>
				<Route
					path={urls.createGame}
					element={<RequireAuthCoordinator children={<CreateGame />} />}
				/>
				<Route
					path={urls.playersList}
					element={<RequireAuthCoordinator children={<PlayersList />} />}
				/>
				<Route
					path={urls.coordinatorGame}
					element={<RequireAuthCoordinator children={<CoordinatorGame />} />}
				/>
				# Ошибки
				<Route path={"*"} element={<Error404 />} />
				# Верстка
				<Route path={urls.businessGame} element={<Game />} />
				<Route path={urls.fillingData} element={<UserEnterData />} />
				<Route path={"/123"} element={<CoordinatorCreateGame />} />
				<Route path={urls.viewUserProfile} element={<ViewUserProfile />} />
			</Routes>
			<TokensCheck />
		</BrowserRouter>
	)
}

export default Urls
