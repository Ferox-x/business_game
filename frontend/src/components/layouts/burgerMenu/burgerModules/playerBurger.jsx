import React from "react"
import "./burgerStyles/playerBurger.scss"
import ButtonLogout from "./modules/buttonLogout"
import LinksBurgerPlayer from "./modules/linksBurgerPlayer"
import PlayerInputJoinGame from "./modules/playerInputJoinGame"
import ButtonPurple from "../../../UI-UX/button_purple"

function PlayerBurger(props) {
	return (
		<div className={"player_burger_container"}>
			<div className="player_burger_top">
				<LinksBurgerPlayer />
				<ButtonLogout />
			</div>
			<div className="join_container">
				<div className="join_container__input">
					<PlayerInputJoinGame />
				</div>
				<div className="join_container__btn">
					<ButtonPurple children={"Присоединиться"} />
				</div>
			</div>
		</div>
	)
}

export default PlayerBurger
