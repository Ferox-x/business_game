import React from "react"
import "../burgerStyles/linksCoordinator.scss"
import "../burgerStyles/linkCoordinatorAttribute.scss"
import LinkBurger from "./linkBurger"
import { urls } from "../../../../../urls"

function LinksBurgerCoordinator(props) {
	return (
		<div className={"links_coordinator_container"}>
			<LinkBurger
				text={"Настройка полей"}
				icon={"link_coordinator_icon_profile"}
				url={urls.settingAttribute}
			/>
			<LinkBurger
				text={"Профиль"}
				icon={"link_coordinator_icon_profile"}
				url={urls.profileCoordinator}
			/>
			<LinkBurger
				text={"Список игр"}
				icon={"link_coordinator_icon_game"}
				url={urls.userGameList}
			/>
			<LinkBurger
				text={"Пользователи"}
				icon={"link_coordinator_icon_users"}
				url={urls.playersList}
			/>
		</div>
	)
}

export default LinksBurgerCoordinator
