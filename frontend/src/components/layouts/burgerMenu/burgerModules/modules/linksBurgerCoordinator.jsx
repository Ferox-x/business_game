import React from "react"
import "../burgerStyles/linksCoordinator.scss"
import "../burgerStyles/linkCoordinatorAttribute.scss"
import LinkBurger from "./linkBurger"
import { urls } from "../../../../../urls"

function LinksBurgerCoordinator(props) {
	return (
		<div className={"links_coordinator_container"}>
			<LinkBurger
				text={"Профиль"}
				icon={"link_coordinator_icon_profile"}
				url={urls.profileCoordinator}
			/>
			<LinkBurger
				text={"Игры"}
				icon={"link_coordinator_icon_game"}
				url={urls.profileCoordinator}
			/>
			<LinkBurger
				text={"Пользователи"}
				icon={"link_coordinator_icon_users"}
				url={urls.profileCoordinator}
			/>
		</div>
	)
}

export default LinksBurgerCoordinator
