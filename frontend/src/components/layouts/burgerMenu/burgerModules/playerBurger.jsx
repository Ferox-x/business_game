import React from "react"
import "./burgerStyles/playerBurger.scss"
import ButtonLogout from "./modules/buttonLogout"
import LinksBurgerPlayer from "./modules/linksBurgerPlayer"
import PlayerInputJoinGame from "./modules/playerInputJoinGame"
import PlayerButtonJoinCode from "./modules/playerButtonJoinCode"

function PlayerBurger(props) {
	return (
		<div className={"player_burger_container"}>
			<div className="player_burger_top">
				<LinksBurgerPlayer />
				<ButtonLogout />
			</div>
			<div className="join_container">
				<PlayerInputJoinGame />
				<PlayerButtonJoinCode children={"Присоединиться"} />
			</div>
		</div>
	)
}

export default PlayerBurger
