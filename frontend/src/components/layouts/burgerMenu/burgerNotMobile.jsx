import React from "react"
import "../styles/burger.scss"
import { useSelector } from "react-redux"
import PlayerBurger from "./burgerModules/playerBurger"
import CoordinatorBurger from "./burgerModules/coordinatorBurger"
import burger_active from "../../../static/img/burger_menu/burger_active.svg"

function BurgerNotMobile({ hide, burgerState, ...props }) {
	const user = useSelector((state) => state.user)

	let burgerStateClass

	switch (burgerState) {
		case false:
			burgerStateClass = "popup_hidden"
			break
		case true:
			burgerStateClass = "popup_open"
			break
	}

	let children = <></>

	if (user.isCoordinator) {
		children = <CoordinatorBurger />
	}

	if (user.isPlayer) {
		children = <PlayerBurger />
	}

	return (
		<>
			<div className={"burger " + burgerStateClass}>
				<div className={"burger_container"}>
					<button className="menu_burger btn-reset burger_active">
						<img
							onClick={hide}
							src={burger_active}
							alt="Menu"
							className={"menu_burger_icon"}
						/>
					</button>
					{children}
				</div>
			</div>
		</>
	)
}

export default BurgerNotMobile
