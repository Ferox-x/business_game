import React from "react"
import "./playerBurgerMobile.scss"
import ButtonCreateGame from "../modules/buttonCreateGame"
import LinksBurgerCoordinator from "../modules/linksBurgerCoordinator"
import ButtonLogout from "../modules/buttonLogout"
import "../coordinatorBurgerMobile/coordinatorBurgerMobile.scss"
import LinksBurgerPlayer from "../modules/linksBurgerPlayer"
import PlayerInputJoinGame from "../modules/playerInputJoinGame"
import PlayerButtonJoinCode from "../modules/playerButtonJoinCode"

function PlayerBurgerMobile(props) {
	return (
		<div className={"burger_container_player_mobile"}>
			<div>
				<button className="btn_reset close_burger_menu"></button>
			</div>
			<div className="join_mobile_container">
				<PlayerInputJoinGame />
				<PlayerButtonJoinCode children={"Присоединиться"} />
			</div>
			<div className="links_burger_coordinator_container">
				<LinksBurgerPlayer />
			</div>
			<div className="button_logout_mobile_container">
				<ButtonLogout />
			</div>
		</div>
	)
}

export default PlayerBurgerMobile
