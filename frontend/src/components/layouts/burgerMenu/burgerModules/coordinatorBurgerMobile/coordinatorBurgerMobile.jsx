import React from "react"
import "./coordinatorBurgerMobile.scss"
import "../burgerStyles/buttonCreateGame.css"
import LinksBurgerCoordinator from "../modules/linksBurgerCoordinator"
import ButtonLogout from "../modules/buttonLogout"
import ButtonPurple from "../../../../UI-UX/button_purple"

function CoordinatorBurgerMobile({ hide, ...props }) {
	return (
		<div className={"burger_container_mobile"}>
			<div onClick={hide}>
				<button className="btn_reset close_burger_menu"></button>
			</div>
			<div className="button_create_game_mobile_container">
				<ButtonPurple children={"Создать игру"} />
			</div>
			<div className="links_burger_coordinator_container">
				<LinksBurgerCoordinator />
			</div>
			<div className="button_logout_mobile_container">
				<ButtonLogout />
			</div>
		</div>
	)
}

export default CoordinatorBurgerMobile
